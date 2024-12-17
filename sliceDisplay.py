import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox
import numpy as np

# from nilearn import plotting
# import scipy.ndimage as ndi
#klasa do wyœwietlania slice'ów, przyjmuje jako parametr array z nifti
#funkcje:
# 1. wyswietlenie œrodkowego slice
# 2. wyswietlenie nastêpnego
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

        # Adjust layout
        plt.subplots_adjust(bottom=0.25)  # Leave space for widgets

        # Add slider
        ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor='lightgoldenrodyellow')
        self.slider = Slider(ax_slider, 'Slice', 1, self.num_slices, valinit=self.current_slice + 1, valstep=1)
        self.slider.on_changed(self.on_slider_change)

        # Add text box
        ax_textbox = plt.axes([0.5, 0.03, 0.02, 0.05])
        self.text_box = TextBox(ax_textbox, 'Go to:', initial=str(self.current_slice + 1))
        self.text_box.on_submit(self.on_text_submit)

        # Connect key press events
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

        plt.show()  # Display the interactive window

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
        self.update_slider_and_display()

    def previous(self):
        """
        Display the previous slice.
        """
        self.current_slice = (self.current_slice - 1) % self.num_slices
        self.update_slider_and_display()

    def on_slider_change(self, val):
        """
        Handle slider value changes.
        """
        self.current_slice = int(val) - 1  # Slider is 1-based
        self.update_display()

    def on_text_submit(self, text):
        """
        Handle text box submissions.
        """
        try:
            slice_num = int(text) - 1  # Text box is 1-based
            if 0 <= slice_num < self.num_slices:
                self.current_slice = slice_num
                self.update_slider_and_display()
            else:
                print(f"Slice number must be between 1 and {self.num_slices}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def update_slider_and_display(self):
        """
        Sync slider position and update display.
        """
        self.slider.set_val(self.current_slice + 1)  # Update slider (without triggering on_slider_change)
        self.update_display()

    def on_key(self, event):
        """
        Handle key press events to navigate slices.
        """
        if event.key == 'right':
            self.next()
        elif event.key == 'left':
            self.previous()



