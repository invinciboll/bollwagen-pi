from display import Display
from guizero import PushButton
from displayshoppingcard import DisplayShoppingCard 
from displaybalance import DisplayBalance

class DisplayMoneyMenu(Display):
    def __init__(self, app, path, image):
        self.displays = []
        self.displays.append(DisplayShoppingCard(app, path, image))
        self.displays.append(DisplayBalance(app, path, image))
        super().__init__(app, path, image, use_cancle_button=True, use_confirm_button=False)

    def generateComponents(self):
        menu_buttons = []
        menu_buttons.append(PushButton(
            self.window, command=self.displays[0].open, text="Bezahlen"))
        menu_buttons.append(PushButton(
            self.window, command=self.displays[1].open, text="Kontostand"))
        menu_buttons.append(PushButton(
            self.window, command=None, text="Aufladen"))
        for button in menu_buttons:
            button.text_color = "white"
            button.width = "fill"
            button.height = 4
        pass

    def confirm(self):
        #not needed
        pass

    def cancle(self):
        self.close()

