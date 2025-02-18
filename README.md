# MRI Glioma Detection - AI-Powered Application

## Overview
This project is an AI-powered application designed to analyze and visualize 3D brain scans for the detection of gliomas. The system processes NIfTI files, analyzes MRI scans in 2D slices, and provides a heatmap visualization highlighting potential tumor regions. The goal is to assist doctors, specialists, and non-expert users in identifying gliomas quickly and accurately.

## Features
### ✅ Successfully Implemented Features
- **NIfTI File Handling**: The application successfully opens and reads NIfTI (.nii, .nii.gz) files without errors.
- **MRI Scan Visualization**: Users can view MRI scans in both pre- and post-processing states.
- **2D Slice Analysis**: The AI processes 3D scans by analyzing individual 2D slices.
- **Heatmap Generation**: The system overlays heatmaps on detected regions to highlight potential tumor locations.
- **User Interface**: A Python-based GUI allows users to open, view, and interact with MRI scans.
- **Scan Comparison**: The application provides an interface for viewing MRI scans before and after AI detection.
- **Binary Yes/No Output**: Provides a clear classification of glioma presence, eliminating the need for manual heatmap interpretation.ded.

### ❌ Not Yet Implemented
- **AI Output in Text Form**: The system does not currently generate a textual explanation of the AI's findings.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.1
- Required libraries (install with `pip`):
  ```sh
  pip install numpy nibabel matplotlib opencv-python tkinter
  ```

### Running the Application
1. Clone the repository:
   ```sh
   git clone https://github.com/Muszunia03/MedicalAnalysisPython.git
   ```
2. Navigate to the project folder:
   ```sh
   cd MedicalAnalysisPython
   ```
3. Run the main script:
   ```sh
   python main.py
   ```

## Future Enhancements
We are pleased with the results so far and are considering further improvements, such as:
- Implementing AI-generated text explanations for better interpretability.
- Providing a binary classification output (Yes/No) for glioma detection.
- Enhancing visualization options and user interaction features.


## Usage
   
# 1. Setup nnUNetv2
For example create and activate a Conda environment
conda create -n nnunetv2_env python=3.10 -y
conda activate nnunetv2_env

# Install nnUNetv2
pip install nnunetv2

# Set up environment variables (adjust paths as needed)
export nnUNetv2_results="/path/to/nnUNet_results"  # Path where pretrained models will be stored

# 2. Prepare Your Data
Each training image must have a modality suffix (_0000, _0001, etc.)
BRATS_001_0001.nii.gz  
BRATS_002_0003.nii.gz  


# 3. Provide path to pre-trained model (results directory)
export nnUNetv2_results="/path/to/pretrained_model_directory"

# 4. Run Inference (Prediction on New Scans)
nnUNetv2_predict -i /path/to/imagesTs -o /path/to/output -d DatasetXXX -c 3d_fullres -f all

# 5. Evaluate Model Performance (Optional for Dice Coefficient)
nnUNetv2_evaluate -i /path/to/output -r /path/to/ground_truth -d DatasetXXX -c 3d_fullres

