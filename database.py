import mysql.connector
from class_module import *


class Database:
    def __init__(self):
        self.user = "root"
        self.password = "root"
        self.host = "localhost"
        self.database = "webscraper"

        try:
            self.db = mysql.connector.connect(host=self.host,
                                              user=self.password,
                                              password=self.user,
                                              database=self.database)
        except mysql.connector.Error as e:
            print("Fehler mit der Databenbank: {}".format(e))
            self.db = False

    def close_db(self):
        if self.db:
            self.db.close()

    def get_stock(self):
        statement = "SELECT * FROM t_stock ORDER BY longName"
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(statement)
            except mysql.connector.Error as e:
                print("Fehler mit der Databenbank: {}".format(e))
            else:
                result = cursor.fetchall()
                stock_list = []
                for item in result:
                    stock = Stock(item[0], item[1], item[2], item[3])
                    stock_list.append(stock)
                cursor.close()
                return stock_list
        else:
            return False

    def get_low_high_close(self):
        statement = "SELECT * FROM t_lowHighClose ORDER BY date_pk DESC"
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(statement)
            except mysql.connector.Error as e:
                print("Fehler mit der Databenbank: {}".format(e))
            else:
                low_high_close_list = []
                result = cursor.fetchall()
                for item in result:
                    low_high_close = LowHighClose(item[0], item[1], item[2], item[3], item[4])
                    low_high_close_list.append(low_high_close)
                cursor.close()
                return low_high_close_list

    def get_share_price(self):
        statement = "SELECT * FROM (SELECT DISTINCT * FROM t_sharePrice ORDER BY time_pk DESC) x GROUP BY fk_isin"
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(statement)
            except mysql.connector.Error as e:
                print("Fehler mit der Datenbank: {}".format(e))
            else:
                share_price_list = []
                result = cursor.fetchall()
                for item in result:
                    share_price = SharePrice(item[0], item[1], item[2])
                    share_price_list.append(share_price)
                cursor.close()
                return share_price_list

    def write_stock(self, stock):
        statement = ("INSERT INTO t_stock VALUES('{}', '{}', '{}', '{}')"
                     .format(stock.get_isin(), stock.get_wkn(), stock.get_long_name(), stock.get_short_name()))
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(statement)
                self.db.commit()
            except mysql.connector.Error as e:
                print("Fehler beim Schreiben in die Datenbank: {}".format(e))
            else:
                cursor.close()

    def remove_stock(self, stock):
        statements = [
            "DELETE FROM t_lowHighClose WHERE fk_isin = '{}'",
            "DELETE FROM t_shareprice WHERE fk_isin = '{}'",
            "DELETE FROM t_stock WHERE isin = '{}'"
        ]
        for statement in statements:
            if self.db:
                try:
                    cursor = self.db.cursor()
                    cursor.execute(statement.format(stock.get_isin()))
                    self.db.commit()
                except mysql.connector.Error as e:
                    print("Fehler beim Entfernen der Aktie aus der Datenbank: {}".format(e))
                else:
                    cursor.close()

    def write_low_high_close(self, low_high_close):
        statement = ("INSERT INTO t_lowHighClose VALUES('{0}', '{1}', {2}, {3}, {4}) "
                     "ON DUPLICATE KEY UPDATE dayLow = {2}, dayHigh = {3}, prevClose = {4}")
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(statement.format(low_high_close.get_date(), low_high_close.get_isin(),
                                                low_high_close.get_low(), low_high_close.get_high(),
                                                low_high_close.get_close()))
                self.db.commit()
            except mysql.connector.Error as e:
                print("Fehler beim Schreiben von lowHighClose: {}", format(e))
            else:
                cursor.close()

    def write_share_price(self, share_price):
        statement = "INSERT INTO t_sharePrice VALUES('{}', '{}', {})"
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(statement.format(share_price.get_time(), share_price.get_isin(), share_price.get_price()))
            except mysql.connector.Error as e:
                print("Fehler beim Schreiben von sharePrice: {}".format(e))
            else:
                cursor.close()

    # Moment nicht verwendet
    def write_share_price_list(self, share_price_list):
        statement = "INSERT INTO t_sharePrice VALUES('{}', '{}', {})"
        for sharePrice in share_price_list:
            if self.db:
                try:
                    cursor = self.db.cursor()
                    cursor.execute(statement.format(sharePrice.get_time(), sharePrice.get_isin(),
                                                    sharePrice.get_price()))
                    self.db.commit()
                except mysql.connector.Error as e:
                    print("Fehler beim Schreiben von sharePrice Liste: {}".format(e))
                else:
                    cursor.close()
