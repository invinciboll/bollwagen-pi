# gpiozero needs rpigpio as native factory in system variables ~/.bashrc
# display is used naming for window

from guizero import App
from tile import ToggleTile, MenuTile
from display.home import Home_Display

app = App(title="bollwagen", bg="black", layout="grid")
path = '/home/pi/Desktop/bw/assets/img/'

tiles = []
tiles.append(ToggleTile(app, path, 'sign', [0, 0], 7))
tiles.append(ToggleTile(app, path, 'outside', [1, 0], 1))
tiles.append(ToggleTile(app, path, 'shots', [0, 1], 12))
tiles.append(MenuTile(app, path, 'ambient', [1, 1], [13, 19, 26], 'Led'))
#tiles.append(mTile('effect', [0, 2]))
tiles.append(MenuTile(app, path, 'logo', [1, 2], [16, 20, 21], 'Led'))
tiles.append(MenuTile(app, path, 'vent', [0, 3], [23], 'Vent'))
tiles.append(MenuTile(app, path, 'money', [1, 3], [], 'MoneyMenu'))
tiles.append(MenuTile(app, path, 'bollwagen', [0, 2], [18], 'Bollwagen'))


def main():
    app.tk.attributes("-fullscreen", True)
    app.tk.config(cursor='none')
    app.display()


if __name__ == '__main__':
    main()
