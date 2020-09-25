from guizero import App, PushButton, Slider, Text, Window
import RPi.GPIO as GPIO


class button:
    def __init__(self, index, image, grid, gpio):
        self.index = index
        self.image = image
        self.grid = grid
        self.gpio = gpio


def general_callback(n):
    print('general_callback()', n)
    if GPIO.input(buttons[n].gpio) == 1:
        pushButtons[n].image = buttons[n].image+'_on.png'
        GPIO.output(buttons[n].gpio, GPIO.LOW)
    else:
        pushButtons[n].image = buttons[n].image+'_off.png'
        GPIO.output(buttons[n].gpio, GPIO.HIGH)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
path = '/home/pi/Desktop/bwpy/TouchScreenRelayPanel/'

buttons = []
# index,image,grid,gpio
buttons.append(button(0, 'rear_lights', [0, 0], 40))
buttons.append(button(1, 'front_lights', [1, 0], 38))
buttons.append(button(2, 'water_pump', [2, 0], 36))


app = App(title="BWPY", width=480, height=800, layout="grid", bg="green")

pushButtons = []
for button in buttons:
    GPIO.setup(button.gpio, GPIO.OUT)
    GPIO.output(button.gpio, GPIO.HIGH)
    pushButtons.append(PushButton(app, args=[button.index], command=open_window,
                                  grid=button.grid, align='left', image=path + button.image+'_off.png'))


def main():
    # app.tk.attributes("-fullscreen", True)
    app.tk.config(cursor='none')
    app.display()


if __name__ == '__main__':
    main()
