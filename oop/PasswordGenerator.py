import numpy as np
import random


class PasswordGenerator():
    '''Класс генератор паролей'''
    def __init__(self, alphabet, size):
        self.alphabet = alphabet
        self.size = size

    def generator(self):
        return "".join(random.choices(alphabet, k=self.size))

    def evaluation(self, V, T):
        return V * T / len(self.alphabet) ** self.size


if __name__ == '__main__':
    alphabet ='0123456789qwertyuiopasdfghjklzxcvbnm'
    P = 0.000001            # вероятность перебора паролей злоумышленником
    V = 20                  # скорость перебора [passwords/minutes]
    T = 3 * 7 * 24 * 60     # период действия пароля
    S = V * T / P
    size = round(np.log(S) / np.log(len(alphabet)))
    print(f'Минимальная длина пароля L={size} симолов')

    password_generator = PasswordGenerator(alphabet, size)
    print(f'Вероятность P подбора злоумышленником в течении всего срока действия пароля P={round(password_generator.evaluation(T, V), 12)}')

    print('\nПримеры генерируемых паролей: ')
    for i in range(10):
        print(password_generator.generator())