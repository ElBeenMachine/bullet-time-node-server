import time
import socketio
import platform
from aiohttp import web
import asyncio
from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from picamera2.outputs import CircularOutput
import subprocess
import os

import logging


# Initialise camera instance
cam = Picamera2() 

# Camera lock to ensure its only used by one route at a time
camera_lock = asyncio.Lock()

def getCaptureSpec(data,capture_mode):
    
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
            
    
    logging.info(f"🟠 | Resolution set to {x}x{y} | Iso set to {iso} | Shutter speed set to {shutterSpeed}") 
   
    cam.configure(camera_config) 
    cam.set_controls({"ExposureTime": shutterSpeed})
    
    return cam

