
# Offline Nude Image Scanner
Using notAI-tech/NudeNet (https://github.com/notAI-tech/NudeNet)

## Overview

This is an offline tool, written in python, designed to scan local directories for explicit or inappropriate images using the NudeNet library. 
It operates completely locally; no data leaves your machine *

(as per the requirements.txt configured version of the NudeNet library, which is 2.0.9, if you use another version, please ensure they did not update the code to use web-services!)
I did not perform an audit on the nudenet library. Feel free to check it out yourself, i see it is running without problems without an internet connection, but i did not conduct network analysis to see if it is communicating to a server when connection is availble.


The tool is ideal for system administrators who need to maintain the integrity of local file servers, among other use-cases.
It's also very useful if you want to clean up your computer from time to time!

### Features

-   **Offline Functionality**: Completely local analysis. No data leaves your machine.
-   **Deep Directory Scan**: Scans any directory and all of its subdirectories.
-   **System Directory Handling**: Capable of scanning system directories and even entire drives without crashing.
-   **Complexity Pre-Recognition**: Preliminary complexity check to avoid unnecessary scans and false positives, such as simple traffic signs.
-   **Real-time HTML Reports**: Generates an HTML report in real-time that can be accessed during the scan.
-   **Report Checkpoints**: Automatically saves report checkpoints every time the HTML report reaches 200KB.
-   **Cache Mechanism**: Utilizes a cache for problematic files. Cache is cleared when it reaches 15MB.
-   **Robust Detection**: Can pretty reliably detect a wide variety of explicit situations, including those with multiple people and positions. Images are only considered positively detected when NudeNet is at least 60% sure (a score of 0.6 or above for any matched class).
-   **HTML Report Features**: The HTML report is blurred by default for privacy and contains options to copy image paths to clipboard and to open full-sized images.
-   **Docker Support**: The tool can be dockerized, and both input and output directories can be mounted.

## Use-Cases

-   **System Administrators**: Can be used to scan local file servers for inappropriate or explicit content.
-   **Content Moderators**: A useful tool for initial content filtering.
-   **Personal Use**: Scan your own machine for accidental storage of explicit material.

## Important Note on False Positives

While the tool is pretty reliable, it may produce a number of false positives, especially in folders containing complex images like memes. However, this level of sensitivity also indicates the tool's robustness in correctly identifying true positives. Manual review is absolutely necessary to distinguish between the two.

⚠️ **Disclaimer**: This tool is designed to aid in the detection of explicit content but may produce false positives. Manual review is absolutely necessary.

## Requirements

-   Python 3.x
-   PIL (Pillow)
-   NudeNet
-   tqdm
-   cv2 (OpenCV)
-   webbrowser

## Installation

Install required Python packages. You can alternatively use the Dockerized version of the tool.

bashCopy code

`pip install Pillow nudenet tqdm opencv-python` 

## Running the Script

To run the script, navigate to the directory containing the script and execute:

bashCopy code

`python script_name.py` 

Replace `script_name.py` with the actual script's filename.

## Docker Usage

The tool can be dockerized for ease of deployment. Mount your input and output directories accordingly when running the Docker container.

bashCopy code

`docker run -v /path/to/input:/input -v /path/to/output:/output image-scanner:latest`# NudeNet Image Scanner

## Overview

This is an offline tool designed to scan local directories for explicit or inappropriate images using the NudeNet library. It operates completely locally; no data leaves your machine. The tool is ideal for system administrators who need to maintain the integrity of local file servers, among other use-cases.

### Features

-   **Offline Functionality**: Completely local analysis. No data leaves your machine.
-   **Deep Directory Scan**: Scans any directory and all of its subdirectories.
-   **System Directory Handling**: Capable of scanning system directories and even entire drives without crashing.
-   **Complexity Pre-Recognition**: Preliminary complexity check to avoid unnecessary scans and false positives, such as simple traffic signs.
-   **Real-time HTML Reports**: Generates an HTML report in real-time that can be accessed during the scan.
-   **Report Checkpoints**: Automatically saves report checkpoints every time the HTML report reaches 200KB.
-   **Cache Mechanism**: Utilizes a cache for problematic files. Cache is cleared when it reaches 15MB.
-   **Robust Detection**: Can pretty reliably detect a wide variety of explicit situations, including those with multiple people and positions. Images are only considered positively detected when NudeNet is at least 60% sure (a score of 0.6 or above for any matched class).
-   **HTML Report Features**: The HTML report is blurred by default for privacy and contains options to copy image paths to clipboard and to open full-sized images.
-   **Docker Support**: The tool can be dockerized, and both input and output directories can be mounted.

## Use-Cases

-   **System Administrators**: Can be used to scan local file servers for inappropriate or explicit content.
-   **Content Moderators**: A useful tool for initial content filtering.
-   **Personal Use**: Scan your own machine for accidental storage of explicit material.

## Important Note on False Positives

While the tool is reliable, it may produce a number of false positives, especially in folders containing complex images like memes. However, this level of sensitivity also indicates the tool's robustness in correctly identifying true positives. Manual review is absolutely necessary to distinguish between the two.

⚠️ **WARNING**: This tool is designed to aid in the detection of explicit content but may produce false positives. Manual review is absolutely necessary.

## Requirements

-   Python 3.x
-  Windows or Linux


## Installation

You can install all required Python packages by running the following command. A `requirements.txt` file is provided in the repository for easy installation.


`pip install -r requirements.txt` 

Alternatively, you can use the Dockerized version of the tool, which eliminates the need for manual package installation.

## Running the Script

To run the script, navigate to the directory containing the script and execute:


`python script_name.py` 

Replace `script_name.py` with the actual script's filename.

## Docker Usage

The tool can be dockerized for ease of deployment. Mount your input and output directories accordingly when running the Docker container.


`TBD`


## What does it see?
I uploaded an exemplary image to NudeNet to visualize what NudeNet sees:

This is an example for positive detection:

![example image with positive detection](https://raw.githubusercontent.com/yavuzitconsulting/offline-nudity-scanner/master/readme_data/positive_detection.png)

And an example for false positive detection that explains why you sometimes see false positives:
![example image with false positive detection](https://raw.githubusercontent.com/yavuzitconsulting/offline-nudity-scanner/master/readme_data/false_positive_detection.png)

You can see that the general form is recognized, i never analyzed the nudenet sourcecode, but i assume it is via conture and shape detection, since algorithm do not have a general understanding of what they are seeing, this can lead to false positives that have a very high confidence value (score).
But sadly, adjusting the minimum score to filter to a higher value might skip some actual positives.
I think 0.6 to 0.7 is a very good value to work with.

## Disclaimer

### Software Provided "As-Is"

This software is provided "as-is" and without any warranty, either express or implied. In no event will the authors, maintainers, or contributors be held liable for any damages, including, but not limited to, lost data or damages resulting from the use or inability to use the software.

While this software aims to provide accurate and reliable content filtering, it should not be considered foolproof. It may produce false positives and/or false negatives. Users should exercise their own judgement and discretion and should conduct manual reviews where appropriate.

Your use of this software signifies your agreement to this disclaimer. If you do not agree with these terms, please do not use the software.

##

## NOTE: THIS IS STILL IN DEVEOPMENT :) FEEL FREE TO JOIN, IT'S JUST FOR FUN!
