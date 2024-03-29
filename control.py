import math
import time

class RoombaController:
    def __init__(self, roomba_adapter):
        self.roomba = roomba_adapter
        self.current_lane = 1 
        self.current_lin_cmd = 0.0
        self.current_rot_cmd = 0.0

        self.default_lin_speed = 0.5
        self.default_rot_speed = 50

    def move(self, lin_speed, rot_speed):
        self.roomba.move(lin_speed, math.radians(rot_speed))
    
    def turn_left(self, rot_angle_deg, keep_going=False):
        self.move(0, self.default_rot_speed)
        wait_time = rot_angle_deg / self.default_rot_speed
        if not keep_going:
            time.sleep(wait_time)
            self.stop()

    def turn_right(self, rot_angle_deg, keep_going=False):
        self.move(0, -self.default_rot_speed)
        wait_time = rot_angle_deg / self.default_rot_speed
        if not keep_going:    
            time.sleep(wait_time)
            self.stop()

    def stop(self):
        self.move(0, 0)

    def move_forward(self, distance, keep_going=False):
        self.move(self.default_lin_speed, 0)
        wait_time = distance / self.default_lin_speed
        if not keep_going:
            time.sleep(wait_time)
            self.stop()
    
    def move_backward(self, distance, keep_going=False):
        self.move(-self.default_lin_speed, 0)
        wait_time = distance / self.default_lin_speed
        if not keep_going:
            time.sleep(wait_time)
            self.stop()

    def speed_up_linear(self, delta_speed):
        self.default_lin_speed += delta_speed

    def speed_up_rot(self, delta_speed):
        self.default_rot_speed += delta_speed

    def turn_on_vacuum(self,):
        self.roomba.send_moters_cmd(True, True, True, True, True)

    def turn_off_vacuum(self):
        self.roomba.send_moters_cmd(False, False, False, False, False)

    def new_lane(self,):
        if self.current_lane == 1:
            self.next_lane_right()
        else:
            self.next_lane_left()
        self.current_lane *= -1

    def next_lane_right(self,):
        self.move_backward(0.1, keep_going=False)
        self.turn_right(90)
        self.move_forward(0.1, keep_going=False)
        self.turn_right(90)
        self.move_forward(0.1, keep_going=True)

    def next_lane_left(self,):
        self.move_backward(0.1, keep_going=False)
        self.turn_left(90)
        self.move_forward(0.1, keep_going=False)
        self.turn_left(90)
        self.move_forward(0.1, keep_going=True)

class RLController:
    def __init__(self, roomba_adapter):
        self.DEFAULT_SPEED = 0.2
        self.DEFAULT_ROT = math.radians(10)
        self.controller = roomba_adapter
        self.action_args = {
            0: (self.DEFAULT_SPEED, 0.0),
            1: (-self.DEFAULT_SPEED, 0.0),
            2: (0.0, self.DEFAULT_ROT),
            3: (0.0, -self.DEFAULT_ROT)
        }

    def preprocess(self, action):
        self.controller.move(*self.action_args[action])
