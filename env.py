
import numpy as np

import abc
import dataclasses

@dataclasses.dataclass
class State:
    visual_data: np.array
    sensor_data: np.array


class Env(abc.ABC):
    @abc.abstractmethod
    def step(self, action):
        pass

class RoombaEnv:
    def __init__(self, sensor_preprocessor, visual_preprocessor, api_wrapper):
        self._api_wrapper = api_wrapper
        self._sensor_preprocessor = sensor_preprocessor
        self._visual_preprocessor = visual_preprocessor

    def step(self, action):
        self._api_wrapper.act(action=action)
        sensor_data = self._sensor_preprocessor.preprocess()
        visual_data = self._visual_preprocessor.preprocess()
        state = State(
            visual_data=visual_data,
            sensor_data=sensor_data,
        )
        return state

