import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# Function to display slices of a 3D volume with interactive navigation
def display_interactive_slices(volume):
    num_slices = volume.shape[2]  # Number of slices along the Z-axis
    current_slice = num_slices // 2  # Start at the middle slice

    fig, ax = plt.subplots()
    ax.set_title(f'Slice {current_slice + 1}/{num_slices}')
    img_display = ax.imshow(volume[:, :, current_slice], cmap='gray')
    
    def on_key(event):
        nonlocal current_slice
        if event.key == 'right':
            current_slice = (current_slice + 1) % num_slices  # Move forward
        elif event.key == 'left':
            current_slice = (current_slice - 1) % num_slices  # Move backward
        ax.set_title(f'Slice {current_slice + 1}/{num_slices}')
        img_display.set_data(volume[:, :, current_slice])
        fig.canvas.draw()

    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()

# Path to your NIfTI file (adjust the path accordingly)
nifti_file_path = '/Users/jas1ek/Documents/MedicalAnalysisPython/Task01_BrainTumour/imagesTr/BRATS_001.nii.gz'

# Load the NIfTI file
nifti_img = nib.load(nifti_file_path)

# Extract the image data as a NumPy array
nifti_data = nifti_img.get_fdata()

# Print shape to understand the dimensions of the file
print(f"Data shape: {nifti_data.shape}")  # Expecting a 4D array (X, Y, Z, Channel)

# Select a specific channel (modify this index as needed)
selected_channel = 0
volume = nifti_data[:, :, :, selected_channel]

# Display the interactive slices of the 3D volume
display_interactive_slices(volume)
