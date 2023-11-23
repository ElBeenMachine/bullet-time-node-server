# Import libraries
import base64

# Set up the camera
from picamera2 import Picamera2
cam = Picamera2()
camera_config = cam.create_preview_configuration(main={"size": (1920, 1080)})
cam.configure(camera_config)
cam.start()

def captureImage():
    # Capture a picture from the source and process it into a Base64 String
    try:
        print("🟢 | Capturing image")
        cam.capture_file("img.jpg")

        # Open the image and return the data as a base64 encoded string
        with open("img.jpg", "rb") as image_file:
            data = base64.b64encode(image_file.read())
            return data
    except Exception as e:
        print(f"🔴 | {e}")