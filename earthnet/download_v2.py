


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