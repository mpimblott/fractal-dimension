from pathlib import Path
from typing import Union
import PIL.Image as Image
import numpy as np

def get_np_from_png(path: Path):
    '''
    Read a png into a numpy array.
    '''
    return np.asarray(Image.open(path).convert('L'))

sfx_map = {
    '.png': get_np_from_png
}

def get_np_from_path(path: Union[Path,str]):
    '''
    Get an np array from a filepath

    Args: path (Path): path to file containing the data
    '''
    if not isinstance(path, (Path, str)):
        raise Exception("Not a path or string.")
    if isinstance(path, str):
        path = Path(path)
    if not path.is_file():
        raise Exception(f"Error {path} is not a file.")
    
    sfx = path.suffix
    if sfx in sfx_map:
        return sfx_map[sfx](path)
    else:
        raise Exception(f"{sfx} is not a supported file extension.")
    
