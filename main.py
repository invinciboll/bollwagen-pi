from guizero import App, Window, PushButton, Box, Picture
import RPi.GPIO as GPIO

app = App(title="bollwagen", bg="black", layout="grid")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
path = '/home/pi/Desktop/bw/'

###########################################################################################################################################
### Toggle Buttons ########################################################################################################################

class tButton:
    def __init__(self, index, name, grid, gpio):
        self.index = index
        self.name = name
        self.grid = grid
        self.gpio = gpio

toggleButtons = []
# index,name,grid,gpio
toggleButtons.append(tButton(0, 'sign', [0, 0], 40))
toggleButtons.append(tButton(1, 'outside', [1, 0], 38))
toggleButtons.append(tButton(2, 'shots', [0, 1], 36))

def general_callback(n):
    print('general_callback()', n)
    if GPIO.input(toggleButtons[n].gpio) == 0:
        toggle_pushButtons[n].name = toggleButtons[n].name+'_on.png'
        print(toggle_pushButtons[n].name)
        GPIO.output(toggleButtons[n].gpio, GPIO.HIGH)
    else:
        toggle_pushButtons[n].name = toggleButtons[n].name+'_off.png'
        print(toggle_pushButtons[n].name)
        GPIO.output(toggleButtons[n].gpio, GPIO.LOW)

toggle_pushButtons = []
for tButton in toggleButtons:
    GPIO.setup(tButton.gpio, GPIO.OUT)
    GPIO.output(tButton.gpio, GPIO.LOW)
    toggle_pushButtons.append(PushButton(app, args=[tButton.index], command=general_callback,
                                  grid=tButton.grid, align='left', image=path + tButton.name+'_off.png'))

###########################################################################################################################################
### Menu Buttons ##########################################################################################################################

class mTile:
    def __init__(self, index, name, grid):
        self.index = index
        self.name = name
        self.grid = grid

        self.generateWindow()
        self.generatePicture()
        self.generateButtonBox()
        self.generateCancleButton()
        self.generateOkButton()
        self.generateTileButton()

    def generateWindow(self):
        self.window = Window(app,title=self.name, bg="black", visible=False)
        self.window.tk.attributes("-fullscreen", True)
        self.window.tk.config(cursor='none')

    def generatePicture(self):
        self.wPicture = Picture(self.window, image=self.name + '_off.png')
    
    def generateButtonBox(self):
        self.wButtonBox = Box(self.window, layout="auto", align="bottom", width="fill")

    def generateCancleButton(self):
        self.wCancleButton = PushButton(self.wButtonBox, align="right" ,image=path + "cancle.png", text="Close", command=self.window.hide)

    def generateOkButton(self):
        self.wOkButton = PushButton(self.wButtonBox, align="right" ,image=path + "ok.png", text="Close", command=self.window.hide)
    
    def generateTileButton(self):
        self.button = PushButton(app, command=self.window.show,
                                grid=self.grid, align='left', image=path + self.name+'_off.png')

menuTiles = []
#index, name, grid
menuTiles.append(mTile(0, 'ambient', [1, 1]))
menuTiles.append(mTile(1, 'effect', [0, 2]))
menuTiles.append(mTile(2, 'logo', [1, 2]))
menuTiles.append(mTile(3, 'vent', [0, 3]))
menuTiles.append(mTile(4, 'money', [1, 3]))

###########################################################################################################################################

def main():  
    app.tk.attributes("-fullscreen", True)
    app.tk.config(cursor='none')
    app.display()


if __name__ == '__main__':
    main()
