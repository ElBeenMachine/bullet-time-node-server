from flask import Flask, json
import base64
import platform

# Set up the camera
from picamera2 import Picamera2

cam = Picamera2()
camera_config = cam.create_preview_configuration(main={"size": (1920, 1080)})
cam.configure(camera_config)
cam.start()

app = Flask(__name__)


# Capture route to capture input from the camera
@app.route("/capture")
def capture():
    # Capture a picture from the source and process it into a Base64 String
    try:
        cam.capture_file("img.jpg")

        with open("img.jpg", "rb") as image_file:
            data = base64.b64encode(image_file.read())
    except Exception as e:
        print(e)
        return "An unexpected error has occurred while processing the image", 500

    # Return the result in a JSON format with the device node name attached to the resposne
    return json.dumps({"node": platform.node(), "data": data.decode("utf-8")}), 200


# Ping route to check if node is active
@app.route("/ping")
def ping():
    # Return a pong
    return json.dumps({"response": "Pong!"}), 200


# Start the web server
if __name__ == "__main__":
    print("Waiting for capture request:")
    app.run(host="0.0.0.0", port=8080)
