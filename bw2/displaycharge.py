from display import Display
from guizero import PushButton, Text, Box


class DisplayCharge(Display):
    def __init__(self, app, path, image):
        super().__init__(app, path, image, use_cancle_button=True, use_confirm_button=True)

    def generateComponents(self):
        self.top_text = Text(
            self.window, text="Bitte Betrag eingeben", height=3, align="top")
        self.top_text.text_color = "white"
        self.top_text.text_size = self.CONST_FONT_SIZE_GENERAL
        self.current_input = []

        self.numpad = Box(self.window, layout="grid",
                            width="240", align="top")

        buttonsNumpad = []
        buttonsNumpad.append(PushButton(
            self.numpad, command=self.edit_number, args=[0], text="0", grid=[1, 3]))
        buttonsNumpad.append(PushButton(
            self.numpad, command=self.edit_number, args=[1], text="1", grid=[0, 0]))
        buttonsNumpad.append(PushButton(
            self.numpad, command=self.edit_number, args=[2], text="2", grid=[1, 0]))
        buttonsNumpad.append(PushButton(
            self.numpad, command=self.edit_number, args=[3], text="3", grid=[2, 0]))
        buttonsNumpad.append(PushButton(
            self.numpad, command=self.edit_number, args=[4], text="4", grid=[0, 1]))
        buttonsNumpad.append(PushButton(
            self.numpad, command=self.edit_number, args=[5], text="5", grid=[1, 1]))
        buttonsNumpad.append(PushButton(
            self.numpad, command=self.edit_number, args=[6], text="6", grid=[2, 1]))
        buttonsNumpad.append(PushButton(
            self.numpad, command=self.edit_number, args=[7], text="7", grid=[0, 2]))
        buttonsNumpad.append(PushButton(
            self.numpad, command=self.edit_number, args=[8], text="8", grid=[1, 2]))
        buttonsNumpad.append(PushButton(
            self.numpad, command=self.edit_number, args=[9], text="9", grid=[2, 2]))
        buttonsNumpad.append(PushButton(
            self.numpad, command=self.edit_number, args=["<"], text="<", grid=[2, 3]))

        for button in buttonsNumpad:
            button.text_size = self.CONST_FONT_SIZE_GENERAL*2
            button.text_color = "white"
            button.width = 2
            button.height = 1


    def confirm(self):
        pass

    def cancle(self):
        self.reset_numpad()

        self.close()

    def edit_number(self, n):
        if n is "<" and len(self.current_input) > 0:
            self.current_input.pop(0)
        elif n is 0 and len(self.current_input) is 0:
            pass
        elif type(n) is int:
            self.current_input.insert(0, n)

        mystring = ""
        for index, digit in enumerate(self.current_input):
            if index is 2:
                mystring = f"{digit}" + f"." + mystring
            else:
                mystring = f"{digit}" + mystring

        if len(self.current_input) is 0:
            self.top_text.value = f"Bitte Betrag eingeben"
        elif len(self.current_input) is 1:
            self.top_text.value = f"0.0{mystring} €"
        elif len(self.current_input) is 2:
            self.top_text.value = f"0.{mystring} €"
        else:
            self.top_text.value = f"{mystring} €"
    
    def reset_numpad(self):
        self.current_input.clear()
        self.top_text.value = f"Bitte Betrag eingeben"