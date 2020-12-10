from tqdm import tqdm
import numpy as np
from pathlib import Path
import os

class Multicube():
    """MultiCube Class for EarthNet Dataset
    """
    
    def __init__(self, cubenames= True):
        """Data handling
        
        Args:
            cubename (str): True if the only provided pointer to a cube sample is the name of it "cube.npz", False if full paths are given
        """
        #WIP
        self.cubelist = None
    
    
    def cube_rescale(multicube):
        """Rescale the variables in the cube to unit of measurements with physically meaningful
        

        Args:
            path (str): "Path/to/multicube"
            array (str): Either "context","target","full". Determines the frames that are loaded.
            overwrite (bool, optional): If True, overwrites an existing gzipped tarball by downloading it again. Defaults to False.
            delete (bool, optional): If True, deletes the downloaded tarball after unpacking it. Defaults to True.
        """
        #WIP
        return multicube

    @classmethod
    def load(cls, path: str, predpath= None, array="full", onlypred= False, rescale=False):
        """Safe load of entire multicubes
        
        Given the path of a sample returns cube arrays from context, target or full length that are
        safely loaded. If a cube name is given, it searches for it across split/tile subfolder.
        If pred path is given, target frames are loaded both from groundtruth and the 
        prediction directory. If onlypred is true, target frames are only loaded from prediction path.
        If rescale is true variables are converted to original data units.

        Args:
            path (str): "Path/to/dataset/multicube.npz"
            array (str): Either "context","target","full". Determines the frames that are loaded.
            predpath (str): "Path/to/predicted/multicube"
            onlypred (bol): only load target frames from prediction.
            rescale: rescales variables to meaningful units.
        """        
        #WIP
        if "_split" in path:
            path_parts = path.split("_split")
            filename = path.split("/")[-1]
            tilename = path.split("/")[-2]
            context_path = os.path.join(path_parts[0] +"_split","context",tilename, filename)
            target_path = os.path.join(path_parts[0] +"_split","target",tilename, filename)

            context_mc = np.load(context_path)
            target_mc = np.load(target_path)
            
            full_mc['highresdynamic'] = np.concatenate((context_mc['highresdynamic'], target_mc['highresdynamic']), axis=3)
            full_mc['mesodynamic'] = np.concatenate((context_mc['mesodynamic'], target_mc['mesodynamic']), axis=3)
            full_mc['highresstatic'] = context_mc['highresstatic']
            full_mc['mesostaic'] = context_mc['mesostaic']
        else:
            full_mc = np.load(path)
        
        if rescale:
            full_mc = cls.cube_rescale(full_mc)
                
        return full_mc