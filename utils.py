import time
import socketio
import platform
from aiohttp import web
import asyncio
from datetime import datetime
from picamera2 import Picamera2
import cv2
import numpy as np

# Initialise camera instance
cam = Picamera2()

def setCaptureSpec(data):
    # Set default values
    x = 1920
    y = 1080
    iso = 100
    shutterSpeed = 1000 
    
    # Store camera settings if specified 
    if 'resolution' in data:
        resolution = data["resolution"]
        if resolution['x'] is not None and resolution['y'] is not None:
            x = resolution["x"]
            y = resolution["y"]

    if 'iso' in data:
        if data["iso"] is not None:
            iso = data["iso"]
            
    if 'shutter_speed' in data:
        if data["shutter_speed"] is not None:
            shutterSpeed = data["shutter_speed"]

    # Determine capture mode
    camera_config = cam.create_preview_configuration(main={"size": (x, y)})
    print(f"🟠 | Camera configured for capture") 

    # Apply settings
    cam.set_controls({"ExposureTime": shutterSpeed})
    # cam.set_controls({"ExposureTime": shutterSpeed, "AnalogueGain": round(iso / 100,1)})
    cam.configure(camera_config)
    print(f"🟠 | Resolution set to {x}x{y} | Iso set to {iso} | Shutter speed set to {shutterSpeed} ")  

    return cam

def remove_green(image_path):

    input_image = cv2.imread(image_path) 

    if input_image is None:
        print("Error reading image for green removal")

    # Define upper and lower bounds of green in HSV 
    # For openCV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]. 
    lower_green = np.array([35,100,100])
    upper_green = np.array([85,255,255])

    # Convert blue green red image to hue saturation value
    inputImage_HSV = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV) 

    # Creates binary mask, green pixels turned to white(255), subject pixels = black (0)
    mask = cv2.inRange(inputImage_HSV, lower_green, upper_green) 

    # Uses numPy conditional indexing on inputImage, to select all indeces from the mask that are > 0 and turn black
    input_image[mask > 0] = [0,0,0] 
    cv2.imwrite("img.jpg", input_image) 
    