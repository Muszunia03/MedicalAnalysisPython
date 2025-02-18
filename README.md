# 1. Setup nnUNetv2
Create and activate a Conda environment
conda create -n nnunetv2_env python=3.10 -y
conda activate nnunetv2_env

Install nnUNetv2
pip install nnunetv2

Set up environment variables (adjust paths as needed)
Set up environment variables (adjust paths as needed)
export nnUNetv2_results="/path/to/nnUNet_results"  # Path where pretrained models will be stored
# 2. Prepare Your Data
# 3. Provide path to pre-trained model (results file)
# 4. Run Inference (Prediction on New Scans)
nnUNetv2_predict -i /path/to/imagesTs -o /path/to/output -d DatasetXXX -c 3d_fullres -f all
# 5. Evaluate Model Performance (Optional for Dice Coefficient)
nnUNetv2_evaluate -i /path/to/predictions -r /path/to/ground_truth -d DatasetXXX -c 3d_fullres


