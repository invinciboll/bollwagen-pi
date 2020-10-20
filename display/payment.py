from .display import Display
from guizero import  Text ,Drawing
from interfaces.rfid import Reader
from interfaces.repository import Database
import threading
import time


class Payment(Display):
    def __init__(self, app, path, image):
        self.stop = False
        self.db = Database("database.db")
        self.rfid = Reader()
        super().__init__(app, path, image, use_cancle_button=True, use_confirm_button=False)

    def generateComponents(self):
        self.total_text = Text(self.window, align="top", text=f"0.00 €")
        self.total_text.text_color = "white"
        self.total_text.text_size = self.CONST_FONT_SIZE_GENERAL*3

        self.instruction_text = Text(
            self.window, text="Bitte Karte auflegen", align="top")
        self.instruction_text.text_color = "white"
        self.instruction_text.text_size = self.CONST_FONT_SIZE_GENERAL

        self.progress_bar = Drawing(
            self.window, align="top", width="fill", visible=True)
    
    def open(self, *args):
        self.total_text.value =f"{args[0]} €"
        self.window.show()
        tr = threading.Thread(target=self.startPaymentProcess, args=(args[0], args[1], args[2]))
        tr.start()
        

    def confirm(self):
        #not needed
        pass

    def cancle(self):
        self.stop = True
        self.close()

    def startPaymentProcess(self, total, drink_sum, hookah_sum):
        self.stop = False
        while (not self.stop):
            sn = self.rfid.getId()    
            if len(sn) > 4 :
                break   

        if not self.stop:
            balance = self.db.getBalance(sn)
            if (total <= balance):
                # payment accepted
                self.db.setBalance(sn, balance-total)
                self.db.insertPurchase(sn, drink_sum, hookah_sum)

                # give response to user
                self.instruction_text.text_color = "green"
                self.instruction_text.value = "Danke!"
                self.cancle_button.hide()
                width = 0
                for _ in range(120):
                    self.progress_bar.rectangle(
                        0, 0, width, 8, color="green")
                    time.sleep(0.016)
                    width += 4
            else:
                self.instruction_text.text_color = "red"
                self.instruction_text.value = "Fehler: zu wenig Guthaben"
                self.cancle_button.hide()
                time.sleep(2)
        else:
            # break from thread
            print("Killing Thread")    
        
        self.reset()


    def reset(self):
        self.close()
        self.progress_bar.clear()
        self.instruction_text.text_color = "white"
        self.instruction_text.value = "Bitte Karte auflegen"
        self.cancle_button.show()
