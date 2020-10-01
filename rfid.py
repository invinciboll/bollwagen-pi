import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class Reader:
    def __init__(self):
        self.reader = SimpleMFRC522()
    

    def getId(self):
        while True:
            try:
                id = self.reader.read_id()
                GPIO.cleanup()
                return str(id)
            finally:
                GPIO.cleanup()
                pass

if False:
    r = Reader()
    print(r.getId())