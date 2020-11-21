# EarthNet Toolkit

The EarthNet2021 Toolkit

# Install
```
git clone git@git.bgc-jena.mpg.de:earthnet/earthnet-toolkit.git
cd earthnet-toolkit
pip install .
```

# Download
Ensure you have enough free disk space! We recommend 1TB.
```
import earthnet as en
en.Downloader.get(data_dir, splits)
```
Where  `data_dir` is the directory where EarthNet2021 shall be saved and `splits` is `"all"`or a subset of `["train","iid","ood","extreme","seasonal"]`.
