
from typing import Sequence, Union
import os
import urllib.request
from tqdm import tqdm
import tarfile


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


class Downloader():
    """Downloader Class for EarthNet2021
    """    
    __URL__ = {
        "train": ["url","train.tar.gz"],
        "iid": ["url","iid_test.tar.gz"],
        "ood": ["url","ood_test.tar.gz"],
        "extreme": ["url","extreme_test.tar.gz"],
        "seasonal": ["url","seasonal_test.tar.gz"]
    }

    def __init__(self, data_dir: str):
        """Initialize Downloader Class

        Args:
            data_dir (str): The directory where the data shall be saved in, we recommend data/dataset/
        """        
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok = True)

    @classmethod
    def get(cls, data_dir: str, splits: Union[str,Sequence[str]], overwrite: bool = False, delete: bool = True):
        """Download the EarthNet2021 Dataset
        
        Before downloading, ensure that you have enough free disk space. We recommend 1 TB.

        Specify the directory data_dir, where it should be saved. Then choose, which of the splits you want to download.
        All available splits: ["train","iid","ood","extreme","seasonal"]
        You can either give "all" to splits or a List of splits, for example ["train","iid"].

        Args:
            data_dir (str): The directory where the data shall be saved in, we recommend data/dataset/
            splits (Sequence[str]): Either "all" or a subset of ["train","iid","ood","extreme","seasonal"]. This determines the splits that are downloaded.
            overwrite (bool, optional): If True, overwrites an existing gzipped tarball by downloading it again. Defaults to False.
            delete (bool, optional): If True, deletes the downloaded tarball after unpacking it. Defaults to True.
        """        
        self = cls(data_dir)

        if isinstance(str, splits):
            if splits == "all":
                splits = ["train","iid","ood","extreme","seasonal"]

        assert(set(splits).issubset(set(["train","iid","ood","extreme","seasonal"])))

        for split in splits:
            dl_url, filename = self.__URL__[split]
            
            tmp_path = os.path.join(self.data_dir, filename)
            
            if overwrite and os.path.isfile(tmp_path):
                print("Removing temporary file.")
                os.remove(tmp_path)

            print(f"Downloading split {split} as temporary file {filename} to {self.data_dir}.")
            if not os.path.isfile(tmp_path):
                with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=filename) as t:
                    urllib.request.urlretrieve(dl_url, filename = tmp_path, reporthook=t.update_to)
                print("Downloaded!")
                print("Extracting tarball...")
                with tarfile.open(tmp_path, 'r:gz') as tar:
                    members = tar.getmembers()
                    for member in tqdm(iterable=members, total=len(members)):
                        tar.extract(member=member,path=self.data_dir)
                print("Extracted!")
                if delete:
                    print("Deleting tarball...")
                    os.remove(tmp_path)
            else:
                print(f"File existed allready! Please Erase {tmp_path} in case it shall be overwritten or call with overwrite=True")

if __name__ == "__main__":
    import fire
    fire.Fire(Downloader.get)