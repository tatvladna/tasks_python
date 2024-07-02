class A:
    ...


# a = A
#
# B = type('B', (A,), {'data': 123})
# print(B.__mro__)
# print(B.__dict__)


class MyMeta(type):
    @classmethod
    def __prepare__(metacls, name, bases, **extra_kwargs):
        print('Preparing namespace for', name)
        return {}

    def __new__(cls, name, bases, attrs):
        print('creating class', name)
        return super().__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        print('initialization', name)

    def __call__(cls, *args, **kwargs):
        print('creating instance of', cls)


class B:
    ...


def decorator(cls):
    print(cls, 'decorating...')
    return cls


@decorator
class C(metaclass=MyMeta):
    ...


c = C()


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value


s1 = Singleton('1')
s2 = Singleton('2')


# print(s1)
# print(s2)
# print(s1 is s2)


class Meta(type):
    def __new__(cls, name, bases, attrs):
        attrs['data'] = 123
        # bases = list(bases)
        # bases.append(A)
        # bases = tuple(bases)
        # print(bases)
        bases = (*bases, A)
        return super().__new__(cls, name, bases, attrs)


class Final(type):
    def __new__(cls, name, bases, attrs):
        for c in bases:
            if isinstance(c, Final):
                raise Exception(f'class {c.__name__} is inheritable')
        return super().__new__(cls, name, bases, attrs)


class NotInheritable(metaclass=Final):
    pass


# class Data(NotInheritable):
#     ...


class NMeta(type):
    ...


class N(metaclass=NMeta):
    ...


class LMeta(type):
    ...


class L(metaclass=LMeta):
    ...


class QMeta(NMeta, LMeta):
    ...


class Q(N, L, metaclass=QMeta):
    ...


from abc import ABC, ABCMeta, abstractmethod


class MyMetaABC(ABCMeta):
    ...


class MyClass(metaclass=ABCMeta):
    @abstractmethod
    def method(self):
        ...

    def color(self):
        ...


class LoggerMeta(type):
    def __new__(cls, name, bases, attrs):
        for cls_name, method in attrs.items():
            if callable(method) and hasattr(method, '__logged__'):
                attrs[cls_name] = cls.decorate(method)
        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def decorate(func):
        def inner(*args, **kwargs):
            print('START')
            result = func(*args, **kwargs)
            print('DONE')
            return result

        return inner


def logged(method):
    method.__logged__ = True
    return method


class LoggerClass(metaclass=LoggerMeta):
    @logged
    def method(self):
        ...

    @logged
    def fun(self):
        ...

    def hello(self):
        ...


lc = LoggerClass()
lc.method()