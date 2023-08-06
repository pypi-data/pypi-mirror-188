from typing import Union

import numpy as np
import torch

from .lpips import create_lpips_metric
from .ndvicheck import ndvicheck
from .psnr import PSNR
from .shanshan import create_shanshan_metric
from .ssim import SSIM


# Create the metrics
def metrics_creator(metrics: list, map_location: Union[str, torch.device] = None):
    container = dict()

    if "psnr" in metrics:
        container["psnr"] = PSNR().to(map_location)
    if "ssim" in metrics:
        container["ssim"] = SSIM(5).to(map_location)
    if "lpips" in metrics:
        container["lpips"] = create_lpips_metric(map_location=map_location)
    if "shanshan" in metrics:
        container["shanshan"] = create_shanshan_metric(map_location=map_location)
    if "ndvicheck" in metrics:
        container["ndvicheck"] = ndvicheck
    if "elf" in metrics:
        container["elf"] = None

    return container


def check_tensor_sanity(y_pred, y_true, mask):
    if not isinstance(y_pred, torch.Tensor):
        raise TypeError(f"Expected torch.Tensor but got {type(y_pred)}.")

    if not isinstance(y_true, torch.Tensor):
        raise TypeError(f"Expected torch.Tensor but got {type(y_true)}.")

    if not isinstance(mask, torch.Tensor):
        raise TypeError(f"Expected torch.Tensor but got {type(mask)}.")

    if y_pred.shape != y_true.shape:
        raise TypeError(
            f"Expected tensors of equal shapes, but got {y_pred.shape} and {y_true.shape}"
        )

    if not len(y_pred.shape) == 4:
        raise ValueError(
            f"Invalid y_pred shape, we expect BxCxHxW. Got: {y_pred.shape}"
        )

    if not len(y_true.shape) == 4:
        raise ValueError(f"Invalid img2 shape, we expect BxCxHxW. Got: {y_true.shape}")

    return True


def importance_path(mask: torch.Tensor):
    imgsize = mask.shape[-1]
    container = list()
    for i in range(0, imgsize, 224):
        for j in range(0, imgsize, 224):
            if i + 224 > imgsize:
                i = imgsize - 224
            if j + 224 > imgsize:
                j = imgsize - 224
            container.append(
                {
                    "xposition": i,
                    "yposition": j,
                    "importance": float(
                        torch.mean(mask[i : i + 224, j : j + 224])
                        .detach()
                        .cpu()
                        .numpy()
                    ),
                }
            )

    # get the 10 most important patches
    container_imp = sorted(container, key=lambda k: k["importance"], reverse=True)[:10]

    # get the xposition and yposition of the 5 most important patches
    xposition = [x["xposition"] for x in container_imp]
    yposition = [x["yposition"] for x in container_imp]

    return list(zip(xposition, yposition))


def metrics_generator(
    X: torch.Tensor,
    yhat: torch.Tensor,
    y: torch.Tensor,
    mask: torch.Tensor,
    metrics: dict,
    threshold: float,
):

    # Check tensor sanity
    check_tensor_sanity(yhat, y, mask)

    container = dict()

    # Estimate these metrics using cpu

    ## NDVIcheck
    if "ndvicheck" in metrics.keys():
        container["ndvicheck"] = float(
            metrics["ndvicheck"](X, yhat).detach().cpu().numpy()
        )

    ## PSNR
    if "psnr" in metrics.keys():
        container["psnr"] = float(
            metrics["psnr"](yhat, y, mask > threshold).detach().cpu().numpy()
        )

    ## SSIM
    if "ssim" in metrics.keys():
        container["ssim"] = float(
            np.mean(metrics["ssim"](yhat, y).detach().cpu().numpy())
        )

    ## LPIPS
    if "lpips" in metrics.keys():
        metrics["lpips"].eval()
        with torch.no_grad():
            container["lpips"] = float(
                metrics["lpips"](yhat[0, [2, 1, 0]], y[0, [2, 1, 0]]).detach().cpu()
            )

    ## Shanshan
    if "shanshan" in metrics.keys():
        metrics["shanshan"].eval()
        # Run 224x224 model on a nxn image
        shanshanvalues = list()
        important_patches = importance_path(mask)

        shanshanvalues = list()
        for i, j in important_patches:
            with torch.no_grad():
                shanshan_value = metrics["shanshan"](
                    yhat[0:1, [2, 1, 0], i : i + 224, j : j + 224],
                    y[0:1, [2, 1, 0], i : i + 224, j : j + 224],
                )
            shanshanvalues.append(float(shanshan_value.detach().cpu()))

        container["shanshan"] = np.array(shanshanvalues).mean()

    return container
