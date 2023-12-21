# Import libraries
import socketio
import platform
from aiohttp import web
from utils import *
import asyncio
from datetime import datetime, timedelta

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
async def GET_NODE_DATA(sid, environ):
    await sio.emit("NODE_DATA", { "node": platform.node(), "version": VERSION })

# Define a image capture event
@sio.event
async def CAPTURE_IMAGE(sid, data):
    x = data["resolution"]["x"]
    y = data["resolution"]["y"]
    capture_time = datetime.strptime(data["time"], "%a, %d %b %Y %H:%M:%S %Z")
    response = captureImage(x, y, time=capture_time)
    await sio.emit("IMAGE_DATA", {"image_data": response, "node_name": platform.node()})


# Stream event
@sio.event
async def START_STREAM(sid):
    end_time = datetime.now() + timedelta(0, 9)
    while end_time >= datetime.now():
        try:
            # Send the frame over socket
            await sio.emit("VIDEO_FRAME", {"frame_data": captureFrame(cam=cam)})
            await asyncio.sleep(1) # Rate limiting

        except Exception as e:
            print(f"Streaming error or user disconnected:{e}")
            break

# Define an error event
@sio.event
def event_error(sid, error):
    print(f"Error from {sid}: {error}")

# Set the port for the Socket.IO server
if __name__ == '__main__':
    port = 8080
    web.run_app(app, port=port)