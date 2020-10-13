from time import sleep
from picamera import PiCamera
import keyboard

camera = PiCamera()
camera.resolution = (1024,768)
camera.startpreview()
#camera warm up
sleep(2)

run = True
print("press q")

while run:
    if keyboard.is_pressed('q'):
        print("snip snap")
        camera.capture('alex.jpg')
        run = False
