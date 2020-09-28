from guizero import App, Window, PushButton, Box, Picture, Slider, Text, Drawing
from colormap import rgb2hex
import RPi.GPIO as GPIO
from gpiozero import PWMLED

app = App(title="bollwagen", bg="black", layout="grid")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
path = '/home/pi/Desktop/bw/'

led = PWMLED(17)

###########################################################################################################################################
### Toggle Buttons ########################################################################################################################


class tButton:
    def __init__(self, index, image, grid, gpio):
        self.index = index
        self.image = image
        self.grid = grid
        self.gpio = gpio


def general_callback(n):
    print('general_callback()', n)
    if GPIO.input(toggleButtons[n].gpio) == 0:
        led.value = 0.8
        toggle_pushButtons[n].image = toggleButtons[n].image+'_on.png'
        GPIO.output(toggleButtons[n].gpio, GPIO.HIGH)
    else:
        led.value = 0.3
        toggle_pushButtons[n].image = toggleButtons[n].image+'_off.png'
        GPIO.output(toggleButtons[n].gpio, GPIO.LOW)


toggleButtons = []
# index,image,grid,gpio
toggleButtons.append(tButton(0, 'sign', [0, 0], 40))
toggleButtons.append(tButton(1, 'outside', [1, 0], 38))
toggleButtons.append(tButton(2, 'shots', [0, 1], 36))

toggle_pushButtons = []
for tButton in toggleButtons:
    GPIO.setup(tButton.gpio, GPIO.OUT)
    GPIO.output(tButton.gpio, GPIO.LOW)
    toggle_pushButtons.append(PushButton(app, args=[tButton.index], command=general_callback,
                                         grid=tButton.grid, align='left', image=path + tButton.image+'_off.png'))

###########################################################################################################################################
### Menu Buttons ##########################################################################################################################


class mTile:
    def __init__(self, index, image, grid):
        self.index = index
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
        self.wCancleButton = PushButton(self.wButtonBox, align="right",
                                        image=path + "cancle.png", text="Close", command=self.window.hide)
        self.wOkButton = PushButton(self.wButtonBox, align="right",
                                    image=path + "ok.png", text="Close", command=self.window.hide)

    def generateTileButton(self):
        self.button = PushButton(app, command=self.window.show,
                                 grid=self.grid, align='left', image=path + self.image+'_off.png')


class mTileLed(mTile):
    r = 0,
    g = 0,
    b = 0,

    def __init__(self, index, image, grid):
        super().__init__(index, image, grid)
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
        self.r = int(n)
        self.drawColor()

    def sliderGreenChanged(self, n):
        self.g = int(n)
        self.drawColor()

    def sliderBlueChanged(self, n):
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


menuTiles = []

#index, image, grid
menuTiles.append(mTileLed(0, 'ambient', [1, 1]))
menuTiles.append(mTile(1, 'effect', [0, 2]))
menuTiles.append(mTileLed(2, 'logo', [1, 2]))
menuTiles.append(mTile(3, 'vent', [0, 3]))
menuTiles.append(mTile(4, 'money', [1, 3]))

###########################################################################################################################################


def main():
    app.tk.attributes("-fullscreen", True)
    app.tk.config(cursor='none')
    app.display()


if __name__ == '__main__':
    main()
