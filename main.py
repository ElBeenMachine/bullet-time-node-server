from flask import Flask, json
import cv2 as cv
import base64
import platform

app = Flask(__name__)


def checkCamera(source):
    cap = cv.VideoCapture(source)
    if cap is None or not cap.isOpened():
        raise Exception("Camera Not Active")


@app.route("/capture")
def hello():
    print("Capturing Image")

    # Check to see if the provided source is valid
    try:
        checkCamera(0)
    except:
        return "Unable to load a camera", 500

    # Capture a picture from the source and process it into a Base64 String
    try:
        # Get the first camera source on the node
        cam = cv.VideoCapture(0)

        # Set camera resolution to 1080p
        width = 1920
        height = 1080
        cam.set(cv.CAP_PROP_FRAME_WIDTH, width)
        cam.set(cv.CAP_PROP_FRAME_HEIGHT, height)

        # Capture image
        result, image = cam.read()
        res, frame = cv.imencode(".jpg", image)
        data = base64.b64encode(frame)
    except:
        return "An unexpected error has occurred while processing the image", 500

    # Return the result in a JSON format with the device node name attached to the resposne
    return json.dumps({"node": platform.node(), "data": data.decode("utf-8")}), 200


# Start the web server
if __name__ == "__main__":
    print("Waiting for capture request:")
    app.run(host="0.0.0.0", port=8080)
