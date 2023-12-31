
# Offline NSFW Image Scanner
Offline NSFW / Nudity detector based on notAI-tech/NudeNet (https://github.com/notAI-tech/NudeNet).
This tool can be used to scan entire System drives, external drives, usb sticks or any other storage media.
When scanning the system, it takes system directories into account (when run as administrator) and can even find stuff hidden in WSL, Recycle Bin and more.
Easy-to-use tool to detect adult content / restricted content on your own devices, on network devices, on fileservers and more.

## It's easy! (TL;DR)
Don't be afraid stranger! 
It's easier than it looks!
While this readme file has lots of text for you to read, if you're just looking for a quick and easy tool to use, this is where the meat is at!

Just clone or download this repository and run "start.bat", that's it!

The tool comes with its own python executable and virtual environment.

## Overview
This is an offline tool, written in python, designed to scan local directories for explicit or inappropriate images using the NudeNet library. 
It operates completely locally; no data leaves your machine *

(as per the current version of the NudeNet library, which is 2.0.9, if you use another version, please ensure they did not update the code to use web-services!)
**I did not perform an audit on the nudenet library. Feel free to check it out yourself, i see it is running without problems without an internet connection, but i did not conduct network analysis to see if it is communicating to a server when connection is availble.**


The tool is ideal for system administrators who need to maintain the integrity of local file servers, among other use-cases.

**The tool enables you to conduct "Audits", it will store the report files based on their run-start time, so you can just automatically conduct these tests and collect the reports, ideally, the results should be pushed into a more advanced AI that can execute the actual Audit / Data review, this way, administrators do not have any human intervention, in a future version, i might integrate the YITCs own trained AI into the process and provide the model, but to this day, no such model exists and since the tool is supposed to be data-safe, i will not provide an API**

### Features


-   **Easy-To_use**: No Prerequisites! I'm shipping a compatible python version and setting up a virtual environment, just run "start.bat"!
-   **Offline Functionality**: Completely local analysis. No data leaves your machine.
-   **Deep Directory Scan**: Scans any directory and all of its subdirectories.
-   **System Directory Handling**: Capable of scanning system directories and even entire drives without crashing.
-   **Complexity Pre-Recognition**: Preliminary complexity check to avoid unnecessary scans and false positives, such as simple traffic signs.#, icons, or assets of Frameworks.
-   **Fine-Grained Recognition**: The NudeNet library scans the images and sorts them based on a list of labels such as "Covered_Breast, Exposed_Breast" and more, it then applies confidence levels to these detections.
-   **Real-time HTML Reports**: Generates an HTML report in real-time that can be accessed during the scan.
-   **Report Checkpoints**: Automatically saves report checkpoints every time the HTML report reaches 200KB.
-   **Cache Mechanism**: Utilizes a cache for problematic files (meaning files with long filenames, strange characters, emojis in their name, permission problems). Cache is cleared when it reaches 15MB and when the process finishes.
-   **Robust Detection**: Can pretty reliably detect a wide variety of explicit situations, including those with multiple people and positions. Images are only considered positively detected when NudeNet is at least 60% sure (a score of 0.6 or above for any matched class). 
-   **HTML Report Features**: The HTML report is blurred by default for privacy and contains options to copy image paths to clipboard and to open full-sized images, it is easily possible to navigate between reports.
-   **Docker Support**: The tool can be dockerized, and both input and output directories can be mounted. (TBD)
-   **Customization**: The detection is improved by checking the confidence level of each detection and calculating the median, the user can pass the "--minscore" argument to configure the median, the default is 0.6, higher values lead to less false-positives, but also more misses.

## Use-Cases

-   **System Administrators**: Can be used to scan local file servers for inappropriate or explicit content.
-   **Content Moderators**: A useful tool for initial content filtering.
-   **Personal Use**: Scan your own machine for accidental storage of explicit material.

## Important Note on False Positives

While the tool is pretty reliable, it may produce a number of false positives, especially in folders containing complex images like memes. However, this level of sensitivity also indicates the tool's robustness in correctly identifying true positives. Manual review is absolutely necessary to distinguish between the two.

⚠️ **Disclaimer**: This tool is designed to aid in the detection of explicit content but may produce false positives. Manual review is absolutely necessary.

## Requirements

Windows 10 or higher

## Installation

Clone or download the repository.

Run "start.bat"

Wait for the setup to finish, the CMD will prompt you to enter the directory to scan.
You can enter entire drives such as "C:"
Then hit Enter, wait for it to finish, the results are in the "reports" directory.

## Running the Script (manually)

To run the script, navigate to the directory containing the script and execute:


`python script.py [YOUR PATH]` 

Replace `[YOUR PATH]` with the actual directory path or drive, for example:


`python script.py C:/` 

if you just run

`python script.py` 

It will display all possible arguments and options.

## Docker Usage

The tool can be dockerized for ease of deployment. Mount your input and output directories accordingly when running the Docker container.


`TO BE DONE!`


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
