import torch


def ndvicheck(X: torch.Tensor, yhat: torch.Tensor):

    # Squeeze the tensor
    X, yhat = X.squeeze(0), yhat.squeeze(0)

    # Check tensor sanity
    ndvi_X = (X[3] - X[2]) / (X[3] + X[2])
    ndvi_yhat = (yhat[3] - yhat[2]) / (yhat[3] + yhat[2])

    # min max
    Xmin, Xmax = float(ndvi_X.min()), float(ndvi_X.max())

    # LR data
    values_X, _ = torch.histogram(
        ndvi_X.detach().cpu().flatten(), bins=100, range=(Xmin, Xmax)
    )

    # HR data
    values_yhat, _ = torch.histogram(
        ndvi_yhat.detach().cpu().flatten(), bins=100, range=(Xmin, Xmax)
    )

    return torch.cosine_similarity(values_X, values_yhat, dim=0)
