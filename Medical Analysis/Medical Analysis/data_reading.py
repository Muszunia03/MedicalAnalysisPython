import os
import nibabel as nib
import pyvista as pv
import numpy as np
from pathlib import Path
import requests
import io

#Reading data from GitHub repo
def read_data_from_github():
    # Public GitHub repo details
    token = "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"  # Required if the repo is private
    repo = "Muszunia03/MedicalAnalysisPython/tree/b2035951629314a3e50ea90e8e5323c6e6f02e08/Task01_BrainTumour/imagesTr"  # Format: user/repo
    branch = "main"  # Branch where files are located
    directory_path = "Task01_BrainTumour/imagesTr"  # Folder containing NIfTI files

    # GitHub API URL for listing directory contents
    url = f"https://api.github.com/repos/{repo}/contents/{directory_path}?ref={branch}"

    # Authorization header
    headers = {"Authorization": f"token {token}"} if token else {}
    
    # Get the list of files in the directory
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        files = response.json()
        print(f"Found {len(files)} files in directory '{directory_path}':")

        nifti_arr = []

        # Iterate over files and load them in memory if they're NIfTI files (.nii or .nii.gz)
        for file in files:
            file_name = file['name']
            download_url = file['download_url']  # Direct download URL for the file
            if file_name.endswith('.nii') or file_name.endswith('.nii.gz'):
                print(f"Reading {file_name} directly from GitHub...")
            
                # Fetch the file content
                file_response = requests.get(download_url)

                # Load the file content into memory as a BytesIO object
                file_content = io.BytesIO(file_response.content)

                # Use nibabel to load the NIfTI file from the in-memory object
                nifti_image = nib.load(file_content)
            
                # Now you can process the NIfTI file
                print(f"Loaded NIfTI file: {file_name}")
                print(f"Shape of the NIfTI file: {nifti_image.shape}")
                # You can add more operations here, like processing or visualizing the data.
                nifti_arr.insert(nifti_image)

        return nifti_arr

    else:
        print(f"Error fetching directory contents: {response.status_code} - {response.text}")


def read_data_from_path(path, dir_looper): #Path to file and aumper of file in directory
    # Load the NIfTI file (assumed to be 4D)
    data_dir = Path(str(path))
    nifti_file = data_dir / str(os.listdir(data_dir)[dir_looper])
    img = nib.load(nifti_file)
    # data = img.get_fdata()

    # # Check if it's a 4D file
    # if data.ndim != 4:
    #     raise ValueError("Expected a 4D NIfTI file.")

    return img
