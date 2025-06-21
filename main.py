'''
Main file for the project
'''
# import sys
# import traceback
# import tkinter as tk
# from tkinter import messagebox
from prizma_to_brapa.views.interface import PrizmaToBrapaGUI


def main():
    """
    Entry point for the application.

    Initializes the Tkinter event loop with an instance of MainWindow.
    """
    app = PrizmaToBrapaGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
