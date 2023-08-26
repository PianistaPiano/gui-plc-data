from tkinter import *

class ViewInit():

    def __init__(self):
        self.root = Tk()
        # Set basic paremeters
        app_width = 1068
        app_height = 876
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        self.root.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
        self.root.title("PLC Data Base")
        self.root.configure(background="black")
        self.root.resizable(False, False)
        # End od basic parameters