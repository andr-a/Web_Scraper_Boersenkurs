# import Tkinter module
from tkinter import *
# from tkinter.ttk import *


class App2:
    def __init__(self, main):
        self.listbox = Listbox(main, height=25, width=40)
        self.listbox.grid(column=1, row=1, columnspan=6, rowspan=10, sticky="n")
        self.listbox.insert(END, "Beobachtete Aktien")  # TODO: Platzhalter ersetzen
        # TODO: Rahmen entfernen
        self.frame_data = LabelFrame(main, highlightbackground="black", highlightcolor="black", highlightthickness=1, bd=0)
        self.frame_data.grid(column=8, row=1, columnspan=9, rowspan=7, sticky="n")

        # Inhalt von frame_data mit.grid()
        self.label_stock_name = (Label(self.frame_data, font="None 16 bold", text="Gewählter Aktienname").grid(columnspan=2))
        self.label_short_name = Label(self.frame_data, text="(Kürzel)", bg="red").grid(row=1, columnspan=2)
        self.label_isin = Label(self.frame_data, text="ISIN: DE0000000000", bg="blue").grid(column=0, row=2, sticky="w")
        Label(self.frame_data, text="Aktueller Kurs:", bg="yellow").grid(column=0, row=3, sticky="w")
        Label(self.frame_data, text="Vortragskurs:", bg="orange").grid(column=0, row=4, sticky="w")
        Label(self.frame_data, text="Tageshoch:", bg="violet").grid(column=0, row=5, sticky="w")
        Label(self.frame_data, text="Tagestief:", bg="grey").grid(column=0, row=6, sticky="w")
        Label(self.frame_data, text="Veränderung zum Vortage:", bg="pink").grid(column=0, row=7, sticky="w")

        self.label_wkn = Label(self.frame_data, text="WKN: 012345", bg="green")
        self.label_wkn.grid(column=1, row=2, sticky="e")

        col_count, row_count = self.frame_data.grid_size()
        self.frame_data.grid_columnconfigure(0, minsize=160)
        self.frame_data.grid_columnconfigure(1, minsize=200)

        for row in list(range(row_count)):
            self.frame_data.grid_rowconfigure(row, minsize=40)

        # style_button = Style()
        # style_button.configure("TButton", width=120, height=40)
        button_row = 11

        self.button_add_stock = Button(main, text="Aktie hinzufügen")
        self.button_add_stock.grid(column=1, row=button_row, columnspan=3)
        self.button_remove_stock = Button(main, text="Aktie entfernen")
        self.button_remove_stock.grid(column=4, row=button_row, columnspan=3)
        self.button_start_scraping= Button(main, text="Start Scraping")
        self.button_start_scraping.grid(column=8, row=button_row, columnspan=3)

        self.configure_grid(main)

    def configure_grid(self, grid):
        col_count, row_count = grid.grid_size()
        for col in list(range(col_count)):
            grid.grid_columnconfigure(col, minsize=40)

        for row in list(range(row_count)):
            grid.grid_rowconfigure(row, minsize=40)


root = Tk()
root.geometry("720x540")
root.wm_resizable(False, False)
root.title("Web Scraper")
app = App2(root)
root.mainloop()
