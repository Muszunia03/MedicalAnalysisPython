import os
import nibabel as nib
import pyvista as pv
import numpy as np
from pathlib import Path
import data_reading
import visualisation
import keyboard

# Load the NIfTI file (assumed to be 4D)
dir_looper = 0
img = data_reading.read_data_from_path("E:\GitHub\MedicalAnalysisPython\Task01_BrainTumour\imagesTr", dir_looper)
data = img.get_fdata()

# Extract the number of time points (or 4th dimension size)
num_timepoints = data.shape[3]

# Ensure the data is float32, which PyVista prefers for rendering
data = data.astype(np.float32)

# Initialize the time index
time_index = 0

# Create a PyVista plotter for rendering
plotter = pv.Plotter()

# Render the initial timepoint
visualisation.render_timepoint(time_index, plotter, num_timepoints, data)

# Callback to go to the previous timepoint
def previous_timepoint():
    global time_index
    time_index = max(time_index - 1, 0)  # Don't go below 0
    visualisation.render_timepoint(time_index, plotter, num_timepoints, data)

# Callback to go to the next timepoint
def next_timepoint():
    global time_index
    time_index = min(time_index + 1, num_timepoints - 1)  # Don't exceed num_timepoints
    visualisation.render_timepoint(time_index, plotter, num_timepoints, data)

# Add interactive buttons (arrows)
plotter.add_text("Use arrows to navigate timepoints", position='lower_left', font_size=10)
plotter.add_key_event("Left", previous_timepoint)
plotter.add_key_event("Right", next_timepoint)
# plotter.add_key_event("Up", visualisation.previous_MRI(dir_looper, "E:\GitHub\MedicalAnalysisPython\Task01_BrainTumour\imagesTr"))
# plotter.add_key_event("Down", visualisation.next_MRI(dir_looper, "E:\GitHub\MedicalAnalysisPython\Task01_BrainTumour\imagesTr"))

# Show the plot
plotter.show()

#Shows a slice of the scan
visualisation.show_slice(data, 96) #shows single lice

visualisation.slice_plot(data) #shows a couple of silces
