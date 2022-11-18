

import numpy as np
import xarray as xr
import pandas as pd
from pathlib import Path
from tqdm import tqdm



def normalized_NSE(targ, pred, name_ndvi_pred = "ndvi_pred"):
    """Compute normalized Nash sutcliffe model efficiency of NDVI for one minicube
    
        The normalized Nash sutcliffe model efficiency scores the predictive skill of a model. It is identical to the most general definition of the coefficient of determination $R^2$.

        We score only on non-cloud observations (determined by the variable `s2_mask` in the target minicube).

        $$$
        nnse = 1 / (2 - nse)
        nse = \frac{\sum_{time} (obs - pred)^2}{\sum_{time} (obs - obsmean)^2}
        $$$

        Further reading: 
        - Normalized NSE https://en.wikipedia.org/wiki/Nash%E2%80%93Sutcliffe_model_efficiency_coefficient
        - NDVI https://de.wikipedia.org/wiki/Normalized_Difference_Vegetation_Index

        Args:
            targ (xr.Dataset): target minicube
            pred (xr.Dataset): prediction minicube, contains `name_ndvi_pred` variable with NDVI predictions during the forecasting period.
            name_ndvi_pred (str, optional): Name of the NDVI prediction variable, defaults to `"ndvi_pred"`.
    """

    pred_start_idx = len(targ.time.isel(time = slice(4,None,5))) - len(pred.time)

    nir = targ.s2_B8A.isel(time = slice(4,None,5)).isel(time = slice(pred_start_idx, None))
    red = targ.s2_B04.isel(time = slice(4,None,5)).isel(time = slice(pred_start_idx, None))
    mask = targ.s2_mask.isel(time = slice(4,None,5)).isel(time = slice(pred_start_idx, None))

    targ_ndvi = ((nir - red) / (nir + red + 1e-8)).where(mask == 0, np.NaN)
    pred_ndvi = pred[name_ndvi_pred]

    nnse = 1 / (2 - (1 - (((targ_ndvi - pred_ndvi)**2).sum("time") / ((targ_ndvi - targ_ndvi.mean("time"))**2).sum("time"))))

    df = xr.Dataset({"NNSE": nnse, "landcover": targ.esawc_lc}).to_dataframe()

    return df.drop(columns="sentinel:product_id", errors = "ignore")

def score_over_dataset(testset_dir, pred_dir, name_ndvi_pred = "ndvi_pred", verbose = True):
    """Compute normalized Nash sutcliffe model efficiency of NDVI for a full dataset

    Args:
        testset_dir (str): directory under which the target minicubes are stored. e.g. `"data/earthnet2021x/test/"`.
        pred_dir (str): directory under which the predictions are stored. e.g. `"preds/my_model/earthnet2021x-test/"`.
        name_ndvi_pred (str, optional): Name of the NDVI prediction variable, defaults to `"ndvi_pred"`.
        verbose (boolean, optional): Set to false to silence this function.
    """

    targetfiles = list(Path(testset_dir).glob("**/*.nc"))

    pred_dir = Path(pred_dir)
    
    if verbose:
        print(f"scoring {testset_dir} against {pred_dir}")

    dfs = []
    for targetfile in tqdm(targetfiles) if verbose else targetfiles:

        cubename = targetfile.name
        region = targetfile.parent.stem

        predfile = pred_dir/region/cubename

        targ = xr.open_dataset(targetfile)
        pred = xr.open_dataset(predfile)

        curr_df = normalized_NSE(targ, pred, name_ndvi_pred=name_ndvi_pred)
        curr_df["id"] = targetfile.stem

        dfs.append(curr_df)

    df = pd.concat(dfs).reset_index()

    tree_score = df[df.landcover == 10.].NNSE.mean()
    shrub_score = df[df.landcover == 20.].NNSE.mean()
    grass_score = df[df.landcover == 30.].NNSE.mean()
    crop_score = df[df.landcover == 40.].NNSE.mean()
    swamp_score = df[df.landcover == 90.].NNSE.mean()
    mangroves_score = df[df.landcover == 95.].NNSE.mean()
    moss_score = df[df.landcover == 100.].NNSE.mean()

    veg_micro_score = df[df.landcover <= 30.].NNSE.mean()
    veg_macro_score = np.nanmean([tree_score, shrub_score, grass_score])

    scores = {
        "veg_macro_score": veg_macro_score,
        "veg_micro_score": veg_micro_score,
        "tree_score": tree_score,
        "shrub_score": shrub_score,
        "grass_score": grass_score,
        "crop_score": crop_score,
        "swamp_score": swamp_score,
        "mangroves_score": mangroves_score,
        "moss_score": moss_score,
        "all_scores": df
    }

    if verbose:
        print("Done!")

    return scores