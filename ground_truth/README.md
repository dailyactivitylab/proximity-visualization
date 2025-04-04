# Ground Truth vs Model Predictions

## Overview

These files are used to display differences between the Ground Truth data and the Model Predicitons.  


## How To Use It

1. Use the Distress Detector Model to get the Model Predictions CSV file.

2. Download the Ground Data and Use the ground_truth_clean.py file in order to clean the data. Make sure you specify your particular file path. The output should result in an updated csv file.

3. Then use the groundtruth_vs_model.py file and replace the specific file paths to match the Model Predicitons CSV and the Updated Ground Truth file. After running the file, the output should be a visualization that showcases the Distress Events. The top graph should represent the Ground Truth Distress Events, and the bottom graph should represent the Model Predictions Distress Events. 
    
