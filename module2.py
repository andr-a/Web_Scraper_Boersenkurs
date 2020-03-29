from tkinter import messagebox
import datetime


# Modul-Methoden
def check_isin_length(isin):
    if len(isin) == 12:
        return True
    else:
        messagebox.showerror("Falsche ISIN Länge", "Die ISIN muss 12 Zeichen haben.")
        return False


# Überprüfen ob innerhalb der Handelszeiten
def check_day_time():
    d = datetime.datetime.now()
    if d.isoweekday() in range(1, 6) and d.hour in range(8, 20):
        return True
    else:
        return False
