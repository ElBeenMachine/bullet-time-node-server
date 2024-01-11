# Import libraries
import logging
logging.basicConfig(filename="./logs.log", filemode="w", format="[%(asctime)s] %(name)s → %(levelname)s: %(message)s", level=logging.DEBUG)

from utils import *

VERSION = "2.1.0"

# Create a new Socket.IO server with specified port
sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

# Define a connection event
@sio.event
async def connect(sid, environ):
    logging.info(f"🟢 | Client {environ['REMOTE_ADDR']} connected")

# Define a node data event
@sio.event
async def GET_NODE_DATA(sid):
    await sio.emit("NODE_DATA", { "node": platform.node(), "version": VERSION })

# Function to capture
async def capture(data):
    # Get current time
    current_time = datetime.now()

    # Determine Capture Time
    if data["time"] is None:
        capture_time = current_time
    else:
        capture_time = datetime.strptime(data["time"], "%a, %d %b %Y %H:%M:%S %Z")

    logging.info(f"🟠 | Capturing image at {capture_time}")
    
    # Calculate sleep time
    sleep_time = (capture_time - current_time).total_seconds()
    
    # Capture a picture from the source and process it into a Base64 String
    async with camera_lock:
        # Configure capture settings
        cam = getCaptureSpec(data,"STILL")
        try:
            # Sleep until it's time to capture
            await asyncio.sleep(max(0, sleep_time))
            
            cam.start()
            
            logging.info("🟢 | Capturing image")

            cam.capture_file("img.jpg")

            # Open the image and return the data as a base64 encoded string
            with open("img.jpg", "rb") as image_file:
                data = image_file.read()
                await sio.emit("IMAGE_DATA", {"image_data": data, "node_name": platform.node()})
        except Exception as e:
            logging.error(f"🔴 | {e}")
        finally:
            cam.stop()
            logging.info(f"🟠 | Camera instance closed")

# Define a image capture event
@sio.event
async def CAPTURE_IMAGE(sid, data):
    asyncio.create_task(capture(data))

async def capture_stream(cam, data, end_time):
    try:
        while datetime.now() < end_time:
            # Capture frame into stream
            cam.start()
            cam.capture_file("live_frame.jpg")

            # Open the image and return the data as a base64 encoded string
            with open("live_frame.jpg", "rb") as image_file:
                frame_data = image_file.read()
                # Send the frame over socket
                await sio.emit("VIDEO_FRAME", {"frame_data": frame_data})

            # Rate Limit
            await asyncio.sleep(0.0167)

    except Exception as e:
        logging.error(f"🔴 | {e}")
        
    finally:
        cam.stop()
        logging.info(f"🟠 | Camera instance closed")  

# Define stream event
@sio.event
async def START_STREAM(sid, data):
    # Get current time
    current_time = datetime.now()

    # Determine length of video stream
    if data["time"] is None:
        end_time = current_time
    else:
        end_time = datetime.strptime(data["time"], "%a, %d %b %Y %H:%M:%S %Z")

    logging.info(f"🟠 | Starting video stream to end at {end_time}")

    async with camera_lock:
        # Configure video settings
        cam = getCaptureSpec(data,"STREAM")
    
        task = asyncio.create_task(capture_stream(cam, data, end_time))
        
        # Stop Stream Route
        @sio.event
        async def STOP_STREAM(sid):
            cam.stop()
            logging.info(f"🟠 | Stopping video stream")
            task.cancel()

        # Disconnect Event Route
        @sio.event
        async def disconnect(sid):
            cam.stop()
            logging.error("🔴 | Client connection severed, stopping video stream")
            task.cancel()

@sio.event
async def GET_LOGS(sid):
    with open('./logs.log', 'r') as file:
        log_content = file.read()
    await sio.emit('LOGS', {'logs': log_content, "node": platform.node() })

# Define an error event
@sio.event
def event_error(sid, error):
    logging.error(f"🔴 | {error}")

# Set the port for the Socket.IO server
if __name__ == '__main__':
    port = 8080
    web.run_app(app, port=port)

