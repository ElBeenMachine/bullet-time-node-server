# Import libraries
import socketio
import platform
from aiohttp import web
from utils import *
import asyncio
import io
import base64

VERSION = "1.7.1"

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
    await sio.emit("NODE_DATA", { "node": platform.node(), "version": VERSION })

# Define a message event
@sio.event
async def CAPTURE_IMAGE(sid, data):
    x = data["resolution"]["x"]
    y = data["resolution"]["y"]
    capture_time = datetime.strptime(data["time"], "%a, %d %b %Y %H:%M:%S %Z")
    response = captureImage(cam, x, y, time=capture_time)
    await sio.emit("IMAGE_DATA", {"image_data": response, "node_name": platform.node()})

# Stream event
@sio.event
async def START_STREAM(sid):
    # Initialise stream to store encoded frames, will ensure stream is instantiated before continuing
    with io.BytesIO() as stream:
        while True:
            try:
                # Rewind the stream for reading and encode to base64
                stream.seek(0)
                frameData = base64.b64encode(captureFrame(stream))

                # Send the frame over socket
                await sio.emit("VIDEO_FRAME", {"frame_data": frameData})
                await asyncio.sleep(0.1) # Rate limiting 
                
                # Reset the stream for the next frame
                stream.seek(0)
                stream.truncate()

            except Exception as e:
                print(f"Streaming error or user disconnected:{e}")
                break

            finally:
                cam.close()

@sio.event
async def LIVE_STREAM(sid):
    with cam as camera:
        camera.resolution(640, 480)
        camera.framerate = 24
        stream = io.BytesIO()

        for _ in camera.capture_continuous(stream, format="jpeg", use_video_port=True):
            stream.seek(0)
            sio.emit("VIDEO_STREAM", {"data": stream.read()})
            stream.seek(0)
            stream.truncate()

# Define an error event
@sio.event
def event_error(sid, error):
    print(f"Error from {sid}: {error}")

# Set the port for the Socket.IO server
if __name__ == '__main__':
    port = 8080
    web.run_app(app, port=port)