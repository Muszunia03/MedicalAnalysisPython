import tkinter as tk
from tkinter import filedialog

class FileLoader:
    def __init__(self):
        self.file_path = None

    def open_file(self):
        """ Opens a file dialog and allows selection of NIfTI/DICOM files """
        # Initialize the Tkinter root window
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        # Open file dialog
        file_types = [("NIfTI files", "*.nii *.nii.gz"), ("All files", "*.*")]
        self.file_path = filedialog.askopenfilename(
            title="Select NIfTI/DICOM file",
            filetypes=file_types
        )

        # Print and return the file path
        if not self.file_path:
            print("No file selected.")
            return None
        else:
            print(f"File selected: {self.file_path}")
            return self.file_path
