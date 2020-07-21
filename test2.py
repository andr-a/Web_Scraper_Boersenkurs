# import Tkinter module
from tkinter import *
from tkinter import font

# # create window from the Tkinter module
# window = Tk()
#
# # size of the window
# window.geometry("800x600")
#
# # window title
# window.title("Test")
#
# # loops the window to keep it open
# window.mainloop()


# class TestApp(Tk.Frame):
#     def __int__(self, main=None):
#         super().__init__(main)
#         self.main

class App1:
    def __init__(self, main):
        frame = Frame(main)
        frame.pack()

        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)
        self.slogan = Button(frame, text="Hello", command=self.write_slogan)
        self.slogan.pack(side=LEFT)

    def write_slogan(self):
        print("Tkinter is easy to use!")


root = Tk()
app = App1(root)
root.mainloop()
