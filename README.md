# EarthNet Toolkit

The EarthNet2021 Toolkit.

# Documentation
Find more information on https://www.earthnet.tech.

# Install
```
pip install earthnet
```

# Downloading new dataset EarthNet2023 - Africa

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10659371.svg)](https://doi.org/10.5281/zenodo.10659371)

Ensure you have enough free disk space! We recommend 1.5TB.
```
import earthnet as entk
entk.download(dataset = "earthnet2023", split = "all", save_directory = "data_dir")
```
Where `data_dir` is the directory where EarthNet2023 - Africa shall be saved and `split` is `"all"` or a subset of `["train", "test]`.

When using EarthNet2023 - Africa, please for now cite the DOI `10.5281/zenodo.10659371`, until there is an original publication on the dataset. 
```
Vitus Benson, Christian Requena-Mesa, Jeran Poehls, Lazaro Alonso, Claire Robin, Nuno Carvalhais, Markus Reichstein. (2024). 
EarthNet Toolkit for accessing the EarthNet2023 - Africa dataset.
Zenodo. https://doi.org/10.5281/zenodo.10659371
```

> This work has received funding from the European Union’s Horizon 2020 Research and Innovation Project DeepCube, under Grant Agreement Numbers 101004188.

# Downloading new dataset EarthNet2021x

Ensure you have enough free disk space! We recommend 1TB.
```
import earthnet as en
en.download(dataset = "earthnet2021x", split = "train", save_directory = "data_dir")
```
Where  `data_dir` is the directory where EarthNet2021 shall be saved and `split` is `"all"`or a subset of `["train","iid","ood","extreme","seasonal"]`.

# Scoring new dataset EarthNet2021x

Save your predictions for one test set in one folder in the following way:
`{pred_dir/region/cubename.nc}`
Name your NDVI prediction variable as `"ndvi_pred"`.

Then use the `data_dir/dataset/split` as the targets.

Then compute the normalized NSE over the full dataset:
```
import earthnet as en
scores = en.score_over_dataset(Path/to/targets, Path/to/predictions)
print(scores["veg_macro_score"])
```

Alternatively you can score a single minicube:
```
import earthnet as en
df = en.normalized_NSE(Path/to/target_minicube, Path/to/prediction_minicube)
print(df.describe())
```


# Download
Ensure you have enough free disk space! We recommend 1TB.
```
import earthnet as en
en.Downloader.get(data_dir, splits)
```
Where  `data_dir` is the directory where EarthNet2021 shall be saved and `splits` is `"all"`or a subset of `["train","iid","ood","extreme","seasonal"]`.


Alternatively if package was installed locally:
```
cd earthnet-toolkit/earthnet/
python download.py -h
python download.py "Path/To/Download/To" "all"
```
For using in the commandline.

# Use EarthNetScore
Save your predictions for one test set in one folder in one of the following ways:
`{pred_dir/tile/cubename.npz, pred_dir/tile/experiment_cubename.npz}`
Then use the Path/To/Download/To/TestSet as the targets.

Then use the EarthNetScore:
```
import earthnet as en
en.EarthNetScore.get_ENS(Path/to/predictions, Path/to/targets, data_output_file = Path/to/data.json, ens_output_file = Path/to/ens.json)
```

# Get Coordinates for a cube
Getting Lon-Lat-coordinates for a cube or tile is as simple as:
```
import earthnet as en
en.get_coords_from_cube(cubename, return_meso = False)
en.get_coords_from_tile(tilename)
```

# Plotting a cube
Creating a gallery view for a cube is done as follows:
```
import earthnet as en
import matplotlib.pyplot as plt
fig = en.cube_gallery(cubepath, variable = "ndvi")
plt.show()
```

Creating a NDVI timeseries view for a cube is done as follows:
```
import earthnet as en
import matplotlib.pyplot as plt
fig = en.cube_ndvi_timeseries(predpath, targpath)
plt.show()
```
