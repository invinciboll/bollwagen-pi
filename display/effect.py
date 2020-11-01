from .display import Display
from guizero import Slider, Drawing, PushButton, Box, Text
from colormap import rgb2hex
from interfaces.dmx import set


class Effect(Display):
    def __init__(self, app, path, image):
        self.dmx_values = [0, 0, 0, 0]

        super().__init__(
            app, path, image, use_cancle_button=True, use_confirm_button=False)

    def generateComponents(self):
        selectbox = Box(self.window, width="fill", layout="grid")

        ef = PushButton(selectbox, text="Einzelfarbe",
                        grid=[0, 0], width=17, args=['color'], command=self.switch_view)
        ef.text_color = "white"
        fw = PushButton(selectbox, text="Farbwechsel",
                        grid=[1, 0], width=16, args=['change'], command=self.switch_view)
        fw.text_color = "white"
        stl = PushButton(selectbox, text="Sound to light",
                         grid=[2, 0], width=17, args=['stl'], command=self.switch_view)
        stl.text_color = "white"

        # -- widgets for color mode --
        self.color_mode = Box(self.window, width="fill", layout="auto")
        select_box = Box(self.color_mode, width="fill", layout="grid")
        PushButton(select_box, width=90, height=45, grid=[
                   0, 0], image="./assets/colors/red.png", args=[0, 10], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   1, 0], image="./assets/colors/green.png", args=[0, 20], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   2, 0], image="./assets/colors/blue.png", args=[0, 30], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   3, 0], image="./assets/colors/orange.png", args=[0, 50], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   4, 0], image="./assets/colors/white.png", args=[0, 40], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   0, 1], image="./assets/colors/purple.png", args=[0, 60], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   1, 1], image="./assets/colors/red_white.png", args=[0, 70], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   2, 1], image="./assets/colors/green_white.png", args=[0, 100], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   3, 1], image="./assets/colors/red_purple.png", args=[0, 80], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   4, 1], image="./assets/colors/green_blue.png", args=[0, 90], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   0, 2], image="./assets/colors/blue_white.png", args=[0, 110], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   1, 2], image="./assets/colors/red_green_orange.png", args=[0, 120], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   2, 2], image="./assets/colors/blue_red_purple.png", args=[0, 130], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   3, 2], image="./assets/colors/red_green_orange_white.png", args=[0, 140], command=self.set_dmx)
        PushButton(select_box, width=90, height=45, grid=[
                   4, 2], image="./assets/colors/all.png", args=[0, 150], command=self.set_dmx)

        Text(self.color_mode, text="Stroboskop",
             color="white", size=16, height=2)
        Slider(self.color_mode, start=0, end=255,
               width="fill", height=60, command=self.set_strobe).text_color = "white"

        Text(self.color_mode, text="Drehung",
             color="white", size=16, height=2)
        Slider(self.color_mode, start=0, end=255,
               width="fill", height=60, command=self.set_turn).text_color = "white"

        # -- widgets for auto-color-switch mode --
        self.change_mode = Box(self.window, layout="auto", width="fill")

        Text(self.change_mode, text="Wechselgeschwindigkeit",
             color="white", size=16, height=2)
        Slider(self.change_mode, start=0, end=255,
               width="fill", height=60, command=self.set_change_speed).text_color = "white"

        Text(self.change_mode, text="Stroboskop",
             color="white", size=16, height=2)
        self.acs_strobe = Slider(self.change_mode, start=0, end=255,
                                 width="fill", height=60, command=self.set_strobe).text_color = "white"

        Text(self.change_mode, text="Drehung",
             color="white", size=16, height=2)
        Slider(self.change_mode, start=0, end=255,
               width="fill", height=60, command=self.set_turn).text_color = "white"

        # -- widgets for Stl mode --
        self.stl_mode = Box(self.window, layout="auto", width="fill")

        Text(self.stl_mode, text="Sound-to-light aktiv",
             color="white", size=16, height=2)

    def open(self):
        self.switch_view('color')
        self.window.show()

    def confirm(self):
        pass

    def cancle(self):
        self.close()

    def set_dmx(self, channel, value):
        self.dmx_values[channel] = value
        set(self.dmx_values[0], self.dmx_values[1],
            self.dmx_values[2], self.dmx_values[3])

        if self.dmx_values[0] == 0 and self.dmx_values[1] == 0 and self.dmx_values[2] == 0 and self.dmx_values[3] == 0:
            self.picture.image = f"{self.path}{self.image}_off.png"
        else:
            self.picture.image = f"{self.path}{self.image}_on.png"

    def set_strobe(self, value):
        self.set_dmx(1, value)

    def set_change_speed(self, value):
        self.set_dmx(2, value)

    def set_turn(self, value):
        self.set_dmx(3, value)

    def switch_view(self, args):
        set(0, 0, 0, 0)
        self.color_mode.hide()
        self.change_mode.hide()
        self.stl_mode.hide()

        if args == 'color':
            self.color_mode.show()
        elif args == 'change':
            self.change_mode.show()
            self.set_dmx(0, 160)
        elif args == 'stl':
            self.stl_mode.show()
            self.set_dmx(0, 230)
