# Электронная библиотека. Реализуйте классы Book (отдельная книга в библиотеке) и Library (класс для управления книгами в библиотеке).
# Используйте дескрипторы данных для реализации следующего:
# При добавлении новой книги в библиотеку, убедитесь, что книга уникальна по своему названию и автору.
# При удалении книги из библиотеки, убедитесь, что она действительно существует в базе данных.
# При запросе чтения книги, убедитесь, что книга доступна для чтения (т.е., она существует в библиотеке).
# При установке атрибутов (например, названия книги, автора и дополнительных при наличии), удостоверьтесь, что они не пустые.
class DescriptionBook:
    def __set_name__(self, owner, name):
        self.name = name
        # self.name = f'_{name}'  # private_name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # return getattr(instance, self.name)
        return instance.__dict__[self.name]


    def __set__(self, instance, value):
        if not isinstance(value, str) or not value:
            raise Exception("attribute must be str and not empty")
        # setattr(instance, self.name, value)
        instance.__dict__[self.name] = value


class Book:

    title = DescriptionBook()
    autor = DescriptionBook()


    def __init__(self, title, autor):
        self.title = title
        self.autor = autor

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.title == other.title and self.autor == other.autor
        return NotImplemented

class Library:
    def __init__(self):
        self.list = []

    def add(self, new_book):
        if not isinstance(new_book, Book):
            raise Exception("object must be class Book")
        if new_book in self.list:
            raise Exception('This book is already in the library')
        self.list.append(new_book)

    def delete(self, book):
        if book not in self.list:
            raise Exception(f'There is no {book.title} by {book.autor} in library')
        self.list.remove(book)

    def read(self, book):
        print(f'You read a book: {book.title} by {book.autor}') if book in self.list \
            else print(f'There is no {book.title} by {book.autor} in library')

    def __call__(self, *args, **kwargs):
        print(f"There are {len(self.list)} books in your library")


b = Book("War and Peace", "Leo Tolstoy")  # create copy of Book
b2 = Book('Garnet Bracelet', 'Alexander Kuprin')
b3 = Book('Garnet Bracelet', 'Alexander Kuprin')

lib = Library()  # create library
lib.add(b)  # addition book in the library
lib.add(b2)  # addition book in the library

try:
    lib.add(b3)
except Exception as e:
    print(e)

lib()


lib.delete(b)
lib()

lib.read(b2)

try:
    lib.read(b)
except Exception as e:
    print(e)


try:
    lib.delete(b)
except Exception as e:
    print(e)

print(lib.__dict__)