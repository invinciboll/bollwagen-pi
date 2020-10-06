# gpiozero needs rpigpio as native factory in system variables ~/.bashrc
# display is used naming for window

from guizero import App
from tile import ToggleTile, MenuTile

app = App(title="bollwagen", bg="black", layout="grid")
path = '/home/pi/Desktop/bw/'


tiles = []
tiles.append(ToggleTile(app, path, 'sign', [0, 0], 14))
tiles.append(ToggleTile(app, path, 'outside', [1, 0], 15))
tiles.append(ToggleTile(app, path, 'shots', [0, 1], 16))
tiles.append(MenuTile(app, path, 'ambient', [1, 1], [3,4,17], 'Led'))
#tiles.append(mTile('effect', [0, 2]))
tiles.append(MenuTile(app, path, 'logo', [1, 2], [18,23,24], 'Led'))
tiles.append(MenuTile(app, path, 'vent', [0, 3], [12], 'Vent'))
tiles.append(MenuTile(app, path,'money', [1, 3],[], 'MoneyMenu'))

def main():
    app.tk.attributes("-fullscreen", True)
    app.tk.config(cursor='none')
    app.display()


if __name__ == '__main__':
    main()
