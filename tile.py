from abc import ABC, abstractmethod
from gpiozero import LED
from guizero import PushButton
from displayledcontrol import DisplayLedControl
from displaymoneymenu import DisplayMoneyMenu
from displayvent import DisplayVent

class Tile:
    def __init__(self, app, path, image, grid, command):
        self.image = image
        self.path = path
        self.button = PushButton(app, command=command,
                                 grid=grid, align='left', image=f"{path}{image}_off.png")

    def toggle_image(self, active):
        if active:
            self.button.image = f"{self.path}{self.image}_on.png"
        else:
            self.button.image = f"{self.path}{self.image}_off.png"



class ToggleTile(Tile):
    def __init__(self, app, path, image, grid, gpio):
        self.device = LED(gpio)
        super().__init__(app, path, image, grid, self.__toggle)

    def __toggle(self):
        self.device.toggle()
        self.toggle_image(self.device.is_active)



class MenuTile(Tile):
    def __init__(self, app, path, image, grid, gpio_list, menu_type, ):
        self.__init_display(app, path, image, gpio_list, menu_type)
        super().__init__(app, path, image, grid, self.display.open)

    def __init_display(self, app, path, image ,gpio_list, menu_type): 
        if menu_type is 'Led':
            self.display = DisplayLedControl(app, path, image, gpio_list[0], gpio_list[1], gpio_list[2])
        elif menu_type is 'MoneyMenu':
            self.display = DisplayMoneyMenu(app, path, image)
        elif menu_type is 'Vent':
            self.display = DisplayVent(app, path, image, gpio_list[0])
