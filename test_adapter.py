
from time import sleep
import math
import keyboard
from pyroombaadapter import PyRoombaAdapter



PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AR0JVPTN-if00-port0"
adapter = PyRoombaAdapter(PORT)


adapter.request_data([1])
adapter.move(0.2, math.radians(0.0))  # go straight
sleep(1.0)
adapter.move(0, math.radians(-20))  # turn right
sleep(6.0)
adapter.move(0.2, math.radians(0.0))  # go straight
sleep(1.0)
adapter.move(0, math.radians(20))  # turn left
sleep(6.0)
