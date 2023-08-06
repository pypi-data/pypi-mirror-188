import io
import pathlib
from typing import Union

import timm
import torch
import torch.nn as nn
import torch.nn.functional as F
from timm.models.resnet import Bottleneck
from timm.models.vision_transformer import Block
from torchvision.ops.deform_conv import DeformConv2d

from ..utils import downloadfile, get_default_datasetpath, getFilename

__url__ = "https://zenodo.org/record/7587620/files/pmetric_shanshan_AHIQ_vit_p8_epoch33.pt?download=1"


class deform_fusion(nn.Module):
    def __init__(
        self, stride=1, in_channels=768 * 5, cnn_channels=256 * 3, out_channels=256 * 3
    ):
        super().__init__()
        # in_channels, out_channels, kernel_size, stride, padding
        self.d_hidn = 512
        self.conv_offset = nn.Conv2d(in_channels, 2 * 3 * 3, 3, 1, 1)
        self.deform = DeformConv2d(cnn_channels, out_channels, 3, 1, 1)
        self.conv1 = nn.Sequential(
            nn.Conv2d(
                in_channels=out_channels,
                out_channels=self.d_hidn,
                kernel_size=3,
                padding=1,
                stride=2,
            ),
            nn.ReLU(),
            nn.Conv2d(
                in_channels=self.d_hidn,
                out_channels=out_channels,
                kernel_size=3,
                padding=1,
                stride=stride,
            ),
        )

    def forward(self, cnn_feat, vit_feat):
        vit_feat = F.interpolate(vit_feat, size=cnn_feat.shape[-2:], mode="nearest")
        offset = self.conv_offset(vit_feat)
        deform_feat = self.deform(cnn_feat, offset)
        deform_feat = self.conv1(deform_feat)

        return deform_feat


class Pixel_Prediction(nn.Module):
    def __init__(self, inchannels=768 * 5 + 256 * 3, outchannels=256, d_hidn=1024):
        super().__init__()
        self.d_hidn = d_hidn
        self.down_channel = nn.Conv2d(inchannels, outchannels, kernel_size=1)
        self.feat_smoothing = nn.Sequential(
            nn.Conv2d(
                in_channels=256 * 3, out_channels=self.d_hidn, kernel_size=3, padding=1
            ),
            nn.ReLU(),
            nn.Conv2d(
                in_channels=self.d_hidn, out_channels=512, kernel_size=3, padding=1
            ),
        )

        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=512, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(),
        )
        self.conv_attent = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=1, kernel_size=1), nn.Sigmoid()
        )
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=1, kernel_size=1),
        )

    def forward(self, f_dis, f_ref, cnn_dis, cnn_ref):
        f_dis = torch.cat((f_dis, cnn_dis), 1)
        f_ref = torch.cat((f_ref, cnn_ref), 1)
        f_dis = self.down_channel(f_dis)
        f_ref = self.down_channel(f_ref)

        f_cat = torch.cat((f_dis - f_ref, f_dis, f_ref), 1)

        feat_fused = self.feat_smoothing(f_cat)
        feat = self.conv1(feat_fused)
        f = self.conv(feat)
        w = self.conv_attent(feat)
        pred = (f * w).sum(dim=2).sum(dim=2) / w.sum(dim=2).sum(dim=2)

        return pred


class SaveOutput:
    def __init__(self):
        self.outputs = []

    def __call__(self, module, module_in, module_out):
        self.outputs.append(module_out)

    def clear(self):
        self.outputs = []


def get_vit_feature(save_output):
    feat = torch.cat(
        (
            save_output.outputs[0][:, 1:, :],
            save_output.outputs[1][:, 1:, :],
            save_output.outputs[2][:, 1:, :],
            save_output.outputs[3][:, 1:, :],
            save_output.outputs[4][:, 1:, :],
        ),
        dim=2,
    )
    return feat


def create_model(pretrained):
    # load the parameters
    checkpoint = torch.load(pretrained)

    # Local features branch
    resnet50 = timm.create_model("resnet50", pretrained=True)

    # Global features branch
    vit = timm.create_model("vit_base_patch8_224", pretrained=True)

    # Deform layer
    deform_net = deform_fusion()
    deform_net.load_state_dict(checkpoint["deform_net_model_state_dict"])

    # Regresion layer
    regressor = Pixel_Prediction()
    regressor.load_state_dict(checkpoint["regressor_model_state_dict"])

    return resnet50, vit, deform_net, regressor


def init_save_outputs(resnet50, vit):
    save_output = SaveOutput()
    hook_handles = []
    for layer in resnet50.modules():
        if isinstance(layer, Bottleneck):
            handle = layer.register_forward_hook(save_output)
            hook_handles.append(handle)
    for layer in vit.modules():
        if isinstance(layer, Block):
            handle = layer.register_forward_hook(save_output)
            hook_handles.append(handle)

    return save_output


def get_resnet_feature(save_output):
    feat = torch.cat(
        (save_output.outputs[0], save_output.outputs[1], save_output.outputs[2]), dim=1
    )

    return feat


class ShanShanMetric(nn.Module):
    def __init__(self, pretrained, device=torch.device("cuda:0")):
        super().__init__()
        self.model = create_model(pretrained)
        if device.type == "cuda":
            self.resnet50 = self.model[0].cuda()
            self.vit = self.model[1].cuda()
            self.deform_net = self.model[2].cuda()
            self.regressor = self.model[3].cuda()
        else:
            self.resnet50 = self.model[0]
            self.vit = self.model[1]
            self.deform_net = self.model[2]
            self.regressor = self.model[3]
        self.save_output = init_save_outputs(self.resnet50, self.vit)
        self.device = device

    def forward(self, inputs, targets):
        # VIT (global branch)
        _ = self.vit(inputs.to(self.device))
        m1_dis = get_vit_feature(self.save_output)
        self.save_output.outputs.clear()

        _ = self.vit(targets.to(self.device))
        m2_ref = get_vit_feature(self.save_output)
        self.save_output.outputs.clear()

        # Disaggregate the results from 784 -> 28x28
        B, N, C = m2_ref.shape
        H, W = 28, 28

        m1_dis = m1_dis.transpose(1, 2).view(B, C, H, W)
        m2_ref = m2_ref.transpose(1, 2).view(B, C, H, W)

        # ResNet branch (local branch)
        _ = self.resnet50(inputs.to(self.device))
        m3_dis = get_resnet_feature(self.save_output)
        self.save_output.outputs.clear()
        m3_dis = self.deform_net(m3_dis, m2_ref)

        _ = self.resnet50(targets.to(self.device))
        m4_ref = get_resnet_feature(self.save_output)
        self.save_output.outputs.clear()
        m4_ref = self.deform_net(m4_ref, m2_ref)

        # make a prediction
        result = self.regressor(m1_dis, m2_ref, m3_dis, m4_ref).squeeze()

        return result


def create_shanshan_metric(
    mainfolder: pathlib.Path = None,
    map_location: Union[str, torch.device] = None,
    force: bool = False,
) -> io.BytesIO:

    if mainfolder is None:
        mainfolder = pathlib.Path(get_default_datasetpath())

    # Get the filename
    filename = mainfolder / getFilename(__url__)

    # Download the file
    if not filename.exists() or force:
        downloadfile(__url__, filename)

    return ShanShanMetric(filename, device=map_location)
