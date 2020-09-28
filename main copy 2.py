from guizero import App, Window, PushButton, Box, Picture, Slider, Text, Drawing
from colormap import rgb2hex
from gpiozero import PWMLED, LED
from abc import ABC, abstractmethod

app = App(title="bollwagen", bg="black", layout="grid")


path = '/home/pi/Desktop/bw/'

class Tile:
    def __init__(self, image, grid):
        self.image = image
        self.grid = grid
        self.generateComponents()
        self.generateTileButton()

    @abstractmethod
    def generateComponents(self):
        pass
        
    @abstractmethod
    def generateTileButton(self):
        pass

###########################################################################################################################################
### Toggle Buttons ########################################################################################################################
class tTile(Tile):
    def __init__(self, image, grid, gpio):
        self.led = LED(gpio)
        super().__init__(image, grid)

    def toggle(self):
        self.led.toggle()
        if(self.led.is_active):
            self.button.image = path + self.image+'_on.png'
        else: 
            self.button.image = path + self.image+'_off.png'

    def generateTileButton(self):
        self.button = PushButton(app, command=self.toggle,
                                         grid=self.grid, align='left', image=path + self.image+'_off.png')

###########################################################################################################################################
### Menu Buttons ##########################################################################################################################
class mTile:
    def __init__(self, image, grid):
        self.image = image
        self.grid = grid

        self.generateWindow()
        self.generatePicture()
        self.generateButtonBox()
        self.generateTileButton()

    def generateWindow(self):
        self.window = Window(app, title=self.image, bg="black", visible=False)
        self.window.tk.attributes("-fullscreen", True)
        self.window.tk.config(cursor='none')

    def generatePicture(self):
        self.wPicture = Picture(self.window, image=self.image + '_off.png')

    def generateButtonBox(self):
        self.wButtonBox = Box(self.window, layout="auto",
                              align="bottom", width="fill")
        #self.wCancleButton = PushButton(self.wButtonBox, align="right",
        #                                image=path + "cancle.png", text="Close", command=self.window.hide)
        self.wOkButton = PushButton(self.wButtonBox, align="right",
                                    image=path + "ok.png", text="Close", command=self.window.hide)

    def generateTileButton(self):
        self.button = PushButton(app, command=self.window.show,
                                 grid=self.grid, align='left', image=path + self.image+'_off.png')


class mTileLed(mTile):
    r = 0,
    g = 0,
    b = 0,

    def __init__(self, image, grid, gpioR, gpioG, gpioB):
        super().__init__(image, grid)
        self.ledR = PWMLED(gpioR)
        self.ledG = PWMLED(gpioG)
        self.ledB = PWMLED(gpioB)

        self.generateDrawing()
        self.generateSliders()

    def generateDrawing(self):
        self.wDrawing = Drawing(self.window, width="fill")

    def drawColor(self):
        self.wDrawing.rectangle(
            20, 0, 460, 60, color=rgb2hex(self.r, self.g, self.b))
        if(self.r > 0 or self.g > 0 or self.b or 0):
            self.button.image = self.image + "_on.png"
        else:
            self.button.image = self.image + "_off.png"

    def sliderRedChanged(self, n):
        self.ledR.value = int(n)/255
        print(self.ledR.value)
        self.r = int(n)
        self.drawColor()

    def sliderGreenChanged(self, n):
        self.ledG.value = int(n)/255
        self.g = int(n)
        self.drawColor()

    def sliderBlueChanged(self, n):
        self.ledB.value = int(n)/255
        self.b = int(n)
        self.drawColor()

    def generateSliders(self):
        self.wSliderRed = Slider(self.window, start=0, command=self.sliderRedChanged,
                                 end=255, width="fill", height=60)
        self.wSliderRed.text_color = "red"

        self.wSliderGreen = Slider(self.window, start=0, command=self.sliderGreenChanged,
                                   end=255, width="fill", height=60)
        self.wSliderGreen.text_color = "green"

        self.wSliderBlue = Slider(self.window, start=0, command=self.sliderBlueChanged,
                                  end=255, width="fill", height=60)
        self.wSliderBlue.text_color = "blue"


tiles = []
tiles.append(tTile('sign', [0, 0], 14))
tiles.append(tTile('outside', [1, 0], 15))
tiles.append(tTile('shots', [0, 1], 16))
tiles.append(mTileLed('ambient', [1, 1], 3, 5 ,7 ))
tiles.append(mTile('effect', [0, 2]))
tiles.append(mTile('logo', [1, 2]))
tiles.append(mTile('vent', [0, 3]))
tiles.append(mTile('money', [1, 3]))

###########################################################################################################################################


def main():
    app.tk.attributes("-fullscreen", True)
    app.tk.config(cursor='none')
    app.display()


if __name__ == '__main__':
    main()
