

import numpy as np
import s3fs
import xarray as xr
from pathlib import Path
from tqdm import tqdm

SPLITS = {
    "earthnet2021x": ["train","iid","ood","extreme","seasonal"]
}

def download(dataset = "earthnet2021x", split = "train", save_directory = "data/", proxy = None, limit = None):
    """Download the recent EarthNet datasets
        
        Before downloading, ensure that you have enough free disk space. We recommend 1 TB.

        Specify the directory `save_directory`, where it should be saved. Then choose, which of the splits you want to download.
        All available splits: 
            - For dataset `"earthnet2021x"`: `["train","iid","ood","extreme","seasonal"]`
        
        You can also give `"all"` to splits to download all splits of a particular dataset.

        Args:
            dataset (str): The dataset you wish to download.
            split (str): A split of the given dataset, can also be `"all"` to download all splits of a given dataset
            save_directory (str): The directory where the data shall be saved in, we recommend data/
            proxy (str, optional): If you need to use a http-proxy to access the internet, you may specify it here.
            limit (int, optional): If you only want to download a certain number of samples, you can set a limit here.
    """  
    if split == "all":
        for split in SPLITS[dataset]:
            download(dataset = dataset, split = split, save_directory=save_directory, proxy = proxy, limit = limit)
    else:
        s3 = s3fs.S3FileSystem(anon=True,
                client_kwargs={
                'endpoint_url': 'https://s3.bgc-jena.mpg.de:9000',
                'region_name': 'thuringia',
                },
                config_kwargs = {
                "proxies": {'http': proxy}
                } if proxy else {}
            )

        print(f"Finding files of {dataset}, split {split} to download.")
        files = s3.find(f"earthnet/{dataset}/{split}")
        print(f"Downloading files of {dataset}, split {split}")
        for file in tqdm(files[:limit] if limit else files):
            savepath = Path(save_directory)/file[9:]
            savepath.parent.mkdir(parents = True, exist_ok = True)
            s3.download(file, str(savepath))
        print(f"Downloaded {dataset}, split {split}.")


def load_minicube(dataset = "earthnet2021x", split = "train", id = "29SND_2018-09-03_2019-01-30_441_569_2745_2873_6_86_42_122", region = None, proxy = None):
    """Load a minicube from a recent EarthNet dataset

        Will give you a minicube loaded from the cloud.

        All available splits: 
            - For dataset `"earthnet2021x"`: `["train","iid","ood","extreme","seasonal"]`

        Args:
            dataset(str): The dataset
            split (str): The split
            id (str): The id of the minicube
            region (str, optional): If you specify the region, downloading will be faster
            proxy (str, optional): If you need to use a http-proxy to access the internet, you may specify it here.
    
    """
    s3 = s3fs.S3FileSystem(anon=True,
            client_kwargs={
            'endpoint_url': 'https://s3.bgc-jena.mpg.de:9000',
            'region_name': 'thuringia',
            },
            config_kwargs = {
            "proxies": {'http': proxy}
            } if proxy else {}
        )
    if region:
        file = f"earthnet/{dataset}/{split}/{region}/{id}.nc"
    else:
        print(f"Searching for {id}...")
        file = s3.glob(f"earthnet/{dataset}/{split}/**/{id}.nc")[0]
        print(f"Found {id}.")
    
    mc = xr.open_dataset(s3.open(file))

    return mc

def load_en21x_as_npz(minicube_path):
    """Load a minicube from the EarthNet2021x dataset as an EarthNet2021-like fake NPZ

        Will return a dictionary with keys `['highresdynamic', 'highresstatic', 'mesodynamic', 'mesostatic']` as in the `.npz` files from EarthNet2021.
        
        Attention!
            - `highresdynamic` has just 5 channels (like in the EarthNet2021 test sets)
            - mesoscale data is just a single value repeated over the 80x80 mesoscale grid
            - the COPDEM in EarthNet2021x has slightly higher resolution than the EU-DEM from EarthNet2021.
            - This function returns a dictionary and not a `numpy.lib.npyio.NpzFile`

        Args:
            minicube_path (str): Path to the minicube from EarthNet2021x to be loaded as a fake NPZ.
    
    """

    minicube = xr.open_dataset(minicube_path)

    minicube["s2_mask"] = minicube.s2_mask.where(minicube.s2_mask == 0.0, 1.0)

    hrd_fake = minicube[["s2_B02", "s2_B03", "s2_B04", "s2_B8A", "s2_mask"]].to_array("band").isel(time = slice(4, None, 5)).transpose("lat", "lon", "band", "time").values

    eobs_shift = xr.DataArray(data = [0.0, -900., 50., 50., 50.], coords = {"var": ["eobs_rr", "eobs_pp", "eobs_tg", "eobs_tn", "eobs_tx"]})
    eobs_scale = xr.DataArray(data = [50., 200., 100., 100., 100.], coords = {"var": ["eobs_rr", "eobs_pp", "eobs_tg", "eobs_tn", "eobs_tx"]})

    md_fake = ((minicube[["eobs_rr", "eobs_pp", "eobs_tg", "eobs_tn", "eobs_tx"]].to_array("var") + eobs_shift)/eobs_scale).transpose("var", "time").values[None, None, :, :].repeat(80, 0).repeat(80, 1)

    hrs_fake = (minicube.cop_dem.values[:, :, None] + 2000)/4000

    ms_fake = np.nanmean(hrs_fake) * np.ones((80, 80, 1))

    npz_fake = {
        'highresdynamic': hrd_fake,
        'highresstatic': hrs_fake,
        'mesodynamic': md_fake,
        'mesostatic': ms_fake
    }

    return npz_fake