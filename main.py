# Import libraries
from utils import *
import subprocess
import os

VERSION = "1.9.9"

# Create a new Socket.IO server with specified port
sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

# Define a connection event
@sio.event
async def connect(sid, environ):
    print(f"🟢 | Client {environ['REMOTE_ADDR']} connected")

# Define a node data event
@sio.event
async def GET_NODE_DATA(sid):
    await sio.emit("NODE_DATA", { "node": platform.node(), "version": VERSION })

# Function to capture
async def capture(data):
    # Get current time
    current_time = datetime.now()

    # Configure capture settings
    cam = setCaptureSpec(data)
    

    # Determine Capture Time
    if data["time"] is None:
        capture_time = current_time
    else:
        capture_time = datetime.strptime(data["time"], "%a, %d %b %Y %H:%M:%S %Z")

    print(f"🟠 | Capturing image at {capture_time}")
    
    # Calculate sleep time
    sleep_time = (capture_time - current_time).total_seconds()
    
    # Sleep until it's time to capture
    await asyncio.sleep(max(0, sleep_time))
            
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
        print(f"🟠 | Camera instance closed")

# Define a image capture event
@sio.event
async def CAPTURE_IMAGE(sid, data):
    asyncio.create_task(capture(data))

# Stream event
@sio.event
async def START_STREAM(sid, data):
    # Get current time
    current_time = datetime.now()

    # Determine length of video stream
    if data["time"] is None:
        end_time = current_time
    else:
        end_time = datetime.strptime(data["time"], "%a, %d %b %Y %H:%M:%S %Z")
    
    print(f"🟠 | Starting video stream to end at {end_time}")

    # Configure video settings
    cam = setCaptureSpec(data)
    cam.start()

    try:
        while datetime.now() < end_time:
            # Capture frame into stream
            cam.capture_file("live_frame.jpg")

            # Open the image and return the data as a base64 encoded string
            with open("live_frame.jpg", "rb") as image_file:
                frame_data = image_file.read()
                # Send the frame over socket
                await sio.emit("VIDEO_FRAME", {"frame_data": frame_data})

            # Rate Limit
            await asyncio.sleep(1)

    except Exception as e:
        print(e)
        
    finally:
        cam.stop()
        print(f"🟠 | Camera instance closed")

@sio.event
def UPDATE(sid):
    try:
        # Run the update script in the background
        os.system("cd ~/btns && nohup ./update.sh &> /dev/null &")
        print("🟢 | Update script started in the background.")
        
        # Exit the current process
        os._exit(0)
    except Exception as e:
        print(f"🔴 | Failed to start update script: {e}")

# Define an error event
@sio.event
def event_error(sid, error):
    print(f"Error from {sid}: {error}")

# Set the port for the Socket.IO server
if __name__ == '__main__':
    port = 8080
    web.run_app(app, port=port)
