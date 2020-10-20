from .display import Display
from .cash import Cash
from guizero import PushButton, Text, Box


class PayMethod(Display):
    def __init__(self, app, path, image):
        self.amount = 0
        self.display_cash = Cash(app, path, image)
        super().__init__(app, path, image, use_cancle_button=True, use_confirm_button=False)

    def generateComponents(self):
        top_text = Text(
            self.window, text="Zahlungsmethode auswählen", align="top", height=3, size=self.CONST_FONT_SIZE_GENERAL)
        top_text.text_color = "white"

        cash = PushButton(
            self.window, command=self.proceed_to_payment, width="fill", height=4, text="Bar")
        cash.text_color = "white"

        paypal = PushButton(
            self.window, command=None, width="fill", height=4, text="PayPal", enabled=False)
        paypal.text_color = "white"
        paypal.bg = "blue"

    def open(self, *args):
        self.window.show()
        self.amount = float(args[0])

    def confirm(self):
        pass

    def cancle(self):
        self.close()

    def proceed_to_payment(self):
        self.display_cash.open(self.amount)
