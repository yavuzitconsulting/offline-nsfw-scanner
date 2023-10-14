import os
import argparse
from PIL import Image
from nudenet import NudeDetector
from tqdm import tqdm
import sys
import re
import shutil
from datetime import datetime
import hashlib
import glob
import uuid
import cv2
import webbrowser

all_labels = [
    "BUTTOCKS_EXPOSED",
    "FEMALE_BREAST_EXPOSED",
    "FEMALE_GENITALIA_EXPOSED",
    "MALE_BREAST_EXPOSED",
    "ANUS_EXPOSED",
    "BELLY_EXPOSED",
    "MALE_GENITALIA_EXPOSED",
]


default_detection_score = 0.6

def create_cache_directory():
    cache_dir = 'cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

def get_cache_filename(filename):
    return os.path.join('cache', filename)

def create_reports_directory():
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%d%m%Y_%H%M")
    reports_dir = "reports\\" + f'reports_{formatted_date}'

    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        
def get_latest_report_directory():
    # Get a list of all directories in the "reports" subdirectory that match the "reports_*" pattern
    report_directories = [d for d in glob.glob('reports/reports_*') if os.path.isdir(d)]

    # Sort the directories by name (which includes the date and time)
    report_directories.sort()

    # Get the latest directory (which will be the last one after sorting)
    latest_directory = report_directories[-1] if report_directories else None

    return latest_directory

def get_report_filename(report_number):
    # Get the latest report directory
    latest_directory = get_latest_report_directory()

    if latest_directory:
        # Extract the date and time portion from the directory name
        date_time_part = latest_directory.replace('reports\\reports_', '')

        # Format it into a datetime object
        report_datetime = datetime.strptime(date_time_part, "%d%m%Y_%H%M")

        # Format the report filename using the latest directory's date and time
        report_filename = f'{latest_directory}/nudenet_report_{report_number}.html'

        return report_filename

    # Return a default path if there are no report directories
    return f'reports/nudenet_report_{report_number}.html'

def create_new_report(report_number):
    report_file = get_report_filename(report_number)
    with open(report_file, 'w') as report:
        report.write(get_report_header())
import os  # Importing os module

def update_report(report_file, image_path, matched_classes):
    # Replace single backslashes with double backslashes
    image_path_escaped = image_path.replace('\\', '\\\\')
    
    # Get only the filename with extension
    file_name_with_extension = os.path.basename(image_path)
    matched_classes_str = ',<br>'.join([f"{item['class']} [{item['score']:.2f}]" for item in matched_classes])
    match_scores_avg = round(sum(item['score'] for item in matched_classes) / len(matched_classes), 2) if matched_classes else 0

    clipboard_emoji = '\U0001F4CB'  # Unicode code point for clipboard emoji

    with open(report_file, 'a', encoding='utf-8') as report:
        report.write(f"""
        <li>
            <a href="{image_path_escaped}" target="_blank">
                <div class="zoom-container">
                    <img src='{image_path_escaped}' alt='Image'>
                </div>
            </a>
            <br>
            <div class="file-info">
            <span class="file-path-label" onclick="copyToClipboard('{image_path_escaped}')">{file_name_with_extension}</span>
            <span class="file-description" onclick="copyToClipboard('{image_path_escaped}')">Matched Classes:<br>{matched_classes_str}<br></span>
            <span class="average-scores" onclick="copyToClipboard('{image_path_escaped}')">[avg: {match_scores_avg}]</span>
            <span class="clipboard-button" onclick="copyToClipboard('{image_path_escaped}')"><Button>{clipboard_emoji}</Button></span>
            </div>
        </li>
        """)


def get_report_header():
    return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>NudeNet Detection Report</title>
            <style>
                body {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                }}

                ul {{
                    list-style: none;
                    padding: 0;
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                }}

                li {{
                    margin: 10px;
                    text-align: center;
                    display: flex;
                    border: 1px dotted;
                    border-radius: 5px;
                }}

                img, .file-path-label {{
                    cursor: pointer;
                    transition: transform 0.1s ease-in-out;
                    font-weight: 600;
                    word-wrap: break-word;
                    margin-bottom: 0.7rem;
                }}

               
                img {{
                    width: 150px;
                    height: 150px;
                    filter: blur(20px);
                    cursor: pointer;
                    transition: transform 0.2s;  /* Updated */
                }}
                
                
                img:hover {{
                    transform: scale(2);  /* Updated */
                }}

                .file-info {{
                    width:300px;
                    display: flex;
                    flex-direction:column;
                    justify-content: space-between;
                }}

                .clicked {{
                    transform: scale(0.95);
                }}
                
                
                .zoom-container {{
                    position: relative;
                    width: 150px;
                    height: 150px;
                    overflow: hidden;
                }}

                .zoom-container img {{
                    width: 100%;
                    height: auto;
                    transition: transform 0.2s;
                    filter: blur(20px);
                }}

                .zoom-container img.unblurred:hover {{
                    transform: scale(2);  /* Adjust scale factor as needed */
                    overflow: auto;
                }}
                
                .average-scores{{
                    font-size: small;
                }}
                
                .clipboard-button{{  
                margin-top: 0.5rem;
                }}

            </style>
            <script>
                function copyToClipboard(text) {{
                    const textArea = document.createElement("textarea");
                    textArea.value = text;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                }}

                   function toggleBlur() {{
                    const images = document.querySelectorAll('.zoom-container img');
                    const blurCheckbox = document.getElementById('blurCheckbox');
                    const blurValue = blurCheckbox.checked ? 'blur(20px)' : 'none';

                    images.forEach(img => {{
                        img.style.filter = blurValue;
                        if (blurValue === 'none') {{
                            img.classList.add('unblurred');
                        }} else {{
                            img.classList.remove('unblurred');
                        }}
                    }});
                }}

                function animateClick(event) {{
                    const element = event.target;
                    element.classList.add('clicked');
                    setTimeout(() => element.classList.remove('clicked'), 100);
                }}
            </script>
        </head>
        <body>
            <label for="blurCheckbox">Blur Images</label>
            <input type="checkbox" id="blurCheckbox" checked onchange="toggleBlur()">
            <ul onclick="animateClick(event)">
    """



def sanitize_filename(filename):
    # Extract the file extension from the original filename
    _, file_extension = os.path.splitext(filename)

    # Generate a simple UID as the filename without dashes
    uid = str(uuid.uuid4().hex).replace('-', '')

    # Append the original file extension to the UID
    sanitized_filename = uid + file_extension
    return sanitized_filename

def create_error_log_directory():
    error_log_dir = 'logs/error_logs'
    if not os.path.exists(error_log_dir):
        os.makedirs(error_log_dir)

def get_error_log_filename(error_log_number):
    return f'logs/error_logs/error_log_{error_log_number}.txt'

def create_new_error_log(error_log_number):
    error_log_file = get_error_log_filename(error_log_number)
    with open(error_log_file, 'w') as error_log:
        error_log.write("Error Log:\n")


def log_error(error_log_number, message):
    error_log_file = get_error_log_filename(error_log_number)
    with open(error_log_file, 'a', encoding='utf-8') as error_log:
        error_log.write(f"{datetime.now()} - {message}\n")


def clean_cache_directory(cache_dir, max_size_bytes):
    # Get the current size of the cache directory
    current_size = sum(os.path.getsize(os.path.join(cache_dir, f)) for f in os.listdir(cache_dir) if os.path.isfile(os.path.join(cache_dir, f)))

    # Check if the current size exceeds the maximum allowed size
    if current_size > max_size_bytes:
        # List all files in the cache directory and sort them by modification time
        files = [(os.path.join(cache_dir, f), os.path.getmtime(os.path.join(cache_dir, f))) for f in os.listdir(cache_dir) if os.path.isfile(os.path.join(cache_dir, f))]
        files.sort(key=lambda x: x[1])  # Sort by modification time (oldest first)

        # Calculate the amount of space to free up
        space_to_free = current_size - max_size_bytes

        # Iterate through the files and delete the oldest ones until enough space is freed
        for file_path, _ in files:
            if current_size <= max_size_bytes:
                break
            file_size = os.path.getsize(file_path)
            os.remove(file_path)
            current_size -= file_size


def clear_console():
    sys.stdout.write("\033[H\033[J")  # ANSI escape code to clear the screen



def is_complex_image(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Failed to load image from path: {image_path}")

    # Apply binary thresholding
    _, thresh = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours_thresh, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Apply Canny edge detection
    edges = cv2.Canny(image, 100, 200)

    # Find contours in the edge-detected image
    contours_edges, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Assuming a threshold of 5 contours to distinguish between simple and complex images
    return len(contours_thresh) > 5 or len(contours_edges) > 5

def scan_directory(directory, report_number, error_log_number):
    images_with_detections = []
    nude_detector = NudeDetector()

    create_error_log_directory()
    create_new_error_log(error_log_number)
    create_cache_directory()

    max_cache_size_bytes = 15 * 1024 * 1024

    for subdir, _, files in os.walk(directory):
        clear_console()
        # Calculate the total number of files in the current directory
        total_files_in_directory = len(files)

        # Create a new progress bar for the current directory
        pbar = tqdm(total=total_files_in_directory, position=0, leave=True, dynamic_ncols=True, unit='images')

        for file in files:
        
            pbar.update(1)  # Update the progress bar for each processed image
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.abspath(os.path.join(subdir, file))
                sanitized_filename = sanitize_filename(file)

                try:
                    img = Image.open(full_path)
                    img.close()
                except (PermissionError, OSError, Exception) as e:
                    error_message = f"Error while processing {full_path}: {str(e)}"
                    print(error_message)
                    log_error(error_log_number, error_message)
                    temp_path = get_cache_filename(sanitized_filename)
                    try:
                        shutil.copyfile(full_path, temp_path)
                        full_path = temp_path
                    except Exception as e:
                        error_message = f"Error while copying {full_path} to cache: {str(e)}"
                        print(error_message)
                        log_error(error_log_number, error_message)
                        continue

                try:
                    if not is_complex_image(full_path):
                        continue

                    detections = nude_detector.detect(full_path)
                except Exception as e:
                    cache_error_message = f"Error while detecting nudity in {full_path}: {str(e)}"
                    log_error(error_log_number, cache_error_message)
                    temp_path = get_cache_filename(sanitized_filename)
                    try:
                        shutil.copyfile(full_path, temp_path)
                    except Exception as e:
                        error_message = f"Error while copying {full_path} to cache: {str(e)}"
                        print(error_message)
                        log_error(error_log_number, error_message)
                        continue

                    try:
                        if not is_complex_image(temp_path):
                            continue
                        detections = nude_detector.detect(temp_path)
                    except Exception as e:
                        cache_error_message = f"Error while re-detecting nudity in cached {full_path}: {str(e)}"
                        print(cache_error_message)
                        log_error(error_log_number, cache_error_message)
                        continue

                matched_classes = [
                    {'class': item['class'], 'score': item['score']}
                    for item in detections
                    if item['class'] in all_labels and item.get('score', 0) > default_detection_score
                ]

                detected = any(item['class'] in all_labels for item in matched_classes)



                if detected:
                    images_with_detections.append(full_path)
                    print(f"Scanning directory {directory} for nude images...")
                    print(f"Detected: {sanitized_filename}")

                    current_report_size = os.path.getsize(get_report_filename(report_number))
                    if current_report_size >= 200 * 1024:
                        report_number += 1
                        create_new_report(report_number)

                    update_report(get_report_filename(report_number), full_path, matched_classes)

                pbar.set_postfix(current_file=f'{sanitized_filename}')

                clean_cache_directory('cache', max_cache_size_bytes)

        pbar.close()  # Close the progress bar for the current directory

    return images_with_detections

def main():
    parser = argparse.ArgumentParser(description='Scan a directory for nude images and generate an HTML report.')
    parser.add_argument('directory', type=str, help='Directory to scan for images')
    # Add an argument for the detection score
    parser.add_argument('--minscore', type=float, default=0.6, help='Detection score threshold (between 0 and 1), use a decimal point, eg: 0.3, DEFAULT: 0.6')

    args = parser.parse_args()
    create_reports_directory()
    report_number = 1
    create_new_report(report_number)
    error_log_number = 1  # Initialize error log number
    
    
    default_detection_score = args.minscore

    print(f"Scanning directory {args.directory} for nude images...")


    images_with_detections = scan_directory(args.directory, report_number, error_log_number)

    if images_with_detections:
        print("NudeNet Detection Report(s) generated in 'reports' directory.")
    else:
        print("No images with detections found in the specified directory.")

if __name__ == "__main__":
    main()
    clean_cache_directory('cache', 1) #clean after yourself man..