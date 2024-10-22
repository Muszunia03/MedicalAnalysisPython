import os
import nibabel as nib
import pyvista as pv
import numpy as np
from pathlib import Path

def read_data_from_path(path, dir_looper): #Path to file and aumper of file in directory
    # Load the NIfTI file (assumed to be 4D)
    data_dir = Path(str(path))
    nifti_file = data_dir / str(os.listdir(data_dir)[dir_looper])
    img = nib.load(nifti_file)
    # data = img.get_fdata()

    # # Check if it's a 4D file
    # if data.ndim != 4:
    #     raise ValueError("Expected a 4D NIfTI file.")

    return img
