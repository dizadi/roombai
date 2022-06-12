
from pyroombaadapter import PyRoombaAdapter
from perception import SensorPreprocessor, VideoStream, FramePreprocessor
from control import RLController
import time
from train import train_step
from agent import DQNAgent

def main():
    port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AR0JVPTN-if00-port0"
    n_steps = 4
    fps = 5
    frame_size = (128,128)
    adapter = PyRoombaAdapter(port)
    sensor_preprocessor = SensorPreprocessor(roomba_adapter=adapter, n_steps = n_steps, fps = fps)
    video_stream = VideoStream(0, fps = fps)
    frame_preprocessor = FramePreprocessor(video_stream=video_stream, n_frames = n_steps, fps = fps, size=frame_size)
    actor = DQNAgent(state_size = (n_steps, frame_size[0], frame_size[1]))
    controller = RLController(roomba_adapter=adapter)

    while True:
        visual_state = frame_preprocessor.preprocess()
        sensor_state = sensor_preprocessor.preprocess()
        action = actor.act(visual_state)
        controller.act(action)
        time.wait(fps * n_steps)

        next_visual_state = frame_preprocessor.preprocess()
        next_sensor_state = sensor_preprocessor.preprocess()
        
        reward = - sum(next_sensor_state)
        actor.learn(action, visual_state, next_visual_state, reward)

        sensor_state = next_sensor_state
        visual_state = next_visual_state
