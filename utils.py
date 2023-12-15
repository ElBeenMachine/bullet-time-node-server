# Import libraries
import base64
from datetime import datetime, timedelta

# Set up the camera
from picamera2 import Picamera2
cam = Picamera2()
cam.set_controls({"ExposureTime": 5000, "AnalogueGain": 1.0})

def captureImage(x = 1920, y = 1920, time = datetime.now() + timedelta(0, 10)):
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
        cam.stop()

        # Open the image and return the data as a base64 encoded string
        with open("img.jpg", "rb") as image_file:
            data = image_file.read()
            return data
    except Exception as e:
        print(f"🔴 | {e}")