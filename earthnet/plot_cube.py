"""Tools for plotting Cubes
"""

import matplotlib.pyplot as plt 
import numpy as np
import matplotlib.colors as clr
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import copy

from pathlib import Path


def colorize(data, colormap = "ndvi", mask_red = None, mask_blue = None):
    t,h,w = data.shape
    in_data = data.reshape(-1)
    if mask_red is not None:
        in_data = np.ma.array(in_data, mask = mask_red.reshape(-1))  

    cmap = clr.LinearSegmentedColormap.from_list('ndvi', ["#cbbe9a","#fffde4","#bccea5","#66985b","#2e6a32","#123f1e","#0e371a","#01140f","#000d0a"], N=256) if colormap == "ndvi" else copy.copy(plt.get_cmap(colormap))
    cmap.set_bad(color='red')

    if mask_blue is None:
        return cmap(in_data)[:,:3].reshape((t,h,w,3))
    else:
        out = cmap(in_data)[:,:3].reshape((t,h,w,3))
        return np.stack([np.where(mask_blue, out[:,:,:,0],np.zeros_like(out[:,:,:,0])), 
                            np.where(mask_blue, out[:,:,:,1],np.zeros_like(out[:,:,:,1])), 
                            np.where(mask_blue, out[:,:,:,2],0.1*np.ones_like(out[:,:,:,2]))], axis = -1)


def gallery(array, ncols=10):
    nindex, height, width, intensity = array.shape
    padded = np.zeros((nindex, height + 2, width + 2, intensity))
    padded[:,1:-1,1:-1,:] = array
    nindex, height, width, intensity = padded.shape
    nrows = nindex//ncols
    assert nindex == nrows*ncols
    result = (padded.reshape(nrows, ncols, height, width, intensity)
              .swapaxes(1,2)
              .reshape(height*nrows, width*ncols, intensity))
    return result


def cube_gallery(cube, variable = "rgb", vegetation_mask = None, cloud_mask = True, save_path = None):
    """

    Plots a gallery view from a given Cube.

    Args:
        cube (np.ndarray): Numpy Array or loaded NPZ of Cube or path to Cube.
        variable (str, optional):  One of "rgb", "ndvi", "rr","pp","tg","tn","tx". Defaults to "rgb".
        vegetation_mask (np.ndarray, optional): If given uses this as red mask over non-vegetation. S2GLC data. Defaults to None.
        cloud_mask (bool, optional): If True tries to use the last channel from the cubes sat imgs as blue cloud mask, 1 where no clouds, 0 where there are clouds. Defaults to True.
        save_path (str, optional): If given, saves PNG to this path. Defaults to None.

    Returns:
        plt.Figure: Matplotlib Figure
    """    

    assert(variable in ["rgb", "ndvi", "rr","pp","tg","tn","tx"])

    if isinstance(cube, str):
        cube = np.load(cube)

    if isinstance(cube, np.lib.npyio.NpzFile):
        if variable in ["rgb","ndvi"]:
            if "highresdynamic" in cube:
                data = cube["highresdynamic"]
            else:
                for k in cube:
                    if 128 in cube[k].shape:
                        data = cube[k]
                        break
                raise ValueError("data does not contain satellite imagery.")
        elif variable in ["rr","pp","tg","tn","tx"]:
            if "mesodynamic" in cube:
                data = cube["mesodynamic"]
            else:
                raise ValueError("data does not contain E-OBS.")
    elif isinstance(cube, np.ndarray):
        data = cube

    hw = 128 if variable in ["rgb","ndvi"] else 80
    hw_idxs = [i for i,j in enumerate(data.shape) if j == hw]
    assert(len(hw_idxs) > 1)
    if len(hw_idxs) == 2 and hw_idxs != [1,2]:
        c_idx = [i for i,j in enumerate(data.shape) if j == min([j for j in data.shape if j != hw])][0]
        t_idx = [i for i,j in enumerate(data.shape) if j == max([j for j in data.shape if j != hw])][0]
        data = np.transpose(data,(t_idx,hw_idxs[0],hw_idxs[1],c_idx))

    if variable == "rgb":
        targ = np.stack([data[:,:,:,2],data[:,:,:,1],data[:,:,:,0]], axis = -1)
        targ[targ<0] = 0
        targ[targ>0.5] = 0.5
        targ = 2*targ
        if data.shape[-1] > 4 and cloud_mask:
            mask = data[:,:,:,-1]
            zeros = np.zeros_like(targ)
            zeros[:,:,:,2] = 0.1
            targ = np.where(np.stack([mask]*3,-1).astype(np.uint8) | np.isnan(targ).astype(np.uint8), zeros, targ)
        else:
            targ[np.isnan(targ)] = 0

    elif variable == "ndvi":
        targ = (data[:,:,:,3] - data[:,:,:,2]) / (data[:,:,:,2] + data[:,:,:,3] + 1e-6)
        if data.shape[-1] > 4 and cloud_mask:
            cld_mask = 1 - data[:,:,:,-1]
        else:
            cld_mask = None
        
        if vegetation_mask is not None:
            if isinstance(vegetation_mask, str):
                vegetation_mask = np.load(vegetation_mask)
            if isinstance(vegetation_mask, np.lib.npyio.NpzFile):
                vegetation_mask = vegetation_mask["landcover"]
            vegetation_mask = vegetation_mask.reshape(hw, hw)
            lc_mask = 1 - (vegetation_mask > 63) & (vegetation_mask < 105)
            lc_mask = np.repeat(lc_mask[np.newaxis,:,:],targ.shape[0], axis = 0)
        else:
            lc_mask = None
        targ = colorize(targ, colormap = "ndvi", mask_red = lc_mask, mask_blue = cld_mask)
    
    elif variable == "rr":
        targ = data[:,:,:,0]
        targ = colorize(targ, colormap = 'Blues', mask_red = np.isnan(targ))
    elif variable == "pp":
        targ = data[:,:,:,1]
        targ = colorize(targ, colormap = 'rainbow', mask_red = np.isnan(targ))
    elif variable in ["tg","tn","tx"]:
        targ = data[:,:,:, 2 if variable == "tg" else 3 if variable == "tn" else 4]
        targ = colorize(targ, colormap = 'coolwarm', mask_red = np.isnan(targ))

    grid = gallery(targ)

    fig = plt.figure(dpi = 300)
    plt.imshow(grid)
    plt.axis('off')
    if variable != "rgb":
        colormap = {"ndvi": "ndvi", "rr": "Blues", "pp": "rainbow", "tg": "coolwarm", "tn": "coolwarm", "tx": "coolwarm"}[variable]
        cmap = clr.LinearSegmentedColormap.from_list('ndvi', ["#cbbe9a","#fffde4","#bccea5","#66985b","#2e6a32","#123f1e","#0e371a","#01140f","#000d0a"], N=256) if colormap == "ndvi" else copy.copy(plt.get_cmap(colormap))
        divider = make_axes_locatable(plt.gca())
        cax = divider.append_axes("right", size="5%", pad=0.1)
        vmin, vmax = {"ndvi": (0,1), "rr": (0,50), "pp": (900,1100), "tg": (-50,50), "tn": (-50,50), "tx": (-50,50)}[variable]
        label = {"ndvi": "NDVI", "rr": "Precipitation in mm/d", "pp": "Sea-level pressure in hPa", "tg": "Mean temperature in °C", "tn": "Minimum Temperature in °C", "tx": "Maximum Temperature in °C"}[variable]
        plt.colorbar(cm.ScalarMappable(norm = clr.Normalize(vmin = vmin, vmax = vmax), cmap = cmap), cax = cax, label = label)

    if save_path is not None:
        save_path = Path(save_path)
        save_path.parents[0].mkdir(parents = True, exist_ok = True)
        plt.savefig(save_path, dpi = 300, bbox_inches='tight', transparent=True)

    return fig

if __name__ == "__main__":
    import fire
    fire.Fire(cube_gallery)