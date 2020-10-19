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

        self.statistics_name = Text(
            self.window, align="top", size=self.CONST_FONT_SIZE_GENERAL, color=self.CONST_TEXT_COLOR)
       

        self.statistics_box = Box(
                    self.window, width="fill", align="top")

        self.statistic_box_drinks = Box(
                    self.statistics_box, width="fill", align="top")
        self.statistics_drinks = Text(
            self.statistics_box, align="left", size=self.CONST_FONT_SIZE_GENERAL, color=self.CONST_TEXT_COLOR)
        
        self.statistic_box_hookahs = Box(
                    self.window, width="fill", align="top")
        self.statistics_hookahs = Text(
            self.statistic_box_hookahs, align="left", size=self.CONST_FONT_SIZE_GENERAL, color=self.CONST_TEXT_COLOR)

        self.statistics_expenses = Text(
            self.window, align="top", size=self.CONST_FONT_SIZE_GENERAL, color=self.CONST_TEXT_COLOR)

        self.button_box = Box(
            self.window, width="fill", align="top", layout="grid", height=50, border=True, visible=False)

        self.b_w = PushButton(self.button_box, text="Woche", grid=[0, 0], width=12, args=['week'], command=self.get_statistic)
        self.b_w.text_color = "white"

        self.b_m = PushButton(self.button_box, text="Monat", grid=[1, 0],  width=12, args=['month'], command=self.get_statistic)
        self.b_m.text_color = "white"

        self.b_y = PushButton(self.button_box, text="Jahr", grid=[2, 0],  width=12, args=['year'], command=self.get_statistic)
        self.b_y.text_color = "white"

        self.b_l = PushButton(self.button_box, text="Gesamt",
                         grid=[3, 0],  width=12, args=['lifetime'], command=self.get_statistic)
        self.b_l.text_color = "white"

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
                name = self.db.get_name(sn)
                balance = self.db.getBalance(sn)
                self.top_text.value = f"{balance} €"
                self.top_text.text_size = self.CONST_FONT_SIZE_GENERAL*3
                self.enable_buttons(sn)
                self.statistics_name.value = f"Statistik für {name}"
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
        self.statistics_expenses.visible = f""
        self.top_text.text_color = "white"
        self.top_text.value = "Bitte Karte auflegen"
        self.top_text.size = self.CONST_FONT_SIZE_GENERAL
        self.order_history.visible = False
        self.button_box.visible = False


    def enable_buttons(self, sn):
        self.button_box.visible = True
        self.sn = sn
        self.order_history.update_command(
            self.display_history.open, sn)
        self.order_history.visible = True

    def get_statistic(self, interval):
        res = self.db.get_statistic(self.sn, interval)
        self.statistics_drinks.value = f"Getränke: {res[0]}"
        self.statistics_hookahs.value = f"Shisha-Köpfe: {res[1]}"
        expenses = res[0] * 1 + res[1] * 1.50
        self.statistics_expenses.value = f"Gesamtausgaben: {expenses} €"

        self.b_l.bg="black"
        self.b_y.bg="black"
        self.b_m.bg="black"
        self.b_w.bg="black"

        if interval == 'lifetime':
            self.b_l.bg = "blue"
        elif interval == 'year':
            self.b_y.bg = "blue"
        elif interval == 'month':
            self.b_m.bg = "blue"
        elif interval == 'week':
            self.b_w.bg = "blue"

        