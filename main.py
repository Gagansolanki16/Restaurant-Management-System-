from tkinter import Tk
from login import LoginPage

def main():
    win = Tk()
    app = LoginPage(win)
    win.mainloop()

if __name__ == "__main__":
    main()
