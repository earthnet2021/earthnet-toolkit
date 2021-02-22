# EarthNet Toolkit

The EarthNet2021 Toolkit.

# Documentation
Find more information on https://www.earthnet.tech.

# Install
```
pip install earthnet
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