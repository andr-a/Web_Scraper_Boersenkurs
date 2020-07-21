# from tkinter import *  # in class_module importiert
# from tkinter import messagebox  # in module2 importiert
# from tkinter.ttk import *  # in class_module importiert
# from class_module import *  # in scraper.py importiert
from threading import *
from database import *
from scraper import *
from module2 import *

# Zum Starten des Programms ausfürhen!


class App:
    def __init__(self, parent):
        self.thread = None

        self.main = Frame(parent)
        self.main.pack()
        self.listbox = Listbox(self.main, height=25, width=36)
        self.listbox.bind("<<ListboxSelect>>", self.listbox_onselect)
        self.listbox.grid(column=1, row=1, columnspan=6, rowspan=10, sticky="n")
        self.listbox.insert(END, "Beobachtete Aktien")

        self.frame_data = Frame(self.main)
        self.frame_data.grid(column=8, row=1, columnspan=9, rowspan=8, sticky="n")

        # Inhalt von frame_data mit.grid()
        self.label_stock_name = Label(self.frame_data, font="None 16 bold", text="Aktie")
        self.label_stock_name.grid(columnspan=2)
        self.label_isin = Label(self.frame_data, text="ISIN:")
        self.label_isin.grid(column=0, row=1, sticky="sw")
        self.label_short_name = Label(self.frame_data, text="")
        self.label_short_name.grid(row=2, sticky="nw")
        Label(self.frame_data, text="Letzter Kurs:").grid(column=0, row=3, sticky="w")
        Label(self.frame_data, text="Tagestief:").grid(column=0, row=4, sticky="w")
        Label(self.frame_data, text="Tageshoch:").grid(column=0, row=5, sticky="w")
        Label(self.frame_data, text="Vortragskurs:").grid(column=0, row=6, sticky="w")
        Label(self.frame_data, text="Veränderung zum Vortag:").grid(column=0, row=7, sticky="w")

        self.label_wkn = Label(self.frame_data, text="WKN:")
        self.label_wkn.grid(column=1, row=1, sticky="se")
        self.label_time = Label(self.frame_data, text="")
        self.label_time.grid(column=1, row=2, sticky="ne")
        self.label_current_price = Label(self.frame_data)
        self.label_current_price.grid(column=1, row=3, sticky="e")
        self.label_low = Label(self.frame_data)
        self.label_low.grid(column=1, row=4, sticky="e")
        self.label_high = Label(self.frame_data)
        self.label_high.grid(column=1, row=5, sticky="e")
        self.label_prev_day = Label(self.frame_data)
        self.label_prev_day.grid(column=1, row=6, sticky="e")
        self.label_change = Label(self.frame_data)
        self.label_change.grid(column=1, row=7, sticky="e")

        col_count, row_count = self.frame_data.grid_size()
        self.frame_data.grid_columnconfigure(0, minsize=160)
        self.frame_data.grid_columnconfigure(1, minsize=200)

        for row in list(range(row_count)):
            self.frame_data.grid_rowconfigure(row, minsize=30)

        # Buttons
        self.button_add_stock = StyledButton(self.main, text="Aktie hinzufügen", command=self.add_stock_button)
        self.button_add_stock.grid(column=1, row=BUTTON_ROW, columnspan=3)
        self.button_remove_stock = StyledButton(self.main, text="Aktie entfernen", command=self.remove_stock)
        self.button_remove_stock.grid(column=4, row=BUTTON_ROW, columnspan=3)
        self.button_start_scraping = StyledButton(self.main, text="Start Scraping", command=self.start_scraping)
        self.button_start_scraping.grid(column=8, row=BUTTON_ROW, columnspan=3)
        self.button_stop_scraping = StyledButton(self.main, text="Stop Scraping", command=self.stop_scraping)
        self.button_stop_scraping.grid(column=11, row=BUTTON_ROW, columnspan=3)
        self.button_exit = StyledButton(self.main, text="Beenden", command=self.exit_app) \
            .grid(column=14, row=BUTTON_ROW, columnspan=3)

        # Combobox
        self.label_interval = Label(self.main, text="Zeitintervall (min):") \
            .grid(column=5, row=BUTTON_ROW - 1, columnspan=3, sticky="e")
        self.interval_list = [10, 20, 30, 45, 60, 90, 120]
        self.combobox_interval = StyledCombobox(self.main, values=self.interval_list)
        self.combobox_interval.grid(column=8, row=BUTTON_ROW - 1, columnspan=3)

        self.configure_grid(self.main)
        self.populate_listbox()

    # Einrichten eines Grids mit festen Höhen und Breiten (40x40)
    def configure_grid(self, grid):
        Frame(self.main).grid(column=17, row=0)  # Damit Spalte 17 im Grid entsteht
        col_count, row_count = grid.grid_size()
        for col in list(range(col_count)):
            grid.grid_columnconfigure(col, minsize=40, uniform="cells")

        for row in list(range(row_count)):
            grid.grid_rowconfigure(row, minsize=40, uniform="cells")

    def exit_app(self):
        popup = messagebox.askquestion("Programm beenden", "Programm wirklich schließen und Scraping beenden?\n\n"
                                                           "Scraping wird dadurch beendet.", icon="question")
        if popup == "yes":
            self.stop_scraping()
            db.close_db()  # Datanbankverbindung wird beim Programmende gechlossen
            root.destroy()

    def remove_stock(self):
        if self.listbox.curselection():
            # Zweifache Nachfrage
            popup1 = messagebox.askquestion("Aktie entfernen", "Aktie wirklich aus dem Web Scraper entfernen?",
                                            icon="question")
            if popup1 == "yes":
                popup2 = messagebox.askquestion("Aktie entfernen", "Wollen Sie wirklich alle gespeicherten Daten für "
                                                                   "diese Aktie löschen?\n\nDieser Vorgang kann nicht "
                                                                   "rückgängig gemacht werden.", icon="warning")
                if popup2 == "yes":
                    selected_stock = next(x for x in stock_list if x.get_long_name() == self.listbox
                                          .get(self.listbox.curselection()[0]))
                    db.remove_stock(selected_stock)
                    self.populate_listbox()

    @staticmethod
    def add_stock_button():
        AddStock()

    def start_scraping(self):
        if check_day_time():
            self.disable_buttons()
            delay = int(self.combobox_interval.get())
            self.thread = ScraperThread(datetime.datetime.now(), delay * 60, scrape)
            self.thread.daemon = True  # Thread wird mit dem Hauptprogramm beeendet
            self.thread.start()
        else:
            messagebox.showerror("Außerhalb der Handelszeiten",
                                 "Die Handelszeiten sind Montag - Freitag 08:00 - 20:00")

    def stop_scraping(self):
        if self.thread:
            self.thread.done()
            self.enable_buttons()

    def disable_buttons(self):
        self.button_add_stock.disable()
        self.button_remove_stock.disable()
        self.combobox_interval.disable()

    def enable_buttons(self):
        self.button_add_stock.enable()
        self.button_remove_stock.enable()
        self.combobox_interval.enable()

    def populate_listbox(self):
        global stock_list
        stock_list = db.get_stock()
        self.listbox.delete(0, END)
        if stock_list:
            for stock in stock_list:
                self.listbox.insert(END, stock.get_long_name())
            self.listbox.select_set(0)  # Erstes Element standardmäßig ausgewählt
            self.listbox.event_generate("<<ListboxSelect>>")

    def listbox_onselect(self, evt):
        global share_price_list
        global low_high_close_list
        w = evt.widget
        style_label_red = Style()
        style_label_red.configure("Red.TLabel", foreground="red")
        style_label_green = Style()
        style_label_green.configure("Green.TLabel", foreground="green")

        if w.curselection():
            selected_stock = next(x for x in stock_list if x.get_long_name() == w.get(w.curselection()[0]))
            self.label_stock_name.config(text=selected_stock.get_long_name())
            self.label_short_name.config(text=selected_stock.get_short_name())
            self.label_isin.config(text="ISIN: {}".format(selected_stock.get_isin()))
            self.label_wkn.config(text="WKN: {}".format(selected_stock.get_wkn()))

            share_price_list = db.get_share_price()
            if any(x.get_isin() == selected_stock.get_isin() for x in share_price_list):
                stock_price = next(x for x in share_price_list if x.get_isin() == selected_stock.get_isin())
            else:
                stock_price = SharePrice("", selected_stock.get_isin(), "")  # Noch nichts gescraped -> leere Werte
            self.label_time.config(text=stock_price.get_time())
            self.label_current_price.config(text=stock_price.get_price())

            low_high_close_list = db.get_low_high_close()
            if any(x.get_isin() == selected_stock.get_isin() for x in low_high_close_list):
                low_high_close = next(x for x in low_high_close_list if x.get_isin() == selected_stock.get_isin())
            else:
                low_high_close = LowHighClose("", selected_stock.get_isin(), "", "", "")  # Noch nichts gescraped -> leere Werte
            self.label_low.config(text=low_high_close.get_low())
            self.label_high.config(text=low_high_close.get_high())
            self.label_prev_day.config(text=low_high_close.get_close())

            # Veränderung wird nur berechnet, wenn stock_price und low_high_close nicht leer sind
            if stock_price.get_time() != "" and low_high_close.get_date() != "":
                change = (stock_price.get_price() / low_high_close.get_close()) - 1
                if change < 0:
                    self.label_change.config(style="Red.TLabel", text="{:.03%}".format(change))
                elif change > 0:
                    self.label_change.config(style="Green.TLabel", text="{:.03%}".format(change))
                else:
                    self.label_change.config(text="{:.03%}".format(change))
            else:
                self.label_change.config(text="")


# Popup Fenster um eine Aktie hinzuzufügen
class AddStock:
    def __init__(self):
        self.popup = Toplevel()
        self.popup.geometry("280x120")
        self.popup.resizable(False, False)
        self.popup.attributes("-toolwindow", 1)  # entfernt Minimize/Maximize
        self.popup.title("Aktie hinzufügen")
        self.popup.grab_set()  # Macht alle anderen Fenster unnutzbar

        Label(self.popup, text="Aktie hinzufügen", font="None 9 bold").grid(columnspan=2)
        Label(self.popup, text="ISIN:").grid(row=1, padx=48, sticky="w")
        self.stock_input = Entry(self.popup)
        self.stock_input.grid(row=1, columnspan=2, padx=0, pady=8)

        StyledButton(self.popup, text="Hinzufügen", command=self.add_stock).grid(column=0, row=2, pady=8)
        StyledButton(self.popup, text="Abbrechen", command=self.popup.destroy).grid(column=1, row=2)

        for col in range(2):
            self.popup.grid_columnconfigure(col, minsize=140)

    def add_stock(self):
        isin = self.stock_input.get()
        if check_isin_length(isin):
            scraper = Scraper(isin)
            stock = scraper.get_stock()
            db.write_stock(stock)
            app.populate_listbox()
            self.popup.destroy()


# Paralelisierung, Hauptfenster verwendbar während Scraping läuft
class ScraperThread(Thread):
    def __init__(self, start_time, delay, command):  # Mit Übergabe einer Methode, die wiederholt werden soll
        super().__init__()
        self.delay = delay
        self.is_done = False
        self.action = command
        self.start_time = start_time

    def done(self):
        self.is_done = True

    def run(self):
        while not self.is_done and check_day_time():
            self.action()

            # Timer bis zum nächsten Durchlauf
            while datetime.datetime.now() <= self.start_time + datetime.timedelta(seconds=self.delay):
                waiting = self.start_time - datetime.datetime.now() + datetime.timedelta(seconds=self.delay)
                print("\rWaiting: ", str(waiting).split(".")[0], end="")  # Countdown in der Console zu Testzwecken
                time.sleep(1)
        app.enable_buttons()


def scrape():
    for stock in stock_list:
        scraper = Scraper(stock.get_isin())
        new_share_price = scraper.get_share_price()
        db.write_share_price(new_share_price)
        new_low_high_close = scraper.get_low_high_close()
        db.write_low_high_close(new_low_high_close)
        del scraper


db = Database()
stock_list = []
share_price_list = []
low_high_close_list = []
BUTTON_ROW = 12  # Konstante, für nachträglich einfacheres Anpassen des GUI

# Erstellen des Hauptfensterns
root = Tk()
root.geometry("720x540")
root.wm_resizable(False, False)
root.title("Web Scraper")

app = App(root)
root.protocol("WM_DELETE_WINDOW", app.exit_app)  # Standardfunktionalität des "X"-Buttons ändern
root.mainloop()
