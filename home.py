from guizero import Window
from tile import ToggleTile, MenuTile


class Home():
    CONST_TEXT_COLOR = "white"
    CONST_FONT_SIZE_GENERAL = 16

    def __init__(self, app, path):
        self.window = Window(app, title="home", bg="black",
                             layout="grid", visible=False)
        self.window.tk.attributes("-fullscreen", True)
        self.window.tk.config(cursor='none')
        tiles = []
        tiles.append(ToggleTile(self.window, path, 'sign', [0, 0], 7))
        tiles.append(ToggleTile(self.window, path, 'outside', [1, 0], 1))
        tiles.append(ToggleTile(self.window, path, 'shots', [0, 1], 12))
        tiles.append(MenuTile(self.window, path, 'ambient',
                              [1, 1], [13, 19, 26], 'Led'))
        tiles.append(MenuTile(self.window, path,
                              'effect', [0, 2], [], 'Effect'))
        tiles.append(MenuTile(self.window, path, 'logo',
                              [1, 2], [16, 20, 21], 'Led'))
        tiles.append(MenuTile(self.window, path, 'vent', [0, 3], [23], 'Vent'))
        tiles.append(MenuTile(self.window, path,
                              'money', [1, 3], [], 'MoneyMenu'))

    def open(self, *args):
        self.window.show()

    def close(self, *args):
        self.window.hide()
