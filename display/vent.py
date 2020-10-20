from .display import Display
from guizero import Slider
from gpiozero import PWMLED


class Vent(Display):
    def __init__(self, app, path, image, gpio):
        self.fan = PWMLED(gpio)
        self. speed = 0
        super().__init__(app, path, image, use_cancle_button=True, use_confirm_button=False)
        
    def generateComponents(self):
        Slider(self.window, start=0, command=self.__slider_changed,
                                 end=100, width="fill", height=60).text_color = "white"


    def confirm(self):
        pass

    def cancle(self):
        self.close()

    def __slider_changed(self, n):
        x = int(n)
        if x == 0:
            self.speed = 0
        else:
            self.speed = 0.2 + (x/100)*0.8

        self.fan.value = self.speed
