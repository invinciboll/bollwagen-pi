from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class Reader:
    def __init__(self):
        self.reader = SimpleMFRC522()
        pass

    def getId(self):
        while True:
            try:
                id = self.reader.read_id()
                return str(id)
                pass
            finally:
                pass
