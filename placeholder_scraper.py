from class_module import *
from datetime import datetime


def get_new_stock(isin):
    return Stock(isin, "wkn", "name", "kürzel")


def start_scraping():
    print("Scraping gestartet")


def stop_scraping():
    print("Scraping gestoppt")


def get_new_low_high_close(isin):
    return LowHighClose(datetime.date(datetime.now()), isin, 1.0, 5.9, 3.3)


def get_new_share_price_list():
    return
