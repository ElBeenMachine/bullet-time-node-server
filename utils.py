import time
import socketio
import platform
from aiohttp import web
import asyncio
from datetime import datetime
from picamera2 import Picamera2

# Initialise camera instance
cam = Picamera2()

def setCaptureSpec(data,capture_mode):
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
    cam.set_controls({"ExposureTime": shutterSpeed, "AnalogueGain": round(iso / 100,1)})
    cam.configure(camera_config)
    print(f"🟠 | Resolution set to {x}x{y} | Iso set to {iso} | Shutter speed set to {shutterSpeed} ")  

    return cam