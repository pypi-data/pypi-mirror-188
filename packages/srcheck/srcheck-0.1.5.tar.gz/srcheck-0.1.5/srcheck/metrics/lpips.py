import io
import pathlib
from typing import Union

import torch

from ..utils import downloadfile, get_default_datasetpath, getFilename

__url__ = "https://zenodo.org/record/7585091/files/pmetric_lpips_alex.pt?download=1"

# Load the model
def create_lpips_metric(
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

    return torch.jit.load(filename, map_location=map_location)
