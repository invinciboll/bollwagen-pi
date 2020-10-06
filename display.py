from abc import ABC, abstractmethod
from guizero import Window, Picture, PushButton

class Display(ABC):
    CONST_TEXT_COLOR = "white"
    CONST_FONT_SIZE_GENERAL = 16

    def __init__(self, app, path, image, use_cancle_button, use_confirm_button):
        self.window = Window(app, title=image, bg="black", visible=False)
        self.window.tk.attributes("-fullscreen", True)
        self.window.tk.config(cursor='none')

        self.picture = Picture(self.window, image=f"{path}{image}_off.png", align="top")
        
        self.generateComponents()

        if use_cancle_button:
            self.cancle_button = PushButton(
                self.window, command=self.cancle, text="Zurück", height=4, width="fill", align="bottom")
            self.cancle_button.text_color = self.CONST_TEXT_COLOR
        else:
            self.cancle_button = None
            
        if use_confirm_button:
            self.confirm_button = PushButton(
                self.window, command=self.confirm, text="Bestätigen", height=4, width="fill", align="bottom")
            self.confirm_button.text_color = self.CONST_TEXT_COLOR
        else: 
            self.confirm_button = None
     
    def open(self, *args):
        self.window.show()

    def close(self, *args):
        self.window.hide()

    @abstractmethod
    def generateComponents(self):
        pass
    
    @abstractmethod
    def confirm(self):
        pass
    
    @abstractmethod
    def cancle(self):
        pass

