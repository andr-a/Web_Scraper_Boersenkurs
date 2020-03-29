import time
import datetime
import class_module
from selenium import webdriver
from bs4 import BeautifulSoup

# Initialize
# isi = 'DE0008232125'  # Zum Testen


class Scraper:
    def __init__(self, isin):
        self.isin = isin
        self.close = 0.0
        print(self.close)

    # @staticmethod
    # def setup_soup(ISIN):
        # Start WebDriver and load the page
        wd = webdriver.Firefox()
        wd.get('https://www.boerse-frankfurt.de/aktie/{}'.format(isin))
        time.sleep(1)
        # Grab HTML source code
        html_page = wd.page_source
        wd.quit()
        soup = BeautifulSoup(html_page, 'html.parser')
        # Grab all HTML code
        soup.prettify()

        # Grab current stock price
        current_stock_price = soup.find(True, {"class": ["widget-table-cell text-right last-price text-color-red",
                                                         "widget-table-cell text-right last-price text-color-green"]})
        current_stock_price = current_stock_price.text.replace(' ', '')
        current_stock_price = current_stock_price.replace(',', '.')
        current_stock_price = "%.3f" % float(current_stock_price)
        self.current_stock_price = current_stock_price

        # Grab all values under <tr>
        self.stock_data_list = []
        table_body = soup.find('body')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            self.stock_data_list.append(cols)

        # Grab day high/low
        day_high_low = self.stock_data_list[13][1].split('/')
        day_high = str(day_high_low[1])
        day_high = day_high.replace(',', '.')
        day_high = "%.3f" % float(day_high)
        day_low = str(day_high_low[0])
        day_low = day_low.strip()
        day_low = day_low.replace(',', '.')
        day_low = "%.3f" % float(day_low)
        self.day_low = day_low
        self.day_high = day_high

        # Grab date/ time
        date = self.stock_data_list[0][1]
        date_obj = datetime.datetime.strptime(date, '%d.%m.%y %H:%M:%S')
        self.date_obj = date_obj
        print(date)

        # Grab closing price
        close = self.stock_data_list[12][1]
        close = close.replace(',', '.')
        close = "%.3f" % float(close)
        self.close = close

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
        self.wkn = wkn
        self.longname = longname
        self.shortname = shortname
        print(longname, date, current_stock_price, day_low, day_high, close)

    def get_share_price(self):
        share_price = class_module.SharePrice(self.date_obj, self.isin, self.current_stock_price)
        return share_price

    def get_low_high_close(self):
        low_high_close = class_module.LowHighClose(self.date_obj.date(), self.isin,
                                                   self.day_low, self.day_high, self.close)
        return low_high_close

    def get_stock(self):
        stock = class_module.Stock(self.isin, self.wkn, self.longname, self.shortname)
        return stock

# Testing
# scrapy = Scraper(isi)
# shary, lowhighy, stocky = scrapy.setup_soup(isi)
# print(shary)
# print(lowhighy)
# print(stocky)

