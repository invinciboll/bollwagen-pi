from guizero import Text, Box


class List_Entry():
    CONST_TEXT_COLOR = "white"
    CONST_FONT_SIZE_GENERAL = 16
    CONST_HOOKAH_PRICE = 1.50
    CONST_DRINK_PRICE = 1.00

    def __init__(self, display, timestamp, drink_sum, hookah_sum):
        self.master = Box(display, width="fill", height="60",
                          layout="auto", border=True)

        Text(self.master, text=f"{timestamp}", size=self.CONST_FONT_SIZE_GENERAL,
             color=self.CONST_TEXT_COLOR, align="left")

        box = Box(self.master, width="160", height="60",
                  layout="grid", border=True, align="right")

        Text(box, text=f"{drink_sum}", size=self.CONST_FONT_SIZE_GENERAL,
             color=self.CONST_TEXT_COLOR, grid=[1, 0], width=4)

        Text(box, text=f"{hookah_sum}", size=self.CONST_FONT_SIZE_GENERAL,
             color=self.CONST_TEXT_COLOR, grid=[2, 0], width=4)

        total = drink_sum * self.CONST_DRINK_PRICE + \
            hookah_sum * self.CONST_HOOKAH_PRICE

        Text(box, text=f"{total} €", size=self.CONST_FONT_SIZE_GENERAL,
             color=self.CONST_TEXT_COLOR, grid=[3, 0], width=5)

    def destroy(self):
        self.master.destroy()
