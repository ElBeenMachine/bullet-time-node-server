# Import libraries
import socketio
import platform
from aiohttp import web
from utils import *
import os
import subprocess

VERSION = "1.6.1"

# Create a new Socket.IO server with specified port
sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

# Define a connection event
@sio.event
async def connect(sid, environ):
    print(f"🟢 | Client {environ['REMOTE_ADDR']} connected")
    await sio.emit("NODE_DATA", { "node": platform.node(), "version": VERSION })

# Define a message event
@sio.event
async def CAPTURE_IMAGE(sid, data):
    x = data["resolution"]["x"]
    y = data["resolution"]["y"]
    capture_time = datetime.strptime(data["time"], "%a, %d %b %Y %H:%M:%S %Z")
    response = captureImage(x, y, time=capture_time)
    await sio.emit("IMAGE_DATA", {"image_data": response, "node_name": platform.node()})

# Define an error event
@sio.event
def event_error(sid, error):
    print(f"Error from {sid}: {error}")

# Set the port for the Socket.IO server
if __name__ == '__main__':
    port = 8080
    web.run_app(app, port=port)