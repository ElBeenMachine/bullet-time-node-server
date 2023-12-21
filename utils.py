# Import libraries
import base64
from datetime import datetime, timedelta

def captureImage(cam, x = 1920, y = 1920, time = datetime.now() + timedelta(0, 10)):
    wait_state = True
    while wait_state:
        if time <= datetime.now():
            wait_state = False
            
    # Capture a picture from the source and process it into a Base64 String
    try:
        camera_config = cam.create_preview_configuration(main={"size": (x, y)})
        cam.configure(camera_config)
        cam.start()
        print("🟢 | Capturing image")
        cam.capture_file("img.jpg")

        # Open the image and return the data as a base64 encoded string
        with open("img.jpg", "rb") as image_file:
            data = image_file.read()
            return data
    except Exception as e:
        print(f"🔴 | {e}")
    finally:
        cam.stop()


def captureFrame(cam, stream):
    # Configure video settings
    cam.configure(cam.create_video_configuration())
    cam.resolution = (1920, 1080)
    cam.start() 

    # Capture frame into stream
    cam.capture_file(stream, format='jpeg', use_video_port=True)

    # Load image from stream
    frameData = stream.read()

    return frameData
