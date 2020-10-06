from display import Display
from guizero import Box, PushButton, Text
from displaypayment import DisplayPayment

class DisplayShoppingCard(Display):
    CONST_HOOKAH_PRICE = 1.50
    CONST_DRINK_PRICE = 1.00
    def __init__(self, app, path, image):
        self.hookah_sum = 0
        self.drink_sum = 0
        self.total = 0
        self.display_payment = DisplayPayment(app, path, image)
        super().__init__(app, path, image, use_cancle_button=True, use_confirm_button=True)

    def generateComponents(self):
        # ---Box Layout---------------------------------------------------------------------------------------------------------------------
        master_box = Box(self.window, width="fill",align="top")
        
        # ---Plus buttons
        button_box_plus = Box(master_box, align="right", layout="grid")
        button_plus_drink = PushButton(
            button_box_plus, command=self.__edit_consumable, args=['+', 'drink'], width=4, height=2, text="+", grid=[0, 0])
        button_plus_drink.text_color = self.CONST_TEXT_COLOR
        button_plus_drink.text_size = self.CONST_FONT_SIZE_GENERAL

        button_plus_hookah = PushButton(
            button_box_plus, command=self.__edit_consumable, args=['+', 'hookah'], width=4, height=2, text="+", grid=[0, 1])
        button_plus_hookah.text_color = self.CONST_TEXT_COLOR
        button_plus_hookah.text_size = self.CONST_FONT_SIZE_GENERAL
        
        # ---Sum labels
        sum_box = Box(master_box, align="right", layout="grid")
        self.drink_sum_label = Text(sum_box, text=f"0", grid=[0, 0], color="white", width=4, height=3)
        self.drink_sum_label.text_size = self.CONST_FONT_SIZE_GENERAL
        
        self.hookah_sum_label = Text(sum_box,text=f"0", grid=[0, 1], color="white", width=4, height=3)
        self.hookah_sum_label.text_size = self.CONST_FONT_SIZE_GENERAL

        # ---Descriptive row labels
        labelBox = Box(master_box, align="left", layout="grid")
        Text(labelBox, text="Getränke", grid=[0, 0], color="white", align="left", height=3, size=self.CONST_FONT_SIZE_GENERAL)
        Text(labelBox, text="Shisha-Köpfe", grid=[0, 1], color="white", align="left", height=3, size=self.CONST_FONT_SIZE_GENERAL)

        # ---Minus Buttons
        button_box_minus = Box(master_box, align="right", layout="grid")
        button_minus_drink = PushButton(
            button_box_minus, command=self.__edit_consumable, args=['-', 'drink'], width=4, height=2, text="-", grid=[0, 0])
        button_minus_drink.text_color = self.CONST_TEXT_COLOR
        button_minus_drink.text_size = self.CONST_FONT_SIZE_GENERAL

        button_minus_hookah = PushButton(
            button_box_minus, command=self.__edit_consumable, args=['-', 'hookah'], width=4, height=2, text="-", grid=[0, 1])
        button_minus_hookah.text_color = self.CONST_TEXT_COLOR
        button_minus_hookah.text_size = self.CONST_FONT_SIZE_GENERAL

        # ---Total section
        total_box = Box(self.window, width="fill", align="top")
        Text(total_box, text="Total:", color="white", align="left", width=4, height=3, size=self.CONST_FONT_SIZE_GENERAL)
        self.total_label = Text(total_box, text=f"0 €", color="white", align="right", width=6, height=3, size=self.CONST_FONT_SIZE_GENERAL)   

    def confirm(self, ):
        self.display_payment.open(self.total, self.drink_sum, self.hookah_sum)

    def cancle(self):
        self.__reset_shopping_card()
        self.close()

    def __edit_consumable(self, operation, consumable_type):
        if operation is "+":
            if consumable_type is "drink":
                self.drink_sum += 1
            elif consumable_type is "hookah":
                self.hookah_sum += 1

        elif operation is "-":
            if consumable_type is "drink" and self.drink_sum > 0:
                self.drink_sum -= 1
            elif consumable_type is "hookah" and self.hookah_sum > 0:
                self.hookah_sum -= 1

        self.__update_gui()  

    def __update_gui(self):
        self.drink_sum_label.value = f"{self.drink_sum}"
        self.hookah_sum_label.value = f"{self.hookah_sum}"
        self.total = self.drink_sum * self.CONST_DRINK_PRICE + self.hookah_sum * self.CONST_HOOKAH_PRICE
        self.total_label.value = f"{self.total} €"

    def __reset_shopping_card(self):
        self.drink_sum = 0
        self.hookah_sum = 0
        self.__update_gui()
