from pyroombaadapter import PyRoombaAdapter

port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AR0JVPTN-if00-port0"

roomba = PyRoombaAdapter(port)

import time

while True:
    roomba.change_mode_to_full()
    data = roomba.request_data()
    print(int.from_bytes(data, 'little'))
    #time.sleep(1)
