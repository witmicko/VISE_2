from tkinter import Toplevel, Label, Entry, Button
import easygui

class LeftClickDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        Label(top, text="Value").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        print("value is", self.e.get())
        self.top.destroy()

class RightClickDialog:
    easygui.msgbox('This is a basic message box.', 'Title Goes Here')

