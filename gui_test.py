from tkinter import Tk, RAISED
from tkinter.ttk import Frame, Button, Label, Style


class MainWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.grid()
        self.init_ui()

    def init_ui(self):
        self.parent.title("Papers")
        self.style = Style()
        self.style.theme_use("clam")
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.grid(row=0, column=0)
        label = Label(frame, text="Get Images")
        label.grid(row=0, column=0)
        button = Button(frame, text="Start", command=self.start)
        button.grid(row=1, column=0)
        button = Button(frame, text="Stop", command=self.stop)
        button.grid(row=1, column=1)

    def start(self):
        print("Starting")

    def stop(self):
        print("I can't stop.")


def main():
    root = Tk()
    root.geometry("300x200+300+300")
    app = MainWindow(root)
    app.mainloop()


if __name__ == '__main__':
    main()
