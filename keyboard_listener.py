from pynput import keyboard 
from threading import Thread


class KeyboardListener:
    def __init__(self, ):
        self.command_buffer = []
        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()

    def on_press(self, key):
        if isinstance(keyboard.KeyCode):
            self.command_buffer.append(key.char)

    def run(self,):
        # Collect events until released
        with keyboard.Listener(
            on_press=self.on_press) as listener:
            try:
                listener.join()
            except:
                print("Failed to get keypress")

if __name__ == "__main__":
    while True:
        listener = KeyboardListener()
        print(listener.command_buffer)