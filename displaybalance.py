from display import Display
from guizero import Text, Drawing, Box, PushButton
from rfid import Reader
from repository import Database
from displayhistory import DisplayHistory
import threading
import time


class DisplayBalance(Display):
    def __init__(self, app, path, image):
        self.stop = False
        self.db = Database("database.db")
        self.rfid = Reader()
        self.display_history = DisplayHistory(app, path, image)
        super().__init__(app, path, image, use_cancle_button=True, use_confirm_button=False)

    def generateComponents(self):
        self.top_text = Text(self.window, text="Bitte Karte auflegen",
                             align="top", size=self.CONST_FONT_SIZE_GENERAL)
        self.top_text.text_color = "white"

        self.button_box = Box(
            self.window, width="fill", align="top", layout="grid", height=50, border=True, visible=False)

        b_w = PushButton(self.button_box, text="Woche", grid=[0, 0], width=12)
        b_w.text_color = "white"

        b_m = PushButton(self.button_box, text="Monat", grid=[1, 0],  width=12)
        b_m.text_color = "white"

        b_y = PushButton(self.button_box, text="Jahr", grid=[2, 0],  width=12)
        b_y.text_color = "white"

        b_l = PushButton(self.button_box, text="Gesamt",
                         grid=[3, 0],  width=12)
        b_l.text_color = "white"

        self.statistics_box = Box(
            self.window, width="fill", align="top", layout="grid")

        self.statistics_name = Text(
            self.statistics_box, align="left", grid=[0, 0], size=self.CONST_FONT_SIZE_GENERAL)
        self.statistics_name.text_color = "white"

        self.statistics_drinks = Text(
            self.statistics_box, align="left", grid=[0, 1], size=self.CONST_FONT_SIZE_GENERAL)
        self.statistics_drinks.text_color = "white"

        self.statistics_hookahs = Text(
            self.statistics_box, align="left", grid=[0, 2], size=self.CONST_FONT_SIZE_GENERAL)
        self.statistics_hookahs.text_color = "white"

        self.order_history = PushButton(
            self.window, width="fill", command=None, text="Kaufhistorie", visible=False)
        self.order_history.text_color = "white"

    def open(self, *args):
        self.window.show()
        tr = threading.Thread(target=self.startScanProcess)
        tr.start()

    def confirm(self):
        #not needed
        pass

    def cancle(self):
        self.stop = True

    def startScanProcess(self):
        self.stop = False
        while (not self.stop):
            sn = self.rfid.getId()
            if len(sn) > 4:
                user = self.db.getAccountInformation(sn)
                self.top_text.value = f"{user.balance} €"
                self.top_text.text_size = self.CONST_FONT_SIZE_GENERAL*3
                self.button_box.visible = True
                self.order_history.update_command(
                    self.display_history.open, sn)
                self.order_history.visible = True
                self.statistics_name.value = f"Statistik für {user.name}"
                self.statistics_drinks.value = f"Getränke: {user.drinkSum}"
                self.statistics_hookahs.value = f"Shisha-Köpfe: {user.hookahSum}"
            else:
                time.sleep(0.1)
        # break from thread
        print("Killing Thread")
        self.reset()

    def reset(self):
        self.close()
        self.statistics_name.value = f""
        self.statistics_drinks.value = f""
        self.statistics_hookahs.value = f""
        self.top_text.text_color = "white"
        self.top_text.value = "Bitte Karte auflegen"
        self.top_text.size = self.CONST_FONT_SIZE_GENERAL
        self.order_history.visible = False
        self.button_box.visible = False
