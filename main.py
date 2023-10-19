from flask import Flask, json
import base64
import platform

# Import the new camera class
from picamera2 import Picamera2

# Class to initialise the camera
class Camera:
    def __init__(self):         
        #set up camera
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_preview_configuration(main={"size": (4608, 2592)})
        self.picam2.configure(camera_config)
        self.picam2.start()

    def takeImage(self,path):
        self.picam2.capture_file(path)

app = Flask(__name__)


def checkCamera(source):
    cap = cv.VideoCapture(source)
    if cap is None or not cap.isOpened():
        raise Exception("Camera Not Active")


@app.route("/capture")
def hello():
    # Capture a picture from the source and process it into a Base64 String
    try:
        cam = Camera()
        
        cam.takeImage("img.jpg")
        with open('img.jpg', 'rb') as image_file:
            data = base64.b64encode(image_file.read())
    except Exception as e:
        print(e)
        return "An unexpected error has occurred while processing the image", 500

    # Return the result in a JSON format with the device node name attached to the resposne
    return json.dumps({"node": platform.node(), "data": data.decode("utf-8")}), 200


# Start the web server
if __name__ == "__main__":
    print("Waiting for capture request:")
    app.run(host="0.0.0.0", port=8080)
