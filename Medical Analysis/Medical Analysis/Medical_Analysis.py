import os
import nibabel as nib
import pyvista as pv
import numpy as np
from pathlib import Path

# Load the NIfTI file (assumed to be 4D)
data_dir = Path("E:\GitHub\MedicalAnalysisPython\Task01_BrainTumour\imagesTr")
dir_looper = 1
nifti_file = data_dir / str(os.listdir(data_dir)[dir_looper])
img = nib.load(nifti_file)
data = img.get_fdata()

# Check if it's a 4D file
if data.ndim != 4:
    raise ValueError("Expected a 4D NIfTI file.")

# Extract the number of time points (or 4th dimension size)
num_timepoints = data.shape[3]

# Ensure the data is float32, which PyVista prefers for rendering
data = data.astype(np.float32)

# Initialize the time index
time_index = 0

# Create a PyVista plotter for rendering
plotter = pv.Plotter()

# Function to render a specific timepoint
def render_timepoint(time_index):
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

# Callback to go to the previous timepoint
def previous_timepoint():
    global time_index
    time_index = max(time_index - 1, 0)  # Don't go below 0
    render_timepoint(time_index)

# Callback to go to the next timepoint
def next_timepoint():
    global time_index
    time_index = min(time_index + 1, num_timepoints - 1)  # Don't exceed num_timepoints
    render_timepoint(time_index)

# Callback to go to the previous MRI
def previous_MRI():
    if dir_looper == 0:
        dir_looper = os.listdir(data_dir).__sizeof__
    else:
        dir_looper - 1

# Callback to go to the next MRI
def next_MRI():
    if dir_looper < os.listdir(data_dir).__sizeof__:
        dir_looper+1
    else:
        dir_looper = 0

# Render the initial timepoint
render_timepoint(time_index)

# Add interactive buttons (arrows)
plotter.add_text("Use arrows to navigate timepoints", position='lower_left', font_size=10)
plotter.add_key_event("Left", previous_timepoint)
plotter.add_key_event("Right", next_timepoint)
# plotter.add_key_event("Up", previous_MRI)
# plotter.add_key_event("Down", next_MRI)

# Show the plot
plotter.show()
