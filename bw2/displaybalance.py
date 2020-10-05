from display import Display
from guizero import Text, Drawing, Box
from rfid import Reader
from repository import Database
import threading
import time


class DisplayBalance(Display):
    def __init__(self, app, path, image):
        self.stop = False
        self.db = Database("database.db")
        self.rfid = Reader()
        super().__init__(app, path, image, use_cancle_button=True, use_confirm_button=False)

    def generateComponents(self):
        self.top_text = Text(self.window, text="Bitte Karte auflegen",
                             align="top", size=self.CONST_FONT_SIZE_GENERAL)
        self.top_text.text_color = "white"

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
