from weakref import ref, WeakKeyDictionary
import gc

# a = set([1, 2, 3])
# wr = ref(a)
# print(wr())
# del a
# print(wr)
# print(wr())


class A:
    def __init__(self):
        self.data = [1, 2, 3]


a = A()
d = {a: True}

wd = WeakKeyDictionary(d)
del d
gc.collect()
print(wd.keyrefs())
print(wd)