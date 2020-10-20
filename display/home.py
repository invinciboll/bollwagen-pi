from .display import Display
from guizero import Text, Box
import Adafruit_DHT
import time
import threading


class Home_Display(Display):
    def __init__(self, app, path, image, gpio):
        self.DHT_SENSOR = Adafruit_DHT.DHT11
        self.DHT_PIN = gpio
        self.leave = False
        super().__init__(app, path, image, use_cancle_button=True, use_confirm_button=False)

    def generateComponents(self):
        self.clock = Text(self.window,
                          align="top", size=self.CONST_FONT_SIZE_GENERAL*4)
        self.clock.text_color = "white"

        self.temp = Text(self.window,
                         align="top", size=self.CONST_FONT_SIZE_GENERAL*1)
        self.temp.text_color = "white"

        self.hum = Text(self.window,
                        align="top", size=self.CONST_FONT_SIZE_GENERAL*1)
        self.hum.text_color = "white"

    def open(self):
        self.window.show()
        tr = threading.Thread(target=self.action)
        tr.start()

    def action(self):
        while not self.leave:
            t = time.localtime()
            self.clock.value = time.strftime("%H:%M", t)

            humidity, temperature = Adafruit_DHT.read(
                self.DHT_SENSOR, self.DHT_PIN)
            if temperature is not None:
                self.temp.value = "{0:0.1f}C".format(
                    temperature)
            if humidity is not None:
                self.hum.value = "{0:0.1f}%".format(
                    humidity)
            self.window.update()

            index = 0
            while (not self.leave) and (index < 300):
                time.sleep(0.1)
                print(f"sleepy {index}")
                index += 1
        print("Thread killed")
        self.leave = False

    def cancle(self):
        self.leave = True
        self.close()

    def confirm(self):
        pass
