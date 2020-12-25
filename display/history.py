from .display import Display
from guizero import Text, Drawing, Box
from interfaces.repository import Database
from listentry import List_Entry


class History(Display):
    def __init__(self, app, path, image):
        self.db = Database("database.db")
        super().__init__(app, path, image, use_cancle_button=True, use_confirm_button=False)

    def open(self, *args):
        self.window.show()

        self.master = Box(self.window, width="fill", height="60",
                          layout="auto", border=True)

        Text(self.master, text=f"Zeitpunkt", size=self.CONST_FONT_SIZE_GENERAL,
             color=self.CONST_TEXT_COLOR, align="left")

        box = Box(self.master, width="160", height="60",
                  layout="grid", border=True, align="right")

        Text(box, text=f"Getränke", size=self.CONST_FONT_SIZE_GENERAL,
             color=self.CONST_TEXT_COLOR, grid=[1, 0], width=8)

        Text(box, text=f"Köpfe", size=self.CONST_FONT_SIZE_GENERAL,
             color=self.CONST_TEXT_COLOR, grid=[2, 0], width=4)

        Text(box, text=f"Total", size=self.CONST_FONT_SIZE_GENERAL,
             color=self.CONST_TEXT_COLOR, grid=[3, 0], width=5)

        sn = "".join(args)
        purchases = self.db.get_purchase_history(sn)
        self.list_entries = []
        for purchase in purchases:
            self.list_entries.append(List_Entry(self.window,
                                                purchase[0], purchase[1], purchase[2]))

    def generateComponents(self):
        pass

    def confirm(self):
        pass

    def cancle(self):
        for entry in self.list_entries:
            entry.destroy()
        self.list_entries.clear()
        self.close()
