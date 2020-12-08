from tqdm import tqdm
import numpy as np

class Multicube():
    """MultiCube Class for EarthNet Dataset
    """
    
    def cuberescale(multicube):
        """Rescale the variables in the cube to unit of measurements with physically meaningful
        

        Args:
            path (str): "Path/to/multicube"
            array (str): Either "context","target","full". Determines the frames that are loaded.
            overwrite (bool, optional): If True, overwrites an existing gzipped tarball by downloading it again. Defaults to False.
            delete (bool, optional): If True, deletes the downloaded tarball after unpacking it. Defaults to True.
        """     
        return multicube
    
    @classmethod
    def load(cls, path=None, array="full", predpath=None, onlypred= False, rescale=True):
        """Safe load of entire multicube
        
        Given the name of a sample returns cube arrays from context, target or full length that are
        safely loaded. If pred path is given, target frames are loaded both from groundtruth and the 
        prediction directory. If onlypred is true, target frames are only loaded from prediction path.
        If rescale is

        Args:
            path (str): "Path/to/dataset/multicube"
            array (str): Either "context","target","full". Determines the frames that are loaded.
            predpath (str): "Path/to/predicted/multicube"
            onlypred (bol): only load target frames from prediction.
            rescale: rescales variables to meaningful units.
        """        
    