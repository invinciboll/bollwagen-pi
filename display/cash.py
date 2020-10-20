from .display import Display
from guizero import Text, Drawing, Box
from interfaces.rfid import Reader
from interfaces.repository import Database
import threading
import time


class Cash(Display):
    def __init__(self, app, path, image):
        self.stop = False
        self.db = Database("database.db")
        self.rfid = Reader()
        super().__init__(app, path, image, use_cancle_button=True, use_confirm_button=False)

    def generateComponents(self):
        self.total = Text(self.window, align="top",
                          size=self.CONST_FONT_SIZE_GENERAL*3)
        self.total.text_color = "white"

        self.top_text = Text(self.window, text="Bitte Karte auflegen",
                             align="top", size=self.CONST_FONT_SIZE_GENERAL)
        self.top_text.text_color = "white"

        self.progress_bar = Drawing(
            self.window, align="top", width="fill", visible=True)

    def open(self, *args):
        self.total_cash = args[0]
        self.total.value = f"{self.total_cash} €"
        self.window.show()
        tr = threading.Thread(target=self.start_confirmation_process)
        tr.start()

    def confirm(self):
        pass

    def cancle(self):
        self.stop = True

    def start_confirmation_process(self):
        self.stop = False
        while (not self.stop):
            sn = self.rfid.getId()
            if len(sn) > 4:
                break
            else:
                time.sleep(0.1)

        self.top_text.value = "Bestätigung durch Administrator erforderlich"
        time.sleep(1)

        while (not self.stop):
            sn_admin = self.rfid.getId()
            if sn_admin == '1048046807727':
                break
            elif len(sn_admin) > 4:
                self.top_text.text_color = "red"
                self.top_text.value = "Fehler: falsche Karte"
                time.sleep(1)
                self.top_text.text_color = "white"
                self.top_text.value = "Bitte bestätigen durch Administrator"
            else:
                time.sleep(0.1)

        if not self.stop:
            if sn_admin == '1048046807727':
                bl = self.db.getBalance(sn)
                self.db.setBalance(sn, bl + self.total_cash)
                self.top_text.text_color = "green"
                self.top_text.value = "Aufladen erfolgreich!"
                self.cancle_button.hide()
                width = 0
                for _ in range(120):
                    self.progress_bar.rectangle(
                        0, 0, width, 8, color="green")
                    time.sleep(0.016)
                    width += 4

        self.reset()

    def reset(self):
        self.close()
        self.progress_bar.clear()
        self.cancle_button.show()
        self.top_text.text_color = "white"
        self.top_text.value = "Bitte Karte auflegen"
        self.top_text.size = self.CONST_FONT_SIZE_GENERAL
