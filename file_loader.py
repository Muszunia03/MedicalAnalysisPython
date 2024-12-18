import tkinter as tk
from tkinter import filedialog
import pydicom
import nibabel as nib

class FileLoader:
    def __init__(self):
        self.file_path = None

    def open_file(self):
        """ Opens a file dialog and allows selection of NIfTI/DICOM files """
        # Initialize the Tkinter root window
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        # Open file dialog
        #file_types = [("NIfTI files", "*.nii *.nii.gz"), ("All files", "*.*")]
        self.file_path = filedialog.askopenfilename(
            title="Select a file"
        )

        # Print and return the file path
        if self.file_path and self.is_valid_file(self.file_path):
            print(f"File selected: {self.file_path}")
            return self.file_path
        else:
            print("Invalid file type or no file selected.")
            return None

    @staticmethod
    def is_valid_file(file_path):
        """Check if a file is either a NIfTI or DICOM file."""
        try:
            nib.load(file_path)  # Try loading as NIfTI
            return True
        except Exception:
            pass

        try:
            pydicom.dcmread(file_path)  # Try loading as DICOM
            return True
        except Exception:
            pass

        return False