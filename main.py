# gpiozero needs rpigpio as native factory in system variables ~/.bashrc
# display is used naming for window

from guizero import App, PushButton
from tile import ToggleTile, MenuTile
from standby import Standby
from home import Home
import time
import threading

app = App(title="bollwagen", bg="black")
path = '/home/pi/bw/assets/img/'

home = Home(app, path)
standby = Standby(app, path)


def main():
    app.tk.attributes("-fullscreen", True)
    app.tk.config(cursor='none')
    home.open()
    standby.open()
    app.display()


if __name__ == '__main__':
    main()
