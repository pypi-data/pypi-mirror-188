import pathlib

from .dataclass import Dataset, SRDatasets
from .utils import get_default_datasetpath

srdatasets = SRDatasets(
    SRDatasets=dict(
        NAIP20=Dataset(
            name="NAIP20",
            description="A benckmark dataset created using NAIP 2019 imagery",
            path=get_default_datasetpath(),
            metadata="https://zenodo.org/record/7579979/files/NAIP_20_metadata.csv?download=1",
            hr_sensor="NAIP: National Agriculture Imagery Program",
            hr_shape=(20, 1, 5, 2560, 2560),
            hr_url="https://zenodo.org/record/7579979/files/NAIP_20_y.dat?download=1",
            lr_sensor="Sentinel-2",
            lr_shape=(20, 11, 4, 128, 128),
            lr_url="https://zenodo.org/record/7579979/files/NAIP_20_X.dat?download=1",
            bands="R-G-B-NIR",
        )
    )
)
