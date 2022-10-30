from re import L
import time
import math
import numpy as np
from pyroombaadapter import PyRoombaAdapter
from perception import SensorPreprocessor
from audio import Voice
from control import RoombaController


class RoombaRunner:
    def __init__(
        self,
        sensor_preprocessor,
        controller,
    ):
        self._adapter = adapter
        self._controller = controller
    
    def step(self, ):

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

cmd_args = {
    'fwd': (0.2, math.radians(0)),
    'right': (-0.2, math.radians(-20)),
    'left': (-0.2, math.radians(20)),
    'stop': (0, 0)
}

while True:
    time.sleep(0.3)
    sensor_state = int.from_bytes(adapter.request_data(), 'little')
    if sensor_state > 0:
        print(f"Sensor {sensor_state} triggered!")
        print("Turning around ...")
        controller.move_backward(0.4, keep_going=False)
        voice.sound_off()
        controller.turn_right(90)
        controller.move_forward(0.2, keep_going=False)
        controller.turn_right(90)
        
    else:
        controller.move_forward(0.2, keep_going=True)
