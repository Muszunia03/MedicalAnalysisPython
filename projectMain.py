import sliceDisplay
import visualization
import nibabel as nib
import numpy as np

#use example

# Display the interactive slices for all 4 channels
# Load your NIfTI data
nifti_file_path = '/Users/wojtekkurpanik/Documents/GitHub/MRIPROJECT/Data/imagesTr/BRATS_001.nii.gz'
nifti_img = nib.load(nifti_file_path)
nifti_data = nifti_img.get_fdata()

# Ensure the data is 4D (if not, reshape or raise an error)
if nifti_data.ndim == 3:
    nifti_data = nifti_data[..., np.newaxis]  # Add a channel dimension if missing

# Check the shape of the data
print(f"Data shape: {nifti_data.shape}")  # Should be (X, Y, Z, Channels)

# Create a ReturnSlice instance
slicer = sliceDisplay.ReturnSlice(nifti_data)
slicer.keep_running()

# Example usage of 3d model:
viewer = visualization.VisualizeScan(nifti_data)