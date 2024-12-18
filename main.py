from file_loader import FileLoader
import visualization
import sliceDisplay
import nibabel as nib
import numpy as np

# Initialize FileLoader
loader = FileLoader()
file_path = loader.open_file()  # Select the file

if file_path:
    # Load NIfTI data
    nifti_img = nib.load(file_path)
    nifti_data = nifti_img.get_fdata()

    # Ensure data is 4D
    if nifti_data.ndim == 3:
        nifti_data = nifti_data[..., np.newaxis]

    print(f"Data shape: {nifti_data.shape}")  # Confirm the data shape

    # Pass data to slicer and viewer
    slicer = sliceDisplay.ReturnSlice(nifti_data)
    slicer.keep_running()

    viewer = visualization.VisualizeScan(nifti_data)
else:
    print("No file selected. Exiting program.")