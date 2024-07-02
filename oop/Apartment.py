class Apart:

    def __init__(self, area, price, sold=False,  sale=2):
        self._area = area
        self._price = self.check_price(price) - price * self.check_sale(sale) / 100
        self._sold = sold
        self._sale = self.check_sale(sale)

    def check_price(self, price):
        if not isinstance(price, (int, float)):
            raise TypeError("price must be integer or float")
        return price

    def check_sale(self, sale):
        if isinstance(sale, bool):
            raise TypeError("sale must not be bool")

        elif isinstance(sale, str):
            if sale.endswith("%"):
                sale = sale.rstrip("%")
            try:
                sale = int(sale) if float(sale).is_integer() else float(sale)
            except:
                raise ValueError(f"sale is not correct: {sale}")

        return sale


    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, area):
        if not isinstance(area, (int, float)):
            raise TypeError("area must be integer or float")
        self._area = area



    @property
    def sold(self):
        return self._sold

    @sold.setter
    def sold(self, sold):
        if not isinstance(sold, bool):
            raise TypeError("sold must be bool")
        self._sold = sold



    @property
    def sale(self):
        return self._sale

    @sale.setter
    def sale(self, sale):
        if sale == 2:
            raise Exception("Warning: sale = 2%")

        if isinstance(sale, bool):
            raise TypeError("sale must not be bool")

        elif isinstance(sale, str):
            if sale.endswith("%"):
                sale = sale.rstrip("%")
            try:
                sale = int(sale) if float(sale).is_integer() else float(sale)
            except:
                raise ValueError(f"sale is not correct: {sale}")

        self._sale = sale


    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if self._sold:
            raise Exception("Sorry. Apart is sold.")

        elif not isinstance(price, (int, float)):
            raise TypeError("price must be integer or float")
        self._price = price - price * self._sale / 100


    def sell(self):
        if self._sold:
            print(f"Apart sold for {self._price}")
        else:
            print(f"Apart is not sold")


a = Apart(area=1333, price=1234, sold=False, sale="20%")
print(a.area)
print(a.price)
print(a.sold)
print(a.sale)
a.sell()
a.price = 121345672345
a.sold = True
a.sell()

# ========================

#  Abstract classes

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def get_area(self):
        print('base area')

    def change_color(self, color):
        print('color changed')


class Square(Shape):
    def get_area(self):
        print('square area')


class Rectangle(Shape):
    def get_area(self):
        super().get_area()
        print('rectangle area')

# sh = Shape()
s = Square()
s.get_area()

r = Rectangle()
r.get_area()
r.change_color('ad')