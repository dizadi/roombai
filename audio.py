import playsound
import numpy as np
import os

class Voice:
    def __init__(self, sounds_dir = "/home/pi/roombai/sounds/"):
        self.sounds_dir = sounds_dir
        sound_files = os.listdir(self.sounds_dir)
        self.fuck_file = "/home/pi/roombai/test_sound.m4a"
        self.files = [self.fuck_file, "/home/pi/roombai/mfer.m4a", "/home/pi/roombai/dammit.m4a"]

    def fuck(self, ):
        playsound.playsound(self.fuck_file)

    def sound_off(self, ):
        f = self.files[np.random.randint(len(self.files))]
        playsound.playsound(f)
