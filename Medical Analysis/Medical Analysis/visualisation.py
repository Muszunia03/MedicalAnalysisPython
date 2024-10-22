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

# Callback to go to the previous MRI
def previous_MRI(dir_looper, data_dir):
    if dir_looper == 0:
        return os.listdir(data_dir).__sizeof__
    else:
        return dir_looper - 1

# Callback to go to the next MRI
def next_MRI(dir_looper, data_dir):
    if dir_looper < os.listdir(data_dir).__sizeof__:
        return dir_looper+1
    else:
        return 0


def show_slice(data, slice):
    data.shape
    plt.imshow(data[slice], cmap='Greys_r')
    plt.axis('off')
    plt.show()

def slice_plot(data):
    fig_rows = 4
    fig_cols = 4
    n_subplots = fig_rows * fig_cols
    n_slice = data.shape[0]
    step_size = n_slice // n_subplots
    plot_range = n_subplots * step_size
    start_stop = int((n_slice - plot_range) / 2)

    fig, axs = plt.subplots(fig_rows, fig_cols, figsize=[10, 10])

    for idx, img in enumerate(range(start_stop, plot_range, step_size)):
        axs.flat[idx].imshow(ndi.rotate(data[img, :, :], 90), cmap='Greys_r')
        axs.flat[idx].axis('off')
        
    plt.tight_layout()
    plt.show()


