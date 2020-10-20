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
