import sys
import ctypes

from Tkinter import *
import ttk

class Abstrakt(Tk):
    def __init__(self, **kwargs):
        Tk.__init__(self)
        #General routines
        self.overrideredirect(True)
        self._maxified = False
        #self.wm_attributes('-alpha', 0.9)
        #Values for window iconification
        self.GWL_EXSTYLE = -20
        self.WS_EX_APPWINDOW = 0x00040000
        self.WS_EX_TOOLWINDOW = 0x00000080
        self._visibility = 0
        #Icon holder
        self._iconpath = 'Abstrakt.ico'
        #Title holder
        self._Th = kwargs['title'] if kwargs.get('title') else 'Abstrakt'
        #Values for colours
        self._clscolor = kwargs['clscolor'] if kwargs.get('clscolor') else 'red'
        self._maxcolor = kwargs['maxcolor'] if kwargs.get('maxcolor') else 'green'
        self._mincolor = kwargs['mincolor'] if kwargs.get('mincolor') else 'cyan'
        self.wmcolor = kwargs['wmcolor'] if kwargs.get('wmcolor') else '#3A6FFF'
        self.wmcolor2 = kwargs['wmcolor2'] if kwargs.get('wmcolor2') else 'black'
        self.wincolor = kwargs['wincolor'] if kwargs.get('wincolor') else 'black'
        self.sizcolor = kwargs['sizcolor'] if kwargs.get('sizcolor') else 'black'
        #Values for window geometry
        self._width = 200
        self._height = 200
        self._xpos = 0
        self._ypos = 0
        #Offsets for window movement
        self._offsetx = 0
        self._offsety = 0
        #Window manager frame
        self.wmframe = Frame(self, bg = self.wmcolor)
        self.wmframe.pack(side = 'top', fill = X)
        self.wmframe.bind('<1>', self.__clickwin)
        self.wmframe.bind('<B1-Motion>', self.__dragwin)
        self.wmframe.bind("<Map>", self.__wmframe_mapped)
        #Window manager window frame
        self.winframe = Frame(self, bg = self.wincolor)
        self.winframe.pack(side = 'top', fill = BOTH, expand = True)
        #Window manager sizing frame
        self.sizeframe = Frame(self, bg = self.sizcolor)
        self.sizeframe.pack(side = 'bottom', fill = X)
        #Window manager sizegrip
        self.grip = ttk.Sizegrip(self.sizeframe)
        self.grip.pack(side = 'right')
        self.grip.bind("<B1-Motion>", self.__OnResize)
        #Window title
        self.Title = Label(self.wmframe, bg = self.wmcolor, fg = self.wmcolor2, text = self._Th, font = 'Consolas 13 bold')
        self.Title.pack(side = 'left')
        self.Title.bind('<1>', self.__clickwin)
        self.Title.bind('<B1-Motion>', self.__dragwin)
        #Window manager 'buttons'
        #Close
        self.close = Label(self.wmframe, bg = self.wmcolor, fg = self.wmcolor2, text = u'\U0000274C', anchor = 'center', font = 'Calibri 15 bold', width = 3, padx = 3)
        self.close.pack(side = 'right')
        self.close.bind('<1>', self.__cleanexit)
        self.close.bind('<Enter>', self.__clshover)
        self.close.bind('<Leave>', self.__clsunhover)
        #Maximise/Restore
        self.maximise = Label(self.wmframe, bg = self.wmcolor, fg = self.wmcolor2, text = u'\U00002197', anchor = 'center', font = 'Calibri 15 bold', width = 3, padx = 5)
        self.maximise.pack(side = 'right')
        self.maximise.bind('<1>', self.__maxify)
        self.maximise.bind('<Enter>', self.__maxhover)
        self.maximise.bind('<Leave>', self.__maxunhover)
        #Minimise
        self.minimise = Label(self.wmframe, bg = self.wmcolor, fg = self.wmcolor2, text = u'\U00002013', anchor = 'center', font = 'Elephant 15 bold', width = 3)
        self.minimise.pack(side = 'right')
        self.minimise.bind('<1>', self.__minify)
        self.minimise.bind('<Enter>', self.__minhover)
        self.minimise.bind('<Leave>', self.__minunhover)

    def set_geometry(self, width, height, xpos, ypos):
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self.geometry('%dx%d+%d+%d' %(width, height, xpos, ypos))

    def set_icon(self, iconpath):
        self._iconpath = iconpath

    def __dragwin(self,event):
        if self._maxified:
            pass
        else:
            x = self.winfo_pointerx() - self._offsetx
            y = self.winfo_pointery() - self._offsety
            self.geometry('+{x}+{y}'.format(x = x,y = y))
            self._xpos = x
            self._ypos = y

    def __clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def __OnResize(self, event):
        x1 = self.winfo_pointerx()
        y1 = self.winfo_pointery()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        self.geometry("%sx%s" % ((x1-x0), (y1-y0)))
        self._width = x1-x0
        self._height = y1-y0
        if self._maxified:
            self.maximise.config(text = u'\U00002197')
        self._maxified = False
        
    def __clshover(self, event):
        event.widget.config(bg = self._clscolor)

    def __clsunhover(self, event):
        event.widget.config(bg = self.wmcolor)

    def __maxhover(self, event):
        event.widget.config(bg = self._maxcolor)

    def __maxunhover(self, event):
        event.widget.config(bg = self.wmcolor)

    def __minhover(self, event):
        event.widget.config(bg = self._mincolor)

    def __minunhover(self, event):
        event.widget.config(bg = self.wmcolor)

    def __cleanexit(self, event):
        self.destroy()
        sys.exit()

    def __minify(self, event):
        self.update_idletasks()
        self.state('withdrawn')
        self.overrideredirect(False)
        self.title(self._Th)
        self.iconbitmap(self._iconpath)
        self.state('iconic')
        self._visibility = 0

    def __wmframe_mapped(self, event):
        #print(self, event)
        self.update_idletasks()
        self.overrideredirect(True)
        self.state('normal')
        if self._visibility == 0:
            self._setx()
        else:
            pass

    def __maxify(self, event):
        if self._maxified:
            self.geometry('%dx%d+%d+%d' %(self._width, self._height, self._xpos, self._ypos))
            self.maximise.config(text = u'\U00002197')
            self._maxified = False
            #print self._maxified
        else:
            w = self.winfo_screenwidth()
            h = self.winfo_screenheight()
            x = 0
            y = 0
            self.geometry('%dx%d+%d+%d' % (w, h, x, y))
            self.maximise.config(text = u'\U00002199')
            self._maxified = True
            #print self._maxified

    def __setvisiblex(self):
        #Set our native icon & title
        self.wm_title(self._Th)
        self.wm_iconbitmap(self._iconpath)
        #Force iconification
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, self.GWL_EXSTYLE)
        style = style & ~self.WS_EX_TOOLWINDOW
        style = style | self.WS_EX_APPWINDOW
        res = ctypes.windll.user32.SetWindowLongW(hwnd, self.GWL_EXSTYLE, style)
        self.wm_withdraw()
        self.after(1, lambda: self.wm_deiconify())
        self._visibility = 1

    def _setx(self):
        self.after(1, lambda: self.__setvisiblex())

def test():
    my_gui = Abstrakt()
    my_gui.set_geometry(800, 500, 300, 150)
    #Use 'Abstrakt().winframe' as root container to place widgets in the window
    label = Label(my_gui.winframe, text = 'Hello World!', bg = my_gui.wincolor, fg = 'white')
    label.pack()
    my_gui.mainloop()

if __name__ == '__main__':
    test()
