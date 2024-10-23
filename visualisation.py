import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# Function to display slices of a 4D volume (multiple channels) with interactive navigation
def display_interactive_slices_multichannel(volume):
    num_slices = volume.shape[2]  # Number of slices along the Z-axis
    num_channels = volume.shape[3]  # Number of channels (assumed to be 4)
    current_slice = num_slices // 2  # Start at the middle slice

    fig, axes = plt.subplots(1, num_channels, figsize=(15, 5))
    img_displays = []

    # Initialize plots for each channel
    for i in range(num_channels):
        axes[i].set_title(f'Channel {i + 1}, Slice {current_slice + 1}/{num_slices}')
        img = axes[i].imshow(volume[:, :, current_slice, i], cmap='Purples')
        img_displays.append(img)
        axes[i].axis('off')

    def on_key(event):
        nonlocal current_slice
        if event.key == 'right':
            current_slice = (current_slice + 1) % num_slices  # Move forward
        elif event.key == 'left':
            current_slice = (current_slice - 1) % num_slices  # Move backward
        # Update plots for all channels
        for i in range(num_channels):
            axes[i].set_title(f'Channel {i + 1}, Slice {current_slice + 1}/{num_slices}')
            img_displays[i].set_data(volume[:, :, current_slice, i])
        fig.canvas.draw()

    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()

# Path to your NIfTI file (adjust the path accordingly)
nifti_file_path = '/Users/juliamarek/Downloads/BRATS_002.nii.gz'

# Load the NIfTI file
nifti_img = nib.load(nifti_file_path)

# Extract the image data as a NumPy array
nifti_data = nifti_img.get_fdata()

# Print shape to understand the dimensions of the file
print(f"Data shape: {nifti_data.shape}")  # Expecting a 4D array (X, Y, Z, Channels)

# Display the interactive slices for all 4 channels
display_interactive_slices_multichannel(nifti_data)
