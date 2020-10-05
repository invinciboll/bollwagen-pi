from abc import ABC, abstractmethod
from guizero import Window, Picture, PushButton

class Display:
    CONST_TEXT_COLOR = "white"

    def __init__(self, app, image, use_cancle_button, use_confirm_button):
        self.window = Window(app, title=image, bg="black", visible=False)
        self.window.tk.attributes("-fullscreen", True)
        self.window.tk.config(cursor='none')

        Picture(self.window, image=image + '_off.png', align="top")
        
        if use_cancle_button:
            cancle_button = PushButton(
                self.window, command=self.__cancle, text="Zurück", height=4, width="fill", align="bottom")
            cancle_button.text_color = self.CONST_TEXT_COLOR
            
        if use_confirm_button:
            confirm_button = PushButton(
                self.window, command=self.__confirm, text="Bestätigen", height=4, width="fill", align="bottom")
            confirm_button.text_color = self.CONST_TEXT_COLOR
     
    def open(self):
        self.window.show()

    def close(self):
        self.window.hide()

    def __generateComponents(self):
        pass

    def __confirm(self):
        pass
    
    def __cancle(self):
        self.close()

