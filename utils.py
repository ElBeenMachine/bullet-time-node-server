# Import libraries
import base64

# Set up the camera
from picamera2 import Picamera2
cam = Picamera2()

def captureImage(x, y):
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