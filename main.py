# Import libraries
import time
import socketio
import platform
from aiohttp import web
import asyncio
from datetime import datetime

VERSION = "1.7.3"

# Create a new Socket.IO server with specified port
sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

# Set up the camera
from picamera2 import Picamera2
cam = Picamera2()
cam.set_controls({"ExposureTime": 1000, "AnalogueGain": 1.0})

# Define a connection event
@sio.event
async def connect(sid, environ):
    print(f"🟢 | Client {environ['REMOTE_ADDR']} connected")

# Define a node data event
@sio.event
async def GET_NODE_DATA(sid):
    await sio.emit("NODE_DATA", { "node": platform.node(), "version": VERSION })

# Define a image capture event
@sio.event
async def CAPTURE_IMAGE(sid, data):
    x = data["resolution"]["x"]
    y = data["resolution"]["y"]
    capture_time = datetime.strptime(data["time"], "%a, %d %b %Y %H:%M:%S %Z")

    print(f"🟠 | Capturing image at {capture_time}")
    
    camera_config = cam.create_preview_configuration(main={"size": (x, y)})
    cam.configure(camera_config)
    
    # Do nothing until time has passed
    while datetime.now() < capture_time:
        print("Not Time")
            
    # Capture a picture from the source and process it into a Base64 String
    try:
        cam.start()
        print("🟢 | Capturing image")
        cam.capture_file("img.jpg")

        # Open the image and return the data as a base64 encoded string
        with open("img.jpg", "rb") as image_file:
            data = image_file.read()
            await sio.emit("IMAGE_DATA", {"image_data": data, "node_name": platform.node()})
    except Exception as e:
        print(f"🔴 | {e}")
    finally:
        cam.stop()

# Stream event
@sio.event
async def START_STREAM(sid, data):
    x = data["resolution"]["x"]
    y = data["resolution"]["y"]
    end_time = datetime.strptime(data["time"], "%a, %d %b %Y %H:%M:%S %Z")

    print(f"🟠 | Starting video stream to end at {end_time}")
    
    # Configure camera
    camera_config = cam.create_preview_configuration(main={"size": (x, y)})
    cam.configure(camera_config)
    
    # Configure video settings
    cam.start() 
    
    while datetime.now() < end_time:
        try:
            # Capture frame into stream
            cam.capture_file("live_frame.jpg")

            # Open the image and return the data as a base64 encoded string
            with open("live_frame.jpg", "rb") as image_file:
                data = image_file.read()
                # Send the frame over socket
                await sio.emit("VIDEO_FRAME", {"frame_data": data})
            
            # Wait half a second
            await asyncio.sleep(0.5)

        except Exception as e:
            print(e)
            break
        
        finally:
            cam.stop()

# Define an error event
@sio.event
def event_error(sid, error):
    print(f"Error from {sid}: {error}")

# Set the port for the Socket.IO server
if __name__ == '__main__':
    port = 8080
    web.run_app(app, port=port)
