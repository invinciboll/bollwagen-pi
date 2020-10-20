from .display import Display
from guizero import Slider, Drawing
from colormap import rgb2hex
from gpiozero import PWMLED


class LedControl(Display):
    def __init__(self, app, path, image, gpioR, gpioG, gpioB):
        self.red = 0
        self.green = 0
        self.blue = 0
        self.led_r = PWMLED(gpioR)
        self.led_g = PWMLED(gpioG)
        self.led_b = PWMLED(gpioB)
        super().__init__(app, path, image, use_cancle_button=True, use_confirm_button=False)
        
    def generateComponents(self):
        self.drawing = Drawing(self.window, width="fill")

        Slider(self.window, start=0, command=self.__sliderRedChanged,
                                 end=255, width="fill", height=60).text_color = "red"
        Slider(self.window, start=0, command=self.__sliderGreenChanged,
                                   end=255, width="fill", height=60).text_color = "green"
        Slider(self.window, start=0, command=self.__sliderBlueChanged,
                                  end=255, width="fill", height=60).text_color = "blue"

    def confirm(self):
        pass

    def cancle(self):
        self.close()

    def __processColor(self):
        self.drawing.rectangle(
            20, 0, 460, 60, color=rgb2hex(self.red, self.green, self.blue))
        if self.red == 0 and self.green == 0 and self.blue == 0:
            self.picture.image = f"{self.path}{self.image}_off.png"
        else:
            self.picture.image = f"{self.path}{self.image}_on.png"

    def __sliderRedChanged(self, n):
        self.red = int(n)
        self.led_r.value = self.red/255
        self.__processColor()

    def __sliderGreenChanged(self, n):
        self.green = int(n)
        self.led_g.value = self.green/255
        self.__processColor()

    def __sliderBlueChanged(self, n):
        self.blue = int(n)
        self.led_b.value = self.blue/255
        self.__processColor()
    