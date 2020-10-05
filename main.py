# gpiozero needs rpigpio as native factory in system variables ~/.bashrc
# display is used naming for window

from guizero import App, Window, PushButton, Box, Picture, Slider, Text, Drawing
from colormap import rgb2hex
from gpiozero import PWMLED, LED
from abc import ABC, abstractmethod
from repository import Database
from rfid import Reader
import threading
import time
from display import *


app = App(title="bollwagen", bg="black", layout="grid")
db = Database("database.db")
rfid = Reader()
path = '/home/pi/Desktop/bw/'


class Tile:
    def __init__(self, image, grid):
        self.image = image
        self.grid = grid

###########################################################################################################################################
### Toggle Buttons ########################################################################################################################


class tTile(Tile):
    def __init__(self, image, grid, gpio):
        super().__init__(image, grid)
        self.led = LED(gpio)
        self.button = PushButton(app, command=self.toggle,
                                 grid=self.grid, align='left', image=path + self.image+'_off.png')

    def toggle(self):
        self.led.toggle()
        if(self.led.is_active):
            self.button.image = path + self.image+'_on.png'
        else:
            self.button.image = path + self.image+'_off.png'


###########################################################################################################################################
### Menu Buttons ##########################################################################################################################


class mTile(Tile):
    def __init__(self, image, grid):
        super().__init__(image, grid)
        self.display = Display(app, self.image, True, True)
        PushButton(app, command=self.display.open,
                                 grid=self.grid, align='left', image=path + self.image+'_off.png')

class mTileLedNew(mTile):
     def __init__(self, image, grid, gpioR, gpioG, gpioB):
        super().__init__(image, grid)
        self.ledR = PWMLED(gpioR)
        self.ledG = PWMLED(gpioG)
        self.ledB = PWMLED(gpioB)
        self.r = 0
        self.g = 0
        self.b = 0
        super().__init__(image, grid)
        self.generateDrawing()
        self.generateSliders()

class mTileLed(mTile):
    def __init__(self, image, grid, gpioR, gpioG, gpioB):
        self.ledR = PWMLED(gpioR)
        self.ledG = PWMLED(gpioG)
        self.ledB = PWMLED(gpioB)
        self.r = 0
        self.g = 0
        self.b = 0
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
        self.generateBalanceWindow()
        self.generatePaymentMethodWindow()
        self.generateChargeWindow()
        self.cw = Display(app, "money", True, True)
        self.generateMenu()

    def reset(self):
        self.drinkSum = 0
        self.hookahSum = 0
        self.updateDisplayedSums()

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
        self.reset()
        self.payWindow.hide()

    def generateCardWindow(self):
        self.pCardWindow = Window(self.payWindow, bg="black", visible=False)
        self.pCardWindow.tk.attributes("-fullscreen", True)
        self.pCardWindow.tk.config(cursor='none')

    def generateCardWindowComponents(self):
        self.pCWPicture = Picture(
            self.pCardWindow, image=self.image + '_off.png', align="top")

        self.pCWMasterBox = Box(
            self.pCardWindow, width="fill", align="top", border=self.CONST_SHOW_BORDER)
        self.pCWTotal = Text(self.pCWMasterBox, text=f"{self.total} €")
        self.pCWTotal.text_color = "white"
        self.pCWTotal.text_size = self.CONST_FONT_SIZE

        self.pCWText = Text(
            self.pCardWindow, text="Bitte Karte auflegen", align="top")
        self.pCWText.text_color = "white"
        self.pCWText.text_size = self.CONST_FONT_SIZE

        self.pCWAnswer = Text(
            self.pCardWindow, align="top")
        self.pCWAnswer.text_color = "white"
        self.pCWAnswer.text_size = self.CONST_FONT_SIZE

        self.wDrawing = Drawing(
            self.pCardWindow, align="top", width="fill", visible=True)

        self.pCWCancleButton = PushButton(
            self.pCardWindow, command=self.closePaymentProcess, text="Zurück", height=4, width="fill", align="bottom")
        self.pCWCancleButton.text_color = "white"

    def startPaymentProcess(self):
        sn = rfid.getId()
        balance = db.getBalance(sn)
        self.pCWAnswer.size = self.CONST_FONT_SIZE
        if (self.total <= balance):
            db.setBalance(sn, balance-self.total)
            db.insertPurchase(sn, self.drinkSum, self.hookahSum)

            self.pCWAnswer.text_color = "green"
            self.pCWAnswer.value = "Danke!"
            self.pCWCancleButton.hide()
            width = 0
            for _ in range(120):
                self.wDrawing.rectangle(
                    0, 0, width, 8, color="green")
                time.sleep(0.016)
                width += 4

            self.wDrawing.clear()
            self.pCardWindow.hide()
            self.payWindow.hide()
            self.window.hide()

        else:
            self.pCWAnswer.text_color = "red"
            self.pCWAnswer.value = "Fehler: zu wenig Guthaben"
            self.pCWCancleButton.hide()
            time.sleep(2)
            self.pCardWindow.hide()
            self.payWindow.hide()

        self.pCWAnswer.value = ""
        self.reset()
        self.pCWCancleButton.show()

    def openPaymentProcess(self):
        self.pCardWindow.show()
        self.tr = threading.Thread(target=self.startPaymentProcess)
        self.tr.start()

    def closePaymentProcess(self):
        self.pCardWindow.hide()
        self.tr._stop()

    def generatePayWindow(self):
        self.payWindow = Window(self.window, bg="black", visible=False)
        self.payWindow.tk.attributes("-fullscreen", True)
        self.payWindow.tk.config(cursor='none')

    def generatePayWindowComponents(self):
        self.payWindowPicture = Picture(
            self.payWindow, image=self.image + '_off.png', align="top")

        # ---Box Layout---------------------------------------------------------------------------------------------------------------------
        self.masterBox = Box(self.payWindow, width="fill",
                             align="top", border=self.CONST_SHOW_BORDER)
        # ---Plus buttons
        self.buttonBoxPlus = Box(
            self.masterBox, align="right", layout="grid", border=self.CONST_SHOW_BORDER)
        self.pWBDButtonPlus = PushButton(
            self.buttonBoxPlus, command=self.addDrink, width=4, height=2, text="+", grid=[0, 0])
        self.pWBDButtonPlus.text_color = "white"
        self.pWBDButtonPlus.text_size = self.CONST_FONT_SIZE
        self.pWBHButtonPlus = PushButton(
            self.buttonBoxPlus, command=self.addHookah, width=4, height=2, text="+", grid=[0, 1])
        self.pWBHButtonPlus.text_color = "white"
        self.pWBHButtonPlus.text_size = self.CONST_FONT_SIZE
        # ---Sum labels
        self.sumBox = Box(self.masterBox, align="right",
                          layout="grid", border=self.CONST_SHOW_BORDER)
        self.pWBDSum = Text(self.sumBox,
                            text=self.drinkSum, grid=[0, 0], color="white", width=4, height=3)
        self.pWBDSum.text_size = self.CONST_FONT_SIZE
        self.pWBHSum = Text(self.sumBox,
                            text=self.hookahSum, grid=[0, 1], color="white", width=4, height=3)
        self.pWBHSum.text_size = self.CONST_FONT_SIZE
        # ---Minus Buttons
        self.buttonBoxMinus = Box(
            self.masterBox, align="right", layout="grid", border=self.CONST_SHOW_BORDER)
        self.pWBDButtonMinus = PushButton(
            self.buttonBoxMinus, command=self.removeDrink, width=4, height=2, text="-", grid=[0, 0])
        self.pWBDButtonMinus.text_color = "white"
        self.pWBDButtonMinus.text_size = self.CONST_FONT_SIZE
        self.pWBHButtonMinus = PushButton(
            self.buttonBoxMinus, command=self.removeHookah, width=4, height=2, text="-", grid=[0, 1])
        self.pWBHButtonMinus.text_color = "white"
        self.pWBHButtonMinus.text_size = self.CONST_FONT_SIZE
        # ---Descriptive row labels
        self.labelBox = Box(self.masterBox, align="left",
                            layout="grid", border=self.CONST_SHOW_BORDER)
        self.pWBDText = Text(self.labelBox,
                             text="Getränke", grid=[0, 0], color="white", align="left", height=3, size=self.CONST_FONT_SIZE)
        self.pWBHText = Text(self.labelBox,
                             text="Shisha-Köpfe", grid=[0, 1], color="white", align="left", height=3, size=self.CONST_FONT_SIZE)
        # ---Total section
        self.totalBox = Box(self.payWindow, width="fill",
                            align="top", border=self.CONST_SHOW_BORDER)
        self.totalBoxLeft = Box(
            self.totalBox, align="left", layout="grid", border=self.CONST_SHOW_BORDER)
        self.pWBTText = Text(self.totalBoxLeft,
                             text="Total:", color="white", grid=[0, 0], width=4, height=3, size=self.CONST_FONT_SIZE)
        self.totalBoxRight = Box(
            self.totalBox, align="right", layout="grid", border=self.CONST_SHOW_BORDER)
        self.pWBTEuro = Text(self.totalBoxRight, text="€",  color="white", grid=[
                             1, 0], width=4, height=3, size=self.CONST_FONT_SIZE)
        self.pWBTSum = Text(self.totalBoxRight, text=self.total, color="white", grid=[
                            0, 0], width=4, height=3, size=self.CONST_FONT_SIZE)

        self.payWindowCancleButton = PushButton(
            self.payWindow, command=self.closePayWindow, text="Abbrechen", height=4, width="fill", align="bottom")
        self.payWindowCancleButton.text_color = "white"

        self.payWindowPayButton = PushButton(
            self.payWindow, command=self.openPaymentProcess, text="Bezahlen", height=4, width="fill", align="bottom")
        self.payWindowPayButton.text_color = "white"

    # Kontoübersicht anzeigen
    def generateBalanceWindow(self):
        self.balanceWindow = Window(self.payWindow, bg="black", visible=False)
        self.balanceWindow.tk.attributes("-fullscreen", True)
        self.balanceWindow.tk.config(cursor='none')

        self.bWPicture = Picture(
            self.balanceWindow, image=self.image + '_off.png', align="top")

        self.bWText = Text(
            self.balanceWindow, text="Bitte Karte auflegen", align="top")
        self.bWText.text_color = "white"
        self.bWText.text_size = self.CONST_FONT_SIZE

        self.bWStatisticBox = Box(self.balanceWindow, width="fill",
                                  align="top", layout="grid", border=self.CONST_SHOW_BORDER)
        self.bWStatisticName = Text(
            self.bWStatisticBox, align="left", grid=[0, 0])
        self.bWStatisticName.text_color = "white"
        self.bWStatisticName.text_size = self.CONST_FONT_SIZE
        self.bWStatisticDrinks = Text(
            self.bWStatisticBox, align="left", grid=[0, 1])
        self.bWStatisticDrinks.text_color = "white"
        self.bWStatisticDrinks.text_size = self.CONST_FONT_SIZE
        self.bWStatisticHookahs = Text(
            self.bWStatisticBox, align="left", grid=[0, 2])
        self.bWStatisticHookahs.text_color = "white"
        self.bWStatisticHookahs.text_size = self.CONST_FONT_SIZE

        self.bWCancleButton = PushButton(
            self.balanceWindow, command=self.hideBalanceWindow, text="Zurück", height=4, width="fill", align="bottom")
        self.bWCancleButton.text_color = "white"

    def startBalanceScan(self):
        sn = rfid.getId()
        # bl = db.getBalance(sn)
        user = db.getAccountInformation(sn)
        self.bWText.value = f"{user.balance} €"
        self.bWText.text_size = self.CONST_FONT_SIZE*3
        self.bWStatisticName.value = f"Statistik für {user.name}"
        self.bWStatisticDrinks.value = f"Getränke: {user.drinkSum}"
        self.bWStatisticHookahs.value = f"Shisha-Köpfe: {user.hookahSum}"

    def showBalanceWindow(self):
        tr = threading.Thread(target=self.startBalanceScan)
        self.balanceWindow.show()
        tr.start()

    def hideBalanceWindow(self):
        self.bWText.value = "Bitte Karte auflegen"
        self.bWText.text_size = self.CONST_FONT_SIZE
        self.bWStatisticName.value = ""
        self.bWStatisticDrinks.value = ""
        self.bWStatisticHookahs.value = ""
        self.balanceWindow.hide()

    # Konto Aufladen
    def cWaddNumber(self, n):
        if n is "<" and len(self.cWcurrentInput) > 0:
            self.cWcurrentInput.pop(0)
        elif n is 0 and len(self.cWcurrentInput) is 0:
            pass
        elif type(n) is int:
            self.cWcurrentInput.insert(0, n)

        mystring = ""
        for index, digit in enumerate(self.cWcurrentInput):
            if index is 2:
                mystring = f"{digit}" + f"." + mystring
            else:
                mystring = f"{digit}" + mystring

        if len(self.cWcurrentInput) is 0:
            self.cWText.value = f"Bitte Betrag eingeben"
        elif len(self.cWcurrentInput) is 1:
            self.cWText.value = f"0.0{mystring} €"
        elif len(self.cWcurrentInput) is 2:
            self.cWText.value = f"0.{mystring} €"
        else:
            self.cWText.value = f"{mystring} €"

    def generatePaymentMethodWindow(self):
        self.paymentMethodWindow = Window(self.payWindow, bg="black", visible=False)
        self.paymentMethodWindow.tk.attributes("-fullscreen", True)
        self.paymentMethodWindow.tk.config(cursor='none')

        self.pMWPicture = Picture(
            self.paymentMethodWindow, image=self.image + '_off.png', align="top")

        self.pMWText = Text(
            self.paymentMethodWindow, text="Bezahlmethode auswählen", height=3, align="top")
        self.pMWText.text_color = "white"
        self.pMWText.text_size = self.CONST_FONT_SIZE

        self.cWCashButton = PushButton(
            self.paymentMethodWindow, command=None, text="Bar", height=4, width="fill", align="top")
        self.cWCashButton.text_color = "white"

        self.cWPayPalButton = PushButton(
            self.paymentMethodWindow, command=None, text="Paypal", height=4, width="fill", align="top", enabled=False)
        self.cWPayPalButton.text_color = "white"
        self.cWPayPalButton.bg = "blue"

        self.cWCancleButton = PushButton(
            self.paymentMethodWindow, command=self.paymentMethodWindow.hide, text="Zurück", height=4, width="fill", align="bottom")
        self.cWCancleButton.text_color = "white"

    def generateChargeWindow(self):
        self.chargeWindow = Window(self.payWindow, bg="black", visible=False)
        self.chargeWindow.tk.attributes("-fullscreen", True)
        self.chargeWindow.tk.config(cursor='none')

        self.cWPicture = Picture(
            self.chargeWindow, image=self.image + '_off.png', align="top")

        self.cWText = Text(
            self.chargeWindow, text="Bitte Betrag eingeben", height=3, align="top")
        self.cWText.text_color = "white"
        self.cWText.text_size = self.CONST_FONT_SIZE
        self.cWcurrentInput = []

        self.cWNumpad = Box(self.chargeWindow, layout="grid",
                            width="240", align="top")

        buttonsNumpad = []
        buttonsNumpad.append(PushButton(
            self.cWNumpad, command=self.cWaddNumber, args=[0], text="0", grid=[1, 3]))
        buttonsNumpad.append(PushButton(
            self.cWNumpad, command=self.cWaddNumber, args=[1], text="1", grid=[0, 0]))
        buttonsNumpad.append(PushButton(
            self.cWNumpad, command=self.cWaddNumber, args=[2], text="2", grid=[1, 0]))
        buttonsNumpad.append(PushButton(
            self.cWNumpad, command=self.cWaddNumber, args=[3], text="3", grid=[2, 0]))
        buttonsNumpad.append(PushButton(
            self.cWNumpad, command=self.cWaddNumber, args=[4], text="4", grid=[0, 1]))
        buttonsNumpad.append(PushButton(
            self.cWNumpad, command=self.cWaddNumber, args=[5], text="5", grid=[1, 1]))
        buttonsNumpad.append(PushButton(
            self.cWNumpad, command=self.cWaddNumber, args=[6], text="6", grid=[2, 1]))
        buttonsNumpad.append(PushButton(
            self.cWNumpad, command=self.cWaddNumber, args=[7], text="7", grid=[0, 2]))
        buttonsNumpad.append(PushButton(
            self.cWNumpad, command=self.cWaddNumber, args=[8], text="8", grid=[1, 2]))
        buttonsNumpad.append(PushButton(
            self.cWNumpad, command=self.cWaddNumber, args=[9], text="9", grid=[2, 2]))
        buttonsNumpad.append(PushButton(
            self.cWNumpad, command=self.cWaddNumber, args=["<"], text="<", grid=[2, 3]))

        for button in buttonsNumpad:
            button.text_size = self.CONST_FONT_SIZE*2
            button.text_color = "white"
            button.width = 2
            button.height = 1

        self.cWCancleButton = PushButton(
            self.chargeWindow, command=self.chargeWindow.hide, text="Zurück", height=4, width="fill", align="bottom")
        self.cWCancleButton.text_color = "white"

        self.cWConfirmButton = PushButton(
            self.chargeWindow, command=self.paymentMethodWindow.show, text="Bestätigen", height=4, width="fill", align="bottom")
        self.cWConfirmButton.text_color = "white"

    def cheat(self):
        sn = rfid.getId()
        bl = db.getBalance(sn)
        db.setBalance(sn, bl+20)

    def generateMenu(self):
        self.menuButtons = []
        self.menuButtons.append(PushButton(
            self.window, command=self.payWindow.show, text="Bezahlen"))
        self.menuButtons.append(PushButton(
            self.window, command=self.showBalanceWindow, text="Kontostand"))
        self.menuButtons.append(PushButton(
            self.window, command=self.cw.open, text="Aufladen"))
        for button in self.menuButtons:
            button.text_color = "white"
            button.width = "fill"
            button.height = 4


tiles = []
tiles.append(tTile('sign', [0, 0], 14))
tiles.append(tTile('outside', [1, 0], 15))
tiles.append(tTile('shots', [0, 1], 16))
#tiles.append(mTileLed('ambient', [1, 1], 3, 4, 17))
tiles.append(mTile('effect', [0, 2]))
#tiles.append(mTileLed('logo', [1, 2], 18, 23, 24))
#tiles.append(mTileVent('vent', [0, 3], 12))
#tiles.append(mTileMoney('money', [1, 3]))


###########################################################################################################################################
##


def main():
    app.tk.attributes("-fullscreen", True)
    app.tk.config(cursor='none')
    app.display()


if __name__ == '__main__':
    main()
