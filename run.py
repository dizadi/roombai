import time
import math
import numpy as np
from pyroombaadapter import PyRoombaAdapter
from perception import SensorPreprocessor, DetectionPreprocessor
from audio import Voice
from control import RoombaController
from keyboard_listener import KeyboardListener
import cv2

print("Starting...")
PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AR0JVPTN-if00-port0"
adapter = PyRoombaAdapter(PORT)
print("Adapter created...")
adapter.change_mode_to_full()
print("Sensor preprocessor created...")
cap = cv2.VideoCapture(0)
voice = Voice()
print("Roomba Voice created...")
controller = RoombaController(adapter)
print("Controller created...")
keyboard_listener = KeyboardListener()

cmd_args = {
    'w': (controller.move_forward, (.1,True)),
    'd': (controller.turn_right, (15,True)),
    'x': (controller.move_backward, (.1,True)),
    's': (controller.stop, ()),
    'a': (controller.turn_left, (15,True)), 
    'v': (controller.turn_on_vacuum, ()),
    'b': (controller.turn_off_vacuum, ()),
    'l': (controller.new_lane, ()),
    'e': (controller.speed_up_linear, (0.1,)),
    'q': (controller.speed_up_linear, (-0.1,)),
    'c': (controller.speed_up_rot, (5, )),
    'z': (controller.speed_up_rot, (-5, )),
    }
print(cmd_args.keys())
while True:
    #time.sleep(0.1)

    img, img_0 = cap.read()
    cv2.imshow('Video Feed',img_0)
    cv2.waitKey(1)
    current_cmd = None
    sensor_state = int.from_bytes(adapter.request_data(), 'little')
    if sensor_state > 0:
        print(f"Sensor {sensor_state} triggered!")
        print("Turning around ...")
        controller.new_lane()
    else:
        if len(keyboard_listener.command_buffer):
            current_cmd = keyboard_listener.command_buffer.pop(0)
    if current_cmd is not None:
        if current_cmd in cmd_args.keys():
            cmd_args[current_cmd][0](*cmd_args[current_cmd][1])
        else:
            print(f'{current_cmd} not found!')
            print(type(current_cmd))
