from tkinter import *
from tkinter.ttk import *


class Stock:
    def __init__(self, isin="", wkn="", long_name="", short_name=""):
        self._isin = isin
        self._wkn = wkn
        self._long_name = long_name
        self._short_name = short_name

    # Override der "ToString"-Funktion zur Ausgabe in der Console für Testzwecke
    def __str__(self) -> str:
        return "{}, {}, {}, {}".format(self._isin, self._wkn, self._long_name, self._short_name)

    def get_isin(self):
        return self._isin

    def get_wkn(self):
        return self._wkn

    def get_long_name(self):
        return self._long_name

    def get_short_name(self):
        return self._short_name


class LowHighClose:
    def __init__(self, date, isin, low, high, close):
        self._date = date
        self._isin = isin
        self._low = low
        self._high = high
        self._close = close

    def __str__(self) -> str:
        return "{}, {}, {}, {}, {}".format(self._date, self._isin, self._low, self._high, self._close)

    def get_date(self):
        return self._date

    def get_isin(self):
        return self._isin

    def get_low(self):
        return self._low

    def get_high(self):
        return self._high

    def get_close(self):
        return self._close


class SharePrice:
    def __init__(self, time, isin, price):
        self._time = time
        self._isin = isin
        self._price = price

    def __str__(self) -> str:
        return "{}, {}, {}".format(self._time, self._isin, self._price)

    def get_time(self):
        return self._time

    def get_isin(self):
        return self._isin

    def get_price(self):
        return self._price


class StyledButton(Frame):
    def __init__(self, parent, text="", command=None, style=None):
        Frame.__init__(self, parent, height=36, width=100)

        self.pack_propagate(0)
        self._btn = Button(self, text=text, command=command, style=style)
        self._btn.pack(fill=BOTH, expand=1)

    def disable(self):
        self._btn.state(["disabled"])

    def enable(self):
        self._btn.state(["!disabled"])


class StyledCombobox(Frame):
    def __init__(self, parent, values=None, style=None):
        Frame.__init__(self, parent, height=30, width=100)

        self.pack_propagate(0)
        self._cbx = Combobox(self, values=values, style=style, state="readonly")
        self._cbx.current(3)
        self._cbx.pack(fill=BOTH, expand=1)

    def get(self):
        return self._cbx.get()

    def disable(self):
        self._cbx.config(state="disabled")

    def enable(self):
        self._cbx.config(state="readonly")
