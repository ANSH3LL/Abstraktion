from Tkinter import *

class AbstraktThought():
    #Tkinter-based tooltips...supports customization and basically all widgets
    def __init__(self, **kwargs):
        self.widget = kwargs["widget"]
        self.text = kwargs["text"] if kwargs.get("text") else "Your text here"
        self.tiptype = kwargs["tiptype"] if kwargs.get("tiptype") else "normal"
        self.fcolor = kwargs["fcolor"] if kwargs.get("fcolor") else "#f5f5f5"#foreground color
        self.bcolor = kwargs["bcolor"] if kwargs.get("bcolor") else "#404040"#background color
        self.items = []
        self.delay = 0
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self._id1 = self.widget.bind("<Enter>", self.enter)
        self._id2 = self.widget.bind("<Leave>", self.leave)
        self._id3 = self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event = None):
        self.schedule()

    def leave(self, event = None):
        self.unschedule()
        self.killtip()

    def set_delay(self, delay = 500):
        self.delay = delay

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.showtip)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def additem(self, item):
        self.items.append(item)

    def showtip(self):
        if self.tipwindow:
            return
        # The tip window must be completely outside the button
        # otherwise when the mouse enters the tip window we get
        # a leave event and it disappears, and then we get an enter
        # event and it reappears, and so on forever :-(
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 1
        self.tipwindow = Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(True)
        self.tipwindow.wm_geometry("+%d+%d" % (x, y))
        if self.tiptype == "normal":
            self.showcontents1()
        elif self.tiptype == "listed":
            self.showcontents2()
        else:
            raise TypeError, "Unknown type, MUST be normal or listed"

    def showcontents1(self):
        #Normal type thought
        label = Label(self.tipwindow, text = self.text, font = "Courier 10", fg = self.fcolor, bg = self.bcolor, justify = "left")
        label.pack()

    def showcontents2(self):
        #Listed type thought
        listbox = Listbox(self.tipwindow, font = "Courier 10", fg = self.fcolor, bg = self.bcolor, highlightthickness = 0, borderwidth = 0)
        listbox.pack()
        for item in self.items:
            listbox.insert("end", item)

    def killtip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()  

def test():
    root = Tk()
    root.title("ToolTip Test")
    root.geometry("700x500+300+100")
    label = Label(root, text = "Place your mouse over buttons:")
    button1 = Label(root, text = "Button 1")
    button2 = Label(root, text = "Button 2")
    label.pack()
    button1.pack()
    button2.pack()
    a = AbstraktThought(widget = button1, bcolor = '#ffffe0', fcolor = '#000000', text = "This is tooltip text for button1.\nHave fun testing AbstraktThoughts...")
    a.set_delay()
    b = AbstraktThought(widget = button2, tiptype = "listed")
    b.set_delay()
    b.additem("1.Line One")
    b.additem("2.Line Two")
    b.additem("3.Line Three")
    b.additem("4.Line Four")
    b.additem("5.Line Five")
    b.additem("6.Line Six")
    b.additem("7.Line Seven")
    b.additem("8.Line Eight")
    b.additem("9.Line Nine")
    b.additem("10.Line Ten")
    root.mainloop()

if __name__ == '__main__':
    test()
