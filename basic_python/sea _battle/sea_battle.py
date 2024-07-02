import tkinter as tk
from tkinter import *
import re
import numpy as np
import pickle
import random



def rules_game():  # Правила игры
    """
    This function returns Rules of the game
    :return: rules of the game
    """
    with open('rules_game.txt', 'r', encoding='utf-8') as data:
        rules_game = data.read().replace('\t', '   ').split('\n')

    window_rules = Toplevel()
    window_rules.attributes("-topmost",True)  # чтобы окно всегда выводилось сверху
    window_rules.title("Rules Game")
    window_rules.geometry("600x250")
    window_rules.resizable(width=False, height=False)  # запрещаем редактировать размер окна
    label = Label(window_rules, text='Rules Game "Sea Battle"')  # создаем текстовую метку
    label.pack()  # размещаем метку в окне

    languages_var = StringVar(window_rules, value=rules_game)
    listbox = Listbox(window_rules, listvariable=languages_var)
    listbox.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar = tk.Scrollbar(window_rules, orient="vertical", command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox["yscrollcommand"] = scrollbar.set
    window_rules.grab_set()
    window_rules.mainloop()



def dismiss(window, root):  
    """
    This function closes two windows

    :param window: game window
    :param root: main window
    :return: closing two windows
    """
    window.grab_release()
    window.destroy()
    root.destroy()


def click():  # ФУНКЦИЯ ДЛЯ СТОП - root
    """

    :return: Closing the main window
    """
    window = Tk()
    window.attributes("-topmost", True)  # чтобы окно всегда выводилось сверху
    window.title("Close")
    window.geometry("250x100")
    label = tk.Label(window, text="Are you sure you want to exit the game?")
    label.pack(anchor=CENTER, expand=0, fill=NONE)
    no_button = tk.Button(window, text="no", command=lambda: window.destroy())  # "no"
    yes_button = tk.Button(window, text="yes", command=lambda: dismiss(window, root))  # "yes"
    no_button.pack(anchor="e", side=RIGHT)
    yes_button.pack(anchor="w", side=LEFT)
    window.grab_set()





def user_name():

    def save_name():
        with open('user_name.txt', 'w', encoding='utf-8') as name_user:
            if mode:
                name_user.write(user_name1.get())
                name_user.write('\n')
                name_user.write(user_name2.get())
            else:
                name_user.write(user_name1.get())
                name_user.write('\n')
                name_user.write('Kомпьютер')



    def start_game():


        with open('user_name.txt', 'r', encoding='utf-8') as name_user:
            names = []
            for line in name_user:
                names.append(''.join(re.findall(r'[^\n]', line)))

        user_name1, user_name2 = names  # распаковка

        def add_to_all(event):
            global points1, points2, hod_igrovomu_polu_1
            _type = 0  # ЛКМ
            if event.num == 3:
                _type = 1  # ПКМ
            print(_type)
            mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()  # координата мышки по ox относительно всего поля
            mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()  # координата мышки по oy относительно всего поля
            # print(mouse_x, mouse_y)
            ip_x = mouse_x // step_x  # координаты относительно игрового поля
            ip_y = mouse_y // step_y  # координаты относительно игрового поля
            print(ip_x, ip_y, "_type:", _type)


        # здесь мы можем сами разместить корабли
        matrix = np.array([[3, 0, 0, 0, 0, 0, 3, 0, 0, 0],
                           [3, 0, 0, 4, 0, 0, 3, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                           [0, 0, 1, 1, 1, 1, 0, 0, 2, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 2, 0, 0, 3, 3, 0, 0],
                           [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                           [4, 0, 0, 2, 0, 0, 0, 0, 4, 0]])

        with open('ships.bin', 'bw') as data:
            pickle.dump(matrix, data)

        def generation_ships():
            with open('ships.bin', 'rb') as data:
                ships = pickle.load(data)

                # # игровое поле = матрица, напишем свой собственный алогоритм для рандомного переставления кораблей
                matrix_operations = ['transpose', 'rot90', 'fliplr', 'flipud']
                for i in range(1500):
                    operations = random.choice(matrix_operations)
                    if operations == 'transpose':
                        ships = np.transpose(ships)
                    elif operations == 'rot90':
                        ships = np.rot90(ships)
                    elif operations == 'fliplr':
                        ships = np.fliplr(ships)
                    else:
                        ships = np.flipud(ships)

            return ships

            enemy_ships1 = generation_ships()
            list_ids = []  # список объектов canvas



            def draw_point(x, y):
                # print(enemy_ships1[y][x])
                if enemy_ships1[y][x] == 0:
                    color = "red"
                    id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y,
                                             fill=color)
                    id2 = canvas.create_oval(x * step_x + step_x // 3, y * step_y + step_y // 3,
                                             x * step_x + step_x - step_x // 3,
                                             y * step_y + step_y - step_y // 3, fill="white")
                    list_ids.append(id1)
                    list_ids.append(id2)
                if enemy_ships1[y][x] > 0:
                    color = "blue"
                    id1 = canvas.create_rectangle(x * step_x, y * step_y + step_y // 2 - step_y // 10,
                                                  x * step_x + step_x,
                                                  y * step_y + step_y // 2 + step_y // 10, fill=color)
                    id2 = canvas.create_rectangle(x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                                  x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y,
                                                  fill=color)
                    list_ids.append(id1)
                    list_ids.append(id2)

            def draw_point2(x, y, offset_x=size_canvas_x + menu_x):
                # print(enemy_ships1[y][x])
                if enemy_ships2[y][x] == 0:
                    color = "red"
                    id1 = canvas.create_oval(offset_x + x * step_x, y * step_y, offset_x + x * step_x + step_x,
                                             y * step_y + step_y,
                                             fill=color)
                    id2 = canvas.create_oval(offset_x + x * step_x + step_x // 3, y * step_y + step_y // 3,
                                             offset_x + x * step_x + step_x - step_x // 3,
                                             y * step_y + step_y - step_y // 3, fill="white")
                    list_ids.append(id1)
                    list_ids.append(id2)
                if enemy_ships2[y][x] > 0:
                    color = "blue"
                    id1 = canvas.create_rectangle(offset_x + x * step_x, y * step_y + step_y // 2 - step_y // 10,
                                                  offset_x + x * step_x + step_x,
                                                  y * step_y + step_y // 2 + step_y // 10, fill=color)
                    id2 = canvas.create_rectangle(offset_x + x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                                  offset_x + x * step_x + step_x // 2 + step_x // 10,
                                                  y * step_y + step_y,
                                                  fill=color)
                    list_ids.append(id1)
                    list_ids.append(id2)

        def new_click():  # ФУНКЦИЯ ДЛЯ СТОП - window_game
            window = Tk()
            window.attributes("-topmost", True)  # чтобы окно всегда выводилось сверху
            window.title("Close")
            window.geometry("250x100")
            label = tk.Label(window, text="Are you sure you want to exit the game?")
            label.pack(anchor=CENTER, expand=0, fill=NONE)
            no_button = tk.Button(window, text="no", command=lambda: window.destroy())  # "no"
            yes_button = tk.Button(window, text="yes", command=lambda: new_dismiss(window, window_game))  # "yes"
            no_button.pack(anchor="e", side=RIGHT)
            yes_button.pack(anchor="w", side=LEFT)
            window.grab_set()

        def new_dismiss(window, window_game):  # ФУНКЦИЯ ДЛЯ СТОП
            window.grab_release()
            window.destroy()
            window_game.destroy()
            # после завершения игры очищаем файл с именами игроков
            with open('user_name.txt', 'w', encoding='utf-8'):
                pass

        root.destroy()
        window_user_name.destroy()
        window_game = Tk()
        window_game.protocol("WM_DELETE_WINDOW", new_click)  # перехватывание окна
        window_game.title("Sea Battle")
        #window_game.wm_attributes('-fullscreen',True)

        # разворачиваем игру на весь экран
        window_game.geometry('{}x{}'.format(window_game.winfo_screenwidth(), window_game.winfo_screenheight()))

        window_game.iconphoto(False, PhotoImage(file="battleship-logo.png"))  # картинка

        tk.Button(window_game, text='Rules of the game', width=20, command=rules_game).\
            pack(anchor=NE, expand=True, padx=20, pady=30)

        Label(text='How to arrange the ships?').pack(anchor=S, expand=True)  # как расставить корабли?


        automatic = 'Automatically'
        loading_file = 'Loading ships from a file'
        str_var = StringVar(value=loading_file)  # Режим по умолчанию
        tk.Radiobutton(text=automatic, value=automatic, variable=str_var).pack(anchor=S, expand=True)
        tk.Radiobutton(text=loading_file, value=loading_file, variable=str_var).pack(anchor=S, expand=True)

        # рисуем сетку для игры
        size_canvas_x = 500  # общий размер по оси х
        size_canvas_y = 500  # общий размер по оси y
        s_x = s_y = 10  # размер игрового поля (10x10)
        step_x = size_canvas_x // s_x  # шаг по горизонтали
        step_y = size_canvas_y // s_y  # шаг по вертикали
        size_canvas_x = step_x * s_x
        size_canvas_y = step_y * s_y
        menu_x = step_x * 8  # на какое расстояние расположить поля
        menu_y = 40
        # помещаем наше игровое окно выше остальных окон на компьютере, чтобы другие окна не могли его заслонить
        window_game.wm_attributes("-topmost", 1)
        canvas = Canvas(window_game, width=size_canvas_x + menu_x + size_canvas_x, height=size_canvas_y + menu_y, bd=0,
                        highlightthickness=0)
        canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
        canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x + menu_x + size_canvas_x, size_canvas_y,
                                fill="lightyellow")

        canvas.bind_all("<Button-1>", add_to_all)  # ЛКМ
        canvas.bind_all("<Button-3>", add_to_all)  # ПКМ
        canvas.pack()
        window_game.update()

        def draw_table(offset_x=0):
            for i in range(0, s_x + 1):
                canvas.create_line(offset_x + step_x * i, 0, offset_x + step_x * i, size_canvas_y)
            for i in range(0, s_y + 1):
                canvas.create_line(offset_x, step_y * i, offset_x + size_canvas_x, step_y * i)

        draw_table()
        draw_table(size_canvas_x + menu_x)

        t0 = Label(window_game, text=f"Игрок {user_name1}", font=("Helvetica", 16))
        t0.place(x=size_canvas_x - t0.winfo_reqwidth() * 3, y=size_canvas_y + 160)

        t1 = Label(window_game, text=f"Игрок {user_name2}", font=("Helvetica", 16))
        t1.place(x=size_canvas_x + menu_x + size_canvas_x - 250, y=size_canvas_y + 160)

        t0.configure(bg="red")
        t0.configure(bg="#f0f0f0")

        tk.Button(window_game, text='Stop', width=20, command=new_click).\
            pack(anchor=SE, expand=True, padx=20, pady=30)  # регулируем нахождение кнопки stop


        if user_name2 == 'Компьютер':
            pass

        else:
            pass



        window_game.mainloop()




    if mode:
        window_user_name = Tk()
        window_user_name.title('Please enter the name')
        window_user_name.geometry('250x180')
        tk.Label(window_user_name, text=f"Игрок №1").pack()

        user_name1 = tk.Entry(window_user_name, textvariable=StringVar())
        user_name1.pack()
        tk.Button(window_user_name, text="Сохранить", command=save_name).pack()

        tk.Label(window_user_name, text=f"Игрок №2").pack()

        user_name2 = tk.Entry(window_user_name, textvariable=StringVar())
        user_name2.pack()
        tk.Button(window_user_name, text="Сохранить", command=save_name).pack()

        tk.Button(window_user_name, text="Отправить", command=start_game).pack(anchor=S, expand=True)
        window_user_name.mainloop()

    else:
        window_user_name = Tk()
        window_user_name.title('Please enter the name')
        window_user_name.geometry('250x180')
        tk.Label(window_user_name).pack()

        user_name1 = tk.Entry(window_user_name, textvariable=StringVar())
        user_name1.pack()
        tk.Button(window_user_name, text="Сохранить", command=save_name).pack()

        tk.Button(window_user_name, text="Отправить", command=start_game).pack(anchor=S, expand=True)
        window_user_name.mainloop()



# для выбора режима игры
def game_mode1():

    """
    This function returns the game mode.
    True - user vs user
    False - user vs computer
    :return: the game mode
    """

    global mode
    mode = True

def game_mode2():

    """
    This function returns the game mode.
    True - user vs user
    False - user vs computer
    :return: the game mode
    """

    global mode
    mode = False
# ------------------------------------------------------------------


root = Tk()  # создаем корневой объект - окно
root.protocol("WM_DELETE_WINDOW", click)  # перехватывание окна
root.title("Sea battle")  # устанавливаем заголовок окна


# можно зарпетить пользовтаелю растягивать окно -> root.resizable(False, False)
# также можно установить минимальное и максимальное размеры окон
root.geometry("700x500")  # устанавливаем размеры окна

icon = PhotoImage(file="battleship-logo.png")  # устанавливаем картинку
root.iconphoto(False, icon)  # картинка

rules_button = tk.Button(root, text='Rules of the game', width=20, command=rules_game)
rules_button.pack(anchor=NE, expand=True, padx=20, pady=30)

position = {"padx": 6, "pady": 6, "anchor": NW}

user_user = "User1 vs User2"
user_comp = "User vs Computer"


mode = False

tk.Label(text='Please select a game mode').pack(**position)


lang = StringVar(value=user_comp)    # Режим по умолчанию
tk.Radiobutton(text=user_user, value=user_user, variable=lang, command=game_mode1).pack(**position)
tk.Radiobutton(text=user_comp, value=user_comp, variable=lang, command=game_mode2).pack(**position)

Label(text='Start a game of "Sea Battle"?').pack(anchor=S, expand=True)  # размещаем метку в окне
start_button = tk.Button(root, text='Start', padx=10, pady=5, command=user_name)
start_button.pack(anchor=N, expand=True)

stop_button = tk.Button(root, text='Stop', width=20, command=click)  # button - создание кнопки ("stop")
stop_button.pack(anchor=SE, expand=True, padx=20, pady=30)  # регулируем нахождение кнопки stop


rules_game()  # для того, чтобы сразу высвечивались правила игры (нужно располагать после всех кнопок)


#-----------------------

root.mainloop()  # для отображения окна