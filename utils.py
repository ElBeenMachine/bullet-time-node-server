# Set default values
x = 1920
y = 1080
iso = 100
shutterSpeed = 1000 

def setCaptureSpec(cam,data):

    # Set resolution if specified
    if 'resolution' in data:
        resolution = data["resolution"]
        if 'x' in resolution and 'y' in resolution:
            x = resolution["x"]
            y = resolution["y"]

    # Set iso if specified
    if 'iso' in data:
        if data["iso"]:
            iso = data["iso"]
        
    # Set shutter speed if specified
    if 'shutter_speed' in data:
        if data["shutter_speed"]:
            shutterSpeed = data["shutter_speed"]

    # Apply settings
    camera_config = cam.create_still_configuration(main={"size": (x, y)})
    cam.set_controls({"ExposureTime": shutterSpeed, "AnalogueGain": round(iso / 100,1)})

    cam.configure(camera_config)
    return cam