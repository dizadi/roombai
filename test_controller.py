
from control import Controller, RLController
from pyroombaadapter import PyRoombaAdapter


port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AR0JVPTN-if00-port0"
adapter = PyRoombaAdapter(port)
rl_controller = RLController(adapter)
for i in range(len(list(rl_controller.action_args.keys()))):
    rl_controller.act(i)
