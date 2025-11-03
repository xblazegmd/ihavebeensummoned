import _tkinter
from gui import App

def main() -> None:
    try:
        root = App()
        root.mainloop()
    except _tkinter.TclError as e:
        if "application has been destroyed" not in str(e):
            raise
        else:
            print("Tkinter's mad at you rn")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("[-] Exiting...")