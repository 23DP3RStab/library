import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
import os


class library(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Library")
        self.resizable(False, False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._set_appearance_mode("dark")
        self.center(self, 800, 600)
        self.iconbitmap("icon.ico")
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both")


    def center(self, window, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width/2) - (width/2))
        y = int((screen_height/2) - (height/2))
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))

    




if __name__ == "__main__":
    app = library()
    app.mainloop()