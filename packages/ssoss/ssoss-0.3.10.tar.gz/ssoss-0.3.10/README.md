# Safe Sightings of Signs and Signals (SSOSS or SOS)

SOS is an automated tool to check visibility to traffic signals and signs based on predefined sight distances. This tool provides
a repeatable way to monitor and verify traffic signals and signs are visible along any roadway that GPS data and video are recorded on.

This project is a collection of Python classes, methods, and notebooks that are simple and free to use.

## Features
Video Syncronization Helper Tools: Python functions are provided to export the video frames and help to synchronize the video file.
Automated data processing: The SOS program uses a combination of GPS and video data to extract images of traffic signals and/or roadway signs.
Image Labeling and animated GIF image tools: Python functions are included to label images or create an animated GIF from multiple images 
## Requirements
Python 3.9
Required libraries: pandas, numpy, opencv-python, geopy, gpxpy, imageio, tqdm, lxml 
## Installation
To install the SOS program, follow these steps:

    pip install SSOSS

Clone or download the repository to your local machine.
Install the required libraries using pip: pip install pandas numpy opencv-python
Run the program by executing the main.py script.
## Usage
To use the SOS program, follow these steps:

### A. Input Files
Data related to the static road objects (signs and intersections) need to be saved in a CSV file for used in processing.
The intersection CSV file has the following format

ID, Streetname 1, Streetname 2, Latitude, Longitude, Posted Speed (MPH) of NB Approach, Posted Speed (MPH) of EB Approach, 
Posted Speed (MPH) of SB Approach, Posted Speed (MPH) of WB Approach, NB Approach Compass Heading, EB Approach Compass Heading,
SB Approach Compass Heading, WB Approach Compass Heading



### B. Data Collection
Collect data simultaneously:
1. GPX recording
   a. Use GPX Version 1.0 with logging every second
2. Video Recording
   a. Record at 5 Megapixel resolution or more
   b. Record at 30 frames per second or higher

### C. Data Processing

This script captures video footage of the signs and signals, along with GPS data.
Process the data using the data_processing.py script. This script analyzes the data and generates a report or map showing any issues with the visibility of the signs and signals.
Use the report or map to identify and address any issues with the visibility of the signs and signals.
## Documentation

### Jupter Notebook Examples
### Helper Functions
    extract images for sync
    Gif creator
### Heuristic
Inputs include:
 the center point of the intersection, but this could be changed to the stop bar line
the approach speeds to the intersection
the compass bearing of the approach to the intersection

I use a heuristic from the GPX points that goes something like this:

For Each GPX Point:
What are the closest & approaching intersections
Based on compass heading of car and input data, which approach leg is vehicle on
What is the approach speed of that approach leg, and look up sight distance for that speed
Is the current GPX point greater than that sight distance and the next point is less than the sight distance,
If yes, then calculate acceleration between those two points and estimate the time the vehicle traveled over the sight distance.
if no, go to next GPX point

From the sight distance timestamp, the video needs to be synced to a time, and the frame is extracted that is closest to that time.


## Contributions
We welcome contributions to the SOS project! If you have an idea for a new feature or have found a bug, please open an issue or submit a pull request.

## License
The SOS project is licensed under the MIT License. See LICENSE for more information.