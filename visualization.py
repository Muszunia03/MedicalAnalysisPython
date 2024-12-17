
import nibabel as nib
import pyvista as pv
import numpy as np

class VisualizeScan:
    def __init__(self, niftiData):
        """
        Initialize the class for 3D volumetric visualization of a NIfTI file.
        
        Args:
            nifti_file_path (str): Path to the NIfTI file.
        """
        # Load the NIfTI file and its data
        self.data = niftiData
        self.data = self.data.astype(np.float32)
        
        # Initialize time index for 4D data
        self.time_index = 0
        self.num_timepoints = self.data.shape[3] if self.data.ndim == 4 else 1
        
        # Initialize PyVista plotter
        self.plotter = pv.Plotter()
        self.plotter.add_text("Use LEFT/RIGHT arrows to navigate timepoints", position='lower_left', font_size=10)
        self.plotter.add_key_event("Left", self.previous_timepoint)
        self.plotter.add_key_event("Right", self.next_timepoint)
        
        # Render the initial timepoint
        self.render_timepoint()
        self.plotter.show()  # Ensure this blocks until the user closes the window

    def previous_timepoint(self):
        """Navigate to the previous timepoint."""
        if self.num_timepoints > 1:  # Only applicable for 4D data
            self.time_index = max(self.time_index - 1, 0)
            self.render_timepoint()

    def next_timepoint(self):
        """Navigate to the next timepoint."""
        if self.num_timepoints > 1:  # Only applicable for 4D data
            self.time_index = min(self.time_index + 1, self.num_timepoints - 1)
            self.render_timepoint()

    def render_timepoint(self):
        """
        Renders the 3D volume for the current timepoint using PyVista.
        """
        self.plotter.clear()  # Clear the previous plot
        
        # Extract the current 3D volume
        if self.data.ndim == 4:
            volume_data = self.data[:, :, :, self.time_index]
        else:
            volume_data = self.data  # If 3D, use directly
        
        # Wrap the 3D data for PyVista
        volume = pv.wrap(volume_data)
        
        # Add the 3D volume to the PyVista plotter
        self.plotter.add_volume(volume, cmap="Greys_r", opacity="linear")
        self.plotter.add_text(f"Timepoint: {self.time_index + 1}/{self.num_timepoints}", font_size=12)
        self.plotter.render()