import os
import nibabel as nib
import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from nilearn import plotting
import scipy.ndimage as ndi

# Function to render a specific timepoint
def render_timepoint(time_index, plotter, num_timepoints, data):
    plotter.clear()  # Clear the previous plot
    # Extract the 3D volume for the current time point
    volume_data = data[:, :, :, time_index]
    
    # Wrap the 3D data and add it to the plotter
    volume = pv.wrap(volume_data)
    plotter.add_volume(volume, cmap="Greys_r", opacity="linear")
    
    # Update the title to show the current time index
    plotter.add_text(f"Timepoint: {time_index+1}/{num_timepoints}", font_size=12)

    # Render the plot
    plotter.render()

# Function to display slices of a 4D volume (multiple channels) with interactive navigation
def display_interactive_slices_multichannel(data):
    num_slices = data.shape[2]  # Number of slices along the Z-axis
    num_channels = data.shape[3]  # Number of channels (assumed to be 4)
    current_slice = num_slices // 2  # Start at the middle slice

    fig, axes = plt.subplots(1, num_channels, figsize=(15, 5))
    img_displays = []

    # Initialize plots for each channel
    for i in range(num_channels):
        axes[i].set_title(f'Channel {i + 1}, Slice {current_slice + 1}/{num_slices}')
        img = axes[i].imshow(data[:, :, current_slice, i], cmap='gray')
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
            img_displays[i].set_data(data[:, :, current_slice, i])
        fig.canvas.draw()

    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()


