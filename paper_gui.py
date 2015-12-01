from tkinter import Tk, RAISED
from tkinter.ttk import Frame, Button, Label, Style
from packages import WallHandler
from packages import Reddit


class MainWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.grid()
        self.init_ui()
        self.wallhandler = WallHandler()
        self.reddit = Reddit()

    def init_ui(self):
        self.parent.title("Papers")
        self.style = Style()
        self.style.theme_use("clam")
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.grid(row=0, column=0)
        label = Label(frame, text="Change Wallpaper")
        label.grid(row=0, column=0)
        button = Button(frame, text="Change", command=self.change)
        button.grid(row=1, column=0)
        label = Label(frame, text="Fetch Wallpapers")
        label.grid(row=2, column=0)
        button = Button(frame, text="Fetch", command=self.fetch)
        button.grid(row=3, column=0)

    def change(self):
        self.wallhandler.run()

    def fetch(self):
        self.reddit.run()


def main():
    root = Tk()
    root.geometry("300x200+300+300")
    app = MainWindow(root)
    app.mainloop()


if __name__ == '__main__':
    main()
