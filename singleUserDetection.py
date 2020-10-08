# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import picamera
import numpy as np
import RPi.GPIO as GPIO
import time

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.

# Pin defs
doorSignalPin = 18;# Broadcom pin

#Pin setup
GPIO.setMode(GPIO.BCM)
GPIO.setup(doorSignalPin, GPIO.out)
#initialize low
GPIO.output(doorSignalPin, GPIO.LOW)

#camera
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
alex_image = face_recognition.load_image_file("alex.jpg")
alex_face_encoding = face_recognition.face_encodings(alex_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []

while True:
    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces([alex_face_encoding], face_encoding)
        name = "<Unknown Person>"

        if match[0]:
            name = "Alex"
            lastDetectionTime = time.time()



        print("I see someone named {}!".format(name))

    # If a known face was seen in the last 10 UNITS then open the door
    timeToKeepSignalHigh = 10
    if (time.time() - lastDetectionTime) < timeToKeepSignalHigh and (time.time() > timeToKeepSignalHigh):
        print("Door Signal HIGH")
        GPIO.output(doorSignalPin, GPIO.HIGH)
    else:
        GPIO.output(doorSignalPin, GPIO.LOW)
        print("Door Signal LOW")

