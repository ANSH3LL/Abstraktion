from Tkinter import *
from PIL import Image, ImageTk

class Pantry(object):
    #Tkinter-based password input field with show/hide capabilities...just pack/grid/place it like a normal widget
    def __init__(self, parent, **kwargs):
        self.im1 = Image.open('img/eye_open.png')
        self.im2 = Image.open('img/eye_closed.png')
        self.photod = ImageTk.PhotoImage(self.im1)
        self.photoo = ImageTk.PhotoImage(self.im2)

        self.currimg = True #open
        self.container = Frame(parent)
        self.field = Entry(self.container, bg = '#f8f8f8', font = 'Consolas 12 bold', show = u'\u2022', relief = 'flat', width = 40)
        self.button = Label(self.container, image = self.photod)

        self.button.bind('<1>', self.morph)
        self.field.pack(side = 'left')
        self.button.pack(side = 'left')

    def morph(self, event = None):
        if self.currimg:
            event.widget.config(image = self.photoo)
            self.field.config(font = 'Consolas 12')
            self.unhide()
            self.currimg = False
        else:
            event.widget.config(image = self.photod)
            self.field.config(font = 'Consolas 12 bold')
            self.rehide()
            self.currimg = True

    def unhide(self):
        self.field.config(show = '')

    def rehide(self):
        self.field.config(show = u'\u2022')

    def getpass(self):
        return self.field.get()

    def pack(self, *args, **kwargs):
        self.container.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.container.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.container.place(*args, **kwargs)

if __name__ == '__main__':
    root = Tk()
    p = Pantry(root)
    p.pack()
    root.mainloop()
