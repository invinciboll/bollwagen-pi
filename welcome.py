from guizero import Window, Picture, PushButton, Text, Box
import Adafruit_DHT
import time
import threading

class Welcome:
    CONST_TEXT_COLOR = "white"
    CONST_FONT_SIZE_GENERAL = 16

    def __init__(self, app, path, image, gpio):
        self.DHT_SENSOR = Adafruit_DHT.DHT11
        self.DHT_PIN = gpio
        self.leave = False

        self.window = Window(app, title=image, bg="black", visible=True)
        self.window.tk.attributes("-fullscreen", True)
        self.window.tk.config(cursor='none')

        self.clock = Text(self.window,
                          align="top", size=self.CONST_FONT_SIZE_GENERAL*6, color=self.CONST_TEXT_COLOR, font="Roboto Thin")
        
        #empty box for spacing
        Box(self.window, align="top", height=40, border=True)

        Picture(self.window, image=f"{path}{image}.png")

        #empty box for spacing
        Box(self.window, align="top", height=80, border=True)
        
        info_box = Box(self.window, align="top", layout="grid", border=True)

        self.temp = Text(info_box, grid=[0,0], align="left", size=self.CONST_FONT_SIZE_GENERAL*2, color=self.CONST_TEXT_COLOR, font="Roboto Thin")

        #empty string for spacing
        Text(info_box, grid=[1,0],text="        ", size=self.CONST_FONT_SIZE_GENERAL*2, color=self.CONST_TEXT_COLOR)

        self.hum = Text(info_box, grid=[2,0],align="right",size=self.CONST_FONT_SIZE_GENERAL*2, color=self.CONST_TEXT_COLOR, font="Roboto Thin")
        
        button = PushButton(self.window, width="fill", align="bottom", text="Home", height=4, command=self.cancle)
        button.text_color="white"
        button.font = "Roboto"

    def open(self, *args):
        self.window.show()
        tr = threading.Thread(target=self.action)
        tr.start()

    def close(self, *args):
        self.window.hide()

    def action(self):
        while not self.leave:
            t = time.localtime()
            self.clock.value = time.strftime("%H:%M", t)

            humidity, temperature = Adafruit_DHT.read(
                self.DHT_SENSOR, self.DHT_PIN)
            if temperature is not None:
                self.temp.value = "{0:0.1f}C".format(
                    temperature)
            else:
                self.hum.value = "no temp"

            if humidity is not None:
                self.hum.value = "{0:0.1f}%".format(
                    humidity)
            else:
                self.hum.value = "no hum"
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
        