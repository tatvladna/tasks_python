class StringValue:
    def __init__(self, min_length=2, max_length=50):
        self.min_l = min_length
        self.max_l = max_length

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        print('inside get of StringValue')
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        print('inside set of StringValue')
        if not(isinstance(value, str) and self.min_l <= len(value) <= self.max_l):
            raise ValueError('incorrect name')
        instance.__dict__[self._name] = value



class PriceValue:
    def __init__(self, max_value=10000):
        self.max_v = max_value

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        print('inside set of PriceValue')
        if not(isinstance(value, int) and 0 <= value <= self.max_v):
            raise ValueError('incorrect value of price')
        instance.__dict__[self._name] = value

        # else:
        #     print('incorrect value')


class Product:
    name = StringValue()
    price = PriceValue()

    def __init__(self, name, price):
        self.name = name
        self.price = price


class SuperShop:
    def __init__(self, name, goods=()):
        self.name = name
        self.goods = list(goods)

    def add_product(self, product):
        self.goods.append(product)

    def remove_product(self, product):
        self.goods.remove(product)


shop = SuperShop('Shop')

shop.add_product(Product('apple', 5))
shop.add_product(Product('orange', 30))

for p in shop.goods:
    print(f"{p.name} {p.__dict__}")
