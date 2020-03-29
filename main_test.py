import time
import datetime
import class_module
from selenium import webdriver
from bs4 import BeautifulSoup

# Initialize
ISIN = 'DE0008232125'
stock_data_list = []


def setup_soup(ISIN):
    # Start WebDriver and load the page
    wd = webdriver.Firefox()
    wd.get('https://www.boerse-frankfurt.de/aktie/{}'.format(ISIN))
    time.sleep(5)
    # Grab HTML source code
    html_page = wd.page_source
    wd.quit()
    soup = BeautifulSoup(html_page, 'html.parser')
    # Grab all HTML code
    soup.prettify()
    return soup


def get_current_stock_data():
    # Grab current stock price
    soup = setup_soup(ISIN)
    current_stock_price = soup.find(True, {"class": ["widget-table-cell text-right last-price text-color-red",
                                                     "widget-table-cell text-right last-price text-color-green"]})
    current_stock_price = current_stock_price.text.replace(' ', '')
    current_stock_price = current_stock_price.replace(',', '.')
    current_stock_price = float(current_stock_price)

    # Grab all values under <tr>
    table_body = soup.find('body')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [x.text.strip() for x in cols]
        stock_data_list.append(cols)

    # Grab day high/low
    day_high_low = stock_data_list[13][1].split('/')
    day_high = str(day_high_low[0])
    day_high = day_high.replace(',', '.')
    day_high = float(day_high)
    day_low = str(day_high_low[1])
    day_low = day_low.strip()
    day_low = day_low.replace(',', '.')
    day_low = float(day_low)

    # Grab date/ time
    date = stock_data_list[0][1]
    date_obj = datetime.datetime.strptime(date, '%d.%m.%y %H:%M:%S')

    # Grab closing price
    close = stock_data_list[12][1]
    close = close.replace(',', '.')
    close = float(close)

    # Grab ISIN, WKN, shortname, longname
    info = soup.find(True, {"class": ["app-loading-spinner-parent col-md-6 col-lg-8"]})
    info = info.text
    longname = info.split("ISIN:", 1)[0]
    longname = longname.strip()
    info = info.split("ISIN: ", 1)[1]
    isin = info.split(" | WKN:", 1)[0]
    wkn = info.split(" | Kürzel: ", 1)[0]
    wkn = wkn.split("WKN: ", 1)[1]
    info = info.split("Kürzel: ", 1)[1]
    shortname = info.split(" | Typ:", 1)[0]

    return date_obj, "%.2f" % current_stock_price, "%.2f" % day_high, "%.2f" % day_low, "%.2f" % close, \
           longname, shortname, isin, wkn


dateobj, current_stock_price, day_high, day_low, close, longname, shortname, isin, wkn = get_current_stock_data()

# Test Parsing
LHA = class_module.Stock(isin, wkn, longname, shortname)

# class Scraper:
#     self.isin
#     self.time
#     # ...
#     # ...
#     def __init__(self, isin):
#         # scraping findet hier statt
#         self.isin = isin
#         self.day_low = "%.2f" % day_low
#
#     def get_share_price(self):
#         share_price = class_module.SharePrice(self.time, self.isin, self.price)
#         return share_price
