import time
import math
import numpy as np
from pyroombaadapter import PyRoombaAdapter
from perception import SensorPreprocessor
from audio import Voice
from control import RoombaController
from roombai.roombai.keyboard_listener import KeyboardListener
from keyboard_listener import KeyboardListener

print("Starting...")
PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AR0JVPTN-if00-port0"
adapter = PyRoombaAdapter(PORT)
print("Adapter created...")
adapter.change_mode_to_full()
sensor_preprocessor = SensorPreprocessor(adapter, 1, 5)
print("Sensor preprocessor created...")
voice = Voice()
print("Roomba Voice created...")
controller = RoombaController(adapter)
print("Controller created...")
keyboard_listener = KeyboardListener()

cmd_args = {
    'w': (controller.move_forward, (1,)),
    'd': (controller.turn_left, (1, )),
    'x': (controller.move_backward, (1,)),
    's': (controller.stop, ()),
    'a': (controller.turn_right, (1,)), 
    'v': (controller.turn_on_vacuum, ()),
    'b': (controller.turn_off_vacuum, ()),
}

while True:
    time.sleep(0.3)
    current_cmd = None
    sensor_state = int.from_bytes(adapter.request_data(), 'little')
    if sensor_state > 0:
        print(f"Sensor {sensor_state} triggered!")
        print("Turning around ...")
        current_cmd = 's'
    else:
        if len(keyboard_listener.command_buffer):
            current_cmd = keyboard_listener.command_buffer.pop(0)
    cmd_args[current_cmd][0](*cmd_args[current_cmd][1])
            
        