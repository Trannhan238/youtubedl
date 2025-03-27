from views.main_window import MainWindow
from models.settings import AppSettings
import tkinter as tk

def main():
    root = tk.Tk()
    settings = AppSettings()
    app = MainWindow(root, settings)
    root.mainloop()

if __name__ == "__main__":
    main()