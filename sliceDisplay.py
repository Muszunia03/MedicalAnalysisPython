import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

# from nilearn import plotting
# import scipy.ndimage as ndi
#klasa do wyświetlania slice'ów, przyjmuje jako parametr array z nifti
#funkcje:
# 1. wyswietlenie środkowego slice
# 2. wyswietlenie następnego
# 3. wyswietlenie poprzedniego

class ReturnSlice:
    def __init__(self, slice_arr):
        """
        Initialize the ReturnSlice class and display the middle slice for all channels.
        """
        # Ensure input is 4D (X, Y, Z, Channels)
        if slice_arr.ndim != 4:
            raise ValueError(f"Input array must be 4D (X, Y, Z, Channels), but got shape {slice_arr.shape}")

        self.slice_arr = slice_arr
        self.num_slices = slice_arr.shape[2]  # Number of slices along the Z-axis
        self.num_channels = slice_arr.shape[3]  # Number of channels
        self.current_slice = self.num_slices // 2  # Start at the middle slice

        # Set up figure and axes
        self.fig, self.axes = plt.subplots(1, self.num_channels, figsize=(15, 5))
        self.img_displays = []

        # Initialize plots for each channel
        for i in range(self.num_channels):
            self.axes[i].set_title(f'Channel {i + 1}, Slice {self.current_slice + 1}/{self.num_slices}')
            img = self.axes[i].imshow(slice_arr[:, :, self.current_slice, i], cmap='gray')
            self.img_displays.append(img)
            self.axes[i].axis('off')

        # Adjust layout and show the figure
        self.fig.tight_layout()
        self.fig.canvas.draw()
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        plt.show()  # Keep the window interactive

    def update_display(self):
        """
        Update the display for all channels to the current slice.
        """
        for i in range(self.num_channels):
            self.img_displays[i].set_data(self.slice_arr[:, :, self.current_slice, i])
            self.axes[i].set_title(f'Channel {i + 1}, Slice {self.current_slice + 1}/{self.num_slices}')
        self.fig.canvas.draw_idle()  # Trigger an interactive redraw

    def next(self):
        """
        Display the next slice.
        """
        self.current_slice = (self.current_slice + 1) % self.num_slices
        self.update_display()

    def previous(self):
        """
        Display the previous slice.
        """
        self.current_slice = (self.current_slice - 1) % self.num_slices
        self.update_display()

    def on_key(self, event):
        """
        Handle key press events to navigate slices.
        """
        if event.key == 'right':
            self.next()
        elif event.key == 'left':
            self.previous()

    def keep_running(self):
        """
        Keep the program running until the user closes the figure.
        """
        print("Use the right/left arrow keys to navigate slices. Close the window to exit.")
        while plt.fignum_exists(self.fig.number):
            plt.pause(0.1)  # Small pause to prevent high CPU usage


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
slicer = ReturnSlice(nifti_data)
slicer.keep_running()




