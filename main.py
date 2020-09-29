from guizero import App, Window, PushButton, Box, Picture, Slider, Text, Drawing
from colormap import rgb2hex
from gpiozero import PWMLED, LED
from abc import ABC, abstractmethod
from repository import Database

app = App(title="bollwagen", bg="black", layout="grid")
db = Database("database.db")
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
            print(db.getBalance("myrfid"))
        else:
            self.button.image = path + self.image+'_off.png'

    def generateTileButton(self):
        self.button = PushButton(app, command=self.toggle,
                                 grid=self.grid, align='left', image=path + self.image+'_off.png')

###########################################################################################################################################
### Menu Buttons ##########################################################################################################################


class mTile(Tile):
    def __init__(self, image, grid):
        super().__init__(image, grid)

    def generateComponents(self):
        self.window = Window(app, title=self.image, bg="black", visible=False)
        self.window.tk.attributes("-fullscreen", True)
        self.window.tk.config(cursor='none')

        self.wPicture = Picture(self.window, image=self.image + '_off.png')

        self.wBackButton = PushButton(
            self.window, command=self.window.hide, text="Zurück", height=4, width="fill", align="bottom")
        self.wBackButton.text_color = "white"

    def generateTileButton(self):
        self.button = PushButton(app, command=self.window.show,
                                 grid=self.grid, align='left', image=path + self.image+'_off.png')


class mTileLed(mTile):
    def __init__(self, image, grid, gpioR, gpioG, gpioB):
        self.ledR = PWMLED(gpioR)
        self.ledG = PWMLED(gpioG)
        self.ledB = PWMLED(gpioB)
        super().__init__(image, grid)
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


class mTileVent(mTile):
    def __init__(self, image, grid, gpio):
        self.fan = PWMLED(gpio)
        super().__init__(image, grid)
        self.generateSlider()

    def sliderFanChanged(self):
        pass

    def generateSlider(self):
        self.wText = Text(self.window, "Geschwindigkeit",
                          color="white", size="24")
        self.wSliderFan = Slider(self.window, start=0, command=self.sliderFanChanged,
                                 end=100, width="fill", height=100)
        self.wSliderFan.text_color = "white"


class mTileMoney(mTile):
    drinkSum = 0
    hookahSum = 0
    total = 0
    CONST_DRINK_PRICE = 1
    CONST_HOOKAH_PRICE = 1.5
    CONST_FONT_SIZE = 16
    CONST_SHOW_BORDER = False

    def __init__(self, image, grid):
        super().__init__(image, grid)
        self.generatePayWindow()
        self.generateCardWindow()
        self.generateCardWindowComponents()
        self.generatePayWindowComponents()
        self.generateMenu()

    def updateDisplayedSums(self):
        self.pWBDSum.value = self.drinkSum
        self.pWBHSum.value = self.hookahSum
        self.total = self.hookahSum*self.CONST_HOOKAH_PRICE + \
            self.drinkSum*self.CONST_DRINK_PRICE
        self.pWBTSum.value = self.total
        self.pCWTotal.value = self.total

    def addDrink(self):
        self.drinkSum += 1
        self.updateDisplayedSums()

    def removeDrink(self):
        if(self.drinkSum > 0):
            self.drinkSum -= 1
            self.updateDisplayedSums()

    def addHookah(self):
        self.hookahSum += 1
        self.updateDisplayedSums()

    def removeHookah(self):
        if(self.hookahSum > 0):
            self.hookahSum -= 1
            self.updateDisplayedSums()

    def closePayWindow(self):
        self.hookahSum = 0
        self.drinkSum = 0
        self.total = 0
        self.payWindow.hide()

    def generateCardWindow(self):
        self.pCardWindow = Window(self.payWindow, bg="black", visible=False)
        self.pCardWindow.tk.attributes("-fullscreen", True)
        self.pCardWindow.tk.config(cursor='none')

    def generateCardWindowComponents(self):
        self.payWindowPicture = Picture(
            self.pCardWindow, image=self.image + '_off.png')

        self.pCWTotal = Text(self.pCardWindow, text=self.total)
        self.pCWTotal.text_color = "white"
        self.pCWTotal.text_size = "24"

        self.pCWText = Text(
            self.pCardWindow, text="Bitte Karte auflegen", align="top")
        self.pCWText.text_color = "white"
        self.pCWText.text_size = "24"

        self.pCardWindowCancleButton = PushButton(
            self.pCardWindow, command=self.pCardWindow.hide, text="Abbrechen", height=4, width="fill", align="bottom")
        self.pCardWindowCancleButton.text_color = "white"

    def generatePayWindow(self):
        self.payWindow = Window(self.window, bg="black", visible=False)
        self.payWindow.tk.attributes("-fullscreen", True)
        self.payWindow.tk.config(cursor='none')

    def generatePayWindowComponents(self):
        self.payWindowPicture = Picture(
            self.payWindow, image=self.image + '_off.png', align="top")


        self.masterBox = Box(self.payWindow, width="fill", align="top", border=self.CONST_SHOW_BORDER)
        
        self.buttonBoxPlus = Box(self.masterBox, align="right", layout="grid", border=self.CONST_SHOW_BORDER)
        self.pWBDButtonPlus = PushButton(self.buttonBoxPlus, command=self.addDrink, width=4, height=2, text="+", grid=[0,0])
        self.pWBDButtonPlus.text_color = "white"
        self.pWBDButtonPlus.text_size = self.CONST_FONT_SIZE
        self.pWBHButtonPlus = PushButton(self.buttonBoxPlus, command=self.addHookah, width=4, height=2, text="+", grid=[0,1])
        self.pWBHButtonPlus.text_color = "white" 
        self.pWBHButtonPlus.text_size = self.CONST_FONT_SIZE    

        self.sumBox = Box(self.masterBox, align="right", layout="grid",border=self.CONST_SHOW_BORDER)
        self.pWBDSum = Text(self.sumBox,
                            text=self.drinkSum, grid=[0,0], color="white", width=4, height=3)
        self.pWBDSum.text_size=self.CONST_FONT_SIZE   
        self.pWBHSum = Text(self.sumBox,
                            text=self.hookahSum, grid=[0,1], color="white", width=4, height=3)
        self.pWBHSum.text_size=self.CONST_FONT_SIZE   

        self.buttonBoxMinus = Box(self.masterBox, align="right", layout="grid",border=self.CONST_SHOW_BORDER)
        self.pWBDButtonMinus = PushButton(self.buttonBoxMinus, command=self.removeDrink, width=4, height=2, text="-", grid=[0,0])
        self.pWBDButtonMinus.text_color = "white"
        self.pWBDButtonMinus.text_size = self.CONST_FONT_SIZE   
        self.pWBHButtonMinus = PushButton(self.buttonBoxMinus, command=self.removeHookah, width=4, height=2, text="-", grid=[0,1])
        self.pWBHButtonMinus.text_color = "white"
        self.pWBHButtonMinus.text_size = self.CONST_FONT_SIZE    
        
        self.labelBox = Box(self.masterBox, align="left", layout="grid",border=self.CONST_SHOW_BORDER)
        self.pWBDText = Text(self.labelBox,
                             text="Getränke", grid=[0,0], color="white",align="left", height=3, size=self.CONST_FONT_SIZE)
        self.pWBHText = Text(self.labelBox,
                             text="Shisha-Köpfe", grid=[0,1], color="white",align="left", height=3, size=self.CONST_FONT_SIZE)

        self.totalBox = Box(self.payWindow,width="fill", align="top",border=self.CONST_SHOW_BORDER)
        self.totalBoxLeft = Box(self.totalBox, align="left", layout="grid",border=self.CONST_SHOW_BORDER)
        self.pWBTText = Text(self.totalBoxLeft,
                             text="Total:", color="white",grid=[0,0],width=4, height=3, size=self.CONST_FONT_SIZE)
        self.totalBoxRight = Box(self.totalBox, align="right", layout="grid",border=self.CONST_SHOW_BORDER)
        self.pWBTEuro = Text(self.totalBoxRight, text="€",  color="white", grid=[1,0], width=4, height=3, size=self.CONST_FONT_SIZE)
        self.pWBTSum = Text(self.totalBoxRight, text=self.total, color="white", grid=[0,0], width=4, height=3, size=self.CONST_FONT_SIZE)



        self.payWindowCancleButton = PushButton(
            self.payWindow, command=self.closePayWindow, text="Abbrechen", height=4, width="fill", align="bottom")
        self.payWindowCancleButton.text_color = "white"

        self.payWindowPayButton = PushButton(
            self.payWindow, command=self.pCardWindow.show, text="Bezahlen", height=4, width="fill", align="bottom")
        self.payWindowPayButton.text_color = "white"

    def generateMenu(self):
        self.menuButtons = []
        self.menuButtons.append(PushButton(
            self.window, command=self.payWindow.show, text="Bezahlen"))
        self.menuButtons.append(PushButton(
            self.window, command=None, text="Kontostand"))
        self.menuButtons.append(PushButton(
            self.window, command=None, text="Aufladen"))
        for button in self.menuButtons:
            button.text_color = "white"
            button.width = "fill"
            button.height = 4


tiles = []
tiles.append(tTile('sign', [0, 0], 14))
tiles.append(tTile('outside', [1, 0], 15))
tiles.append(tTile('shots', [0, 1], 16))
tiles.append(mTileLed('ambient', [1, 1], 3, 5, 7))
tiles.append(mTile('effect', [0, 2]))
tiles.append(mTile('logo', [1, 2]))
tiles.append(mTileVent('vent', [0, 3], 21))
tiles.append(mTileMoney('money', [1, 3]))

###########################################################################################################################################
##


def main():
    app.tk.attributes("-fullscreen", True)
    app.tk.config(cursor='none')
    app.display()


if __name__ == '__main__':
    main()
