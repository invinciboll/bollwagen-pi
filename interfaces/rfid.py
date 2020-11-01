from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class Reader:
    def __init__(self):
        self.reader = SimpleMFRC522()

    def getId(self):
        id = self.reader.read_id_no_block()
        return str(id)
