import time
import socketio
import platform
from aiohttp import web
import asyncio
from datetime import datetime, timezone
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from picamera2.outputs import CircularOutput
import subprocess
import os

os.environ['LIBCAMERA_LOG_LEVELS'] = '4'

# Initialise camera instance
cam = Picamera2() 
cam.start()

def getCaptureSpec(data,capture_mode):
    # Stop camera ready for configuration
    cam.stop()

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

    # Default capture setting
    camera_config = cam.create_preview_configuration(main={"size": (x,y)})
                                                     
    # Apply settings
    if capture_mode == "STREAM":     
        camera_config = cam.create_video_configuration(main={"size": (x, y)}) 
        cam.options['quality'] = 30
               
    cam.configure(camera_config) 
    cam.set_controls({"ExposureTime": shutterSpeed, "AnalogueGain": iso / 100})
    
    cam.start()
    return cam

