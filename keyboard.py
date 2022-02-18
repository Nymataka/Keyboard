from random import choice
from tkinter import *
from tkinter import messagebox as mb
import shelve
import os


class Keyboard:
    """Все символы клавиатуры"""
    easy = [['Esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'PrtSc\nSysRq',
             'Scroll\nLock', 'Pause\nBreak'],
            ['~ Ё\n`', '!\n1', '@ "\n2', '# №\n3', '$ ;\n4', '%\n5', '^ :\n6', '& ?\n7', '*\n8', '(\n9', ')\n0',
             '-\n_', '+\n=', '⌫', 'Insert', 'Home', 'Page\nUp'],
            ['Tab', 'Q\nЙ', 'W\nЦ', 'E\nУ', 'R\nК', 'T\nЕ', 'Y\nН', 'U\nГ', 'I\nШ', 'O\nЩ', 'P\nЗ', '{\n[ Х',
             '}\n] Ъ', '\ | /', 'Del', 'End', 'Page\nDown'],
            ['Caps\nLock', 'A\nФ', 'S\nЫ', 'D\nВ', 'F\nА', 'G\nП', 'H\nР', 'J\nО', 'K\nЛ', 'L\nД', ':\n; Ж',
             '"\nЭ', 'Enter'],
            ['Shift', 'Z\nЯ', 'X\nЧ', 'C\nС', 'V\nМ', 'B\nИ', 'N\nТ', 'M\nЬ', '<\n, Б', '>\n. Ю', '? ,\n/ .',
             'Shift', '↑'],
            ['Ctrl', 'Win', 'Alt', 'Space', 'Alt', 'Fn', '≣ Menu', 'Ctrl', '←', '↓', '→']]
    """Символы клавиатуры только английской раскладки и без цифр"""
    hard = [['Esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'Ps', 'Sl', 'Pb'],
            ['~`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-\n_', '+\n=', '⌫', 'Ins', 'Hm', 'Pu'],
            ['↹', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{\n[', '}\n]', '|\n\ ', 'Del', 'End', 'Pd'],
            ['Caps\nLock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':\n;', '"', '↵'],
            ['⇧', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<\n,', '>\n.', '?\n/', '⇧', '↑'],
            ['Ctrl', 'Win', 'Alt', 'Space', 'Alt', 'Fn', '≣ Menu', 'Ctrl', '←', '↓', '→']]

    def __init__(self, root):
        """Настройки окна сложности"""
        self.root = root
        self.w = self.root.winfo_screenwidth() // 2
        self.h = self.root.winfo_screenheight() // 2
        self.root.geometry("200x200+{}+{}".format(self.w - 100, self.h - 100))
        self.root.resizable(width=False, height=False)
        self.root.title('level')
        self.root.iconbitmap('keyboard_ico.ico')
        """Настройка всех необходимых переменных"""
        self.stile = ("MS Sans Serif", 11)
        self.stile2 = ("MS Sans Serif", 20)
        self.stile3 = ("MS Sans Serif", 16)
        self.stile4 = ('Trebuchet MS', 20, 'bold')
        self.colors = ['skyblue', 'lime', 'violet', 'gold', 'red', 'white']
        self.top_buttons = [[0] * len(self.easy[0]), [0] * len(self.easy[1]), [0] * len(self.easy[2]),
                            [0] * len(self.easy[3]), [0] * len(self.easy[4]), [0] * len(self.easy[5])]
        self.bot_buttons = self.top_buttons
        self.new_meaning, self.level, self.symbols, self.symbols_copy, self.click = '', '', [], [], False
        self.width, self.y, self.x, self.x_next, self.error, self.right = 6, 5, 15, 0, 0, 0
        self.time_left, self.time_passed, self.all, self.time, self.grade = 211, 0, False, '', ''
        """Создание рамок и меток"""
        self.menu = Menu(self.root)
        self.finish = Frame(master=self.root, width=0, height=0, bg='black')
        self.last_result = Label(self.finish, width=21, height=4,
                                 bg='black', fg='white', relief='flat', font=self.stile2)
        self.result = Label(self.finish, width=21, height=4, bg='black', fg='white', relief='flat', font=self.stile2)
        self.record = Label(self.finish, width=21, height=4, bg='black', fg='white', relief='flat', font=self.stile2)
        self.top_panel = Frame(master=self.root, relief="ridge", bd=5, bg='black')
        self.time_display = Label(self.top_panel, relief='flat', bg='black', fg='white', font=self.stile4)
        self.progress = Label(self.top_panel, text='Готово: 0', relief='flat', bg='black', fg='white',
                              font=self.stile4, width=9)
        self.but_now = Button(self.top_panel, state='disabled', font=self.stile, width=6, height=2, bg='black',
                              relief='flat', disabledforeground='white')
        self.bot_panel = Frame(master=self.root, relief="ridge", bd=5, bg='black')
        self.mistake = Label(self.bot_panel, text=f'Ошибок: 0', width=16, height=1, font=self.stile3,
                             relief='groove', bg='black', fg='white')
        """Кнопки уровней"""
        self.complexity = Frame(master=self.root, relief="flat", bd=1)
        self.bot1 = Button(self.complexity, text='легко', width=12, height=2, font=self.stile2, relief='raised',
                           command=self.easy_level, bg='black', fg='blue', activebackground='black').pack()
        self.bot2 = Button(self.complexity, text='сложно', width=12, height=3, font=self.stile2, relief='raised',
                           command=self.hard_level, bg='black', fg='red', activebackground='black').pack()
        self.complexity.pack(fill=BOTH, expand=True)

    def start(self):
        """Настройки окна приложения и меню"""
        self.complexity.destroy()
        self.root.geometry("1300x700+{}+{}".format(self.w - 650, self.h - 350))
        self.root.resizable(width=False, height=False)
        self.root.title('Собери клавиатуру')
        self.root.iconbitmap('keyboard_ico.ico')
        self.menu.add_command(label="Начать заново", command=anew)
        self.root.config(menu=self.menu)
        self.finish.pack(fill=BOTH)
        """Копия символов"""
        for i in self.symbols:
            for j in i:
                self.symbols_copy.append(j)
        """Клавиши на верхней рамке в рандомном порядке"""
        self.top_panel.pack(fill=BOTH, expand=True)
        for i in range(len(self.top_buttons)):
            for j in range(len(self.top_buttons[i])):
                random_symbols = choice(self.symbols_copy)
                self.top_buttons[i][j] = Button(self.top_panel, text=random_symbols, font=self.stile, relief='groove',
                                                activebackground='black', bg='black', fg='white', width=6, height=2)
                self.top_buttons[i][j].config(
                    command=lambda t=random_symbols, btn=self.top_buttons[i][j]: self.take_text(t, btn))
                self.top_buttons[i][j].place(x=self.x, y=self.y)
                self.x += 75
                self.symbols_copy.remove(random_symbols)
            self.y += 55
            self.x = 15
        self.but_now.place(x=1215, y=5)
        """Клавиши на нижней рамки в правильном порядке но без символов"""
        self.x = 15
        self.y = 3
        self.bot_panel.pack(fill=BOTH, expand=True)
        self.mistake.place(x=1075, y=179)
        for i in range(len(self.bot_buttons)):
            for j in range(len(self.bot_buttons[i])):
                if i != 3 and i != 4 and j == len(self.bot_buttons[i]) - 3:
                    self.x = 1075
                elif i == 0 and (j == 1 or j == 5 or j == 9):
                    if j == 1:
                        self.x += 70
                    else:
                        self.x += 35
                elif i == 1 and (j == 13 or j == 12):
                    if j == 12:
                        self.x_next = -2
                    elif j == 13:
                        self.width += 9
                elif i == 2 and (j == 0 or j == 12 or j == 13):
                    if j == 12:
                        self.x_next = 2
                    else:
                        self.width += 4
                        self.x_next = 35
                elif i == 3 and (j == 0 or j == 12):
                    if j == 0:
                        self.width += 5
                        self.x_next = 43
                    elif j == 12:
                        self.width += 12
                elif i == 4 and (j == 0 or j == 10 or j == 11 or j == 12):
                    if j == 0:
                        self.width += 9
                        self.x_next = 74
                    elif j == 10:
                        self.x_next = -1
                    elif j == 11:
                        self.width += 17
                    elif j == 12:
                        self.x = 1145
                elif i == 5 and (j < 8):
                    if j < 3:
                        self.width += 1
                        self.x_next = 10
                    elif j == 3:
                        self.width += 48
                        self.x_next = 386
                    elif j == 4:
                        self.width += 1
                        self.x_next = 8
                    elif j == 5:
                        self.width += 1
                        self.x_next = 12
                    elif j == 6 or j == 7:
                        self.width += 3
                        self.x_next = 28
                self.bot_buttons[i][j] = Button(self.bot_panel, font=self.stile, width=self.width, relief='groove',
                                                activebackground='black', bg='black', height=2)
                self.bot_buttons[i][j].config(
                    command=lambda btn=self.bot_buttons[i][j], x=i, y=j: self.get_text(btn, x, y))
                self.bot_buttons[i][j].place(x=self.x, y=self.y)
                self.x += self.x_next
                self.x += 70
                self.x_next = 0
                self.width = 6
            self.x = 15
            if i != 0:
                self.y += 55
            else:
                self.y += 60

    def take_text(self, text, btn):
        """Получить текст нажатой клавиши верхней рамки """
        if self.click:
            return
        btn.config(state='disabled', relief='flat', disabledforeground='black')
        self.click = True
        self.new_meaning = text
        self.but_now.config(text=text, relief='groove')  # показывает выбранную сейчас кнопку

    def get_text(self, btn, x, y):
        """Если после выбора клавиши из верхней рамки выбрана правильная клавиша из нижней то поместить в нее текст,
         иначе добавить 1 к счетчику ошибок."""
        if self.new_meaning != '':
            if self.new_meaning == self.symbols[x][y]:
                btn.config(state='disabled', text=self.easy[x][y], disabledforeground=self.colors[x])
                self.new_meaning = ''
                self.click = False
                self.right += 1
                self.progress.config(text=f'Готово: {self.right}')
                self.but_now.config(text='', relief='flat')
                if self.right == 35:
                    """Окно с проверкой на честность """
                    examination = mb.askyesno('Проверка', 'Подглядываешь?')
                    if examination:
                        mb.showinfo("ай-яй-яй", 'Не надо')
                        anew()
                elif self.right == 87:
                    """Вся нижняя рамка заполнена, пора поставить оценку и посчитать время выполнения"""
                    self.all = True
                    if self.symbols == self.easy:
                        self.min_sec(self.time_passed)
                    elif self.symbols == self.hard:
                        self.min_sec(211 - self.time_left)
                    if self.error == 0:
                        self.grade = 'Поздравляю, идеально!!!'
                    elif self.error <= 5:
                        self.grade = 'Молодец, отлично!'
                    elif self.error <= 20:
                        self.grade = 'Очень даже хорошо'
                    elif self.error <= 35:
                        self.grade = 'Неплохо'
                    elif self.error <= 50:
                        self.grade = 'Неплохо, но можно и лучше'
                    else:
                        self.grade = 'Надо еще раз попробовать'
                    self.result.config(text=f'{self.grade}\nОшибок: {self.error}\nВремя: '
                                            f'{self.time}\nУровень: {self.level}')
                    """Перезапись рекорда и предыдущего результата + вывод на экран"""
                    save_data = Save()
                    self.last_result.config(text=save_data.get('last_result'))
                    save_data.save()
                    try:
                        best_result = [line for line in save_data.get('best_result').split('\n')]
                        self.record_miss = best_result[1]
                        self.record_time = best_result[2]
                        self.record_level = best_result[3]
                        if self.error <= int(self.record_miss.split(': ')[1]) and \
                                (self.time <= self.record_time.split(': ')[1]):
                            self.record_miss = self.error
                            self.record_time = self.time
                            self.record_level = self.level
                            save_data.change()
                        self.record.config(text=save_data.get('best_result'))
                    except:
                        self.record_miss = self.error
                        self.record_time = self.time
                        self.record_level = self.level
                        save_data.change()
                    """Верхняя рамка больше не нужна, вместо нее рисуется рамка результатов"""
                    self.top_panel.destroy()
                    self.finish.configure(relief="ridge", bd=5)
                    self.finish.pack(fill=BOTH, expand=True)
                    self.last_result.place(x=40, y=100)
                    self.result.place(x=480, y=100)
                    self.record.place(x=920, y=100)
            else:
                """Пользователь ошибся"""
                self.error += 1
                if self.error == 1:
                    self.mistake.config(fg='red')
                self.mistake.config(text=f'Ошибок: {self.error}')
                if self.symbols == self.hard:
                    if self.error == 20:
                        """На сложном уровне можно допустить не больше 20 ошибок """
                        mb.showinfo("Ошибка", f"Вы допустили {self.error} ошибок\nНачать заново?")
                        anew()
                else:
                    if self.error == 87:
                        """На легком уровне можно допустить не больше 87 ошибок """
                        mb.showinfo("Ошибка", f"Вы допустили {self.error} ошибок\nНачать заново?")
                        anew()

    def easy_level(self):
        """Легкий уровень"""
        self.symbols = self.easy
        self.level = 'легко'
        self.progress.place(x=1055, y=225)
        self.start()
        self.stopwatch()

    def hard_level(self):
        """Сложный уровень с таймером """
        self.symbols = self.hard
        self.level = 'сложно'
        self.time_display.place(x=1020, y=200)
        self.progress.place(x=1055, y=270)
        self.start()
        self.timer()

    def stopwatch(self):
        """Сколько прошло времени"""
        if not self.all:
            self.time_passed += 1
            self.root.after(1000, self.stopwatch)

    def timer(self):
        """Сколько осталось времени"""
        if not self.all:
            if self.time_left < 1:
                mb.showinfo("Не успел", 'Время вышло')
                anew()
            self.time_left -= 1
            self.min_sec(self.time_left)
            fg = 'white'
            if self.time_left <= 30 and self.time_left % 2 == 0:
                fg = 'red'
            self.time_display.config(text=f'Осталось {self.time}', fg=fg)
            self.root.after(1000, self.timer)

    def min_sec(self, t):
        """Перевод секунд в минуты и секунды"""
        minute = t // 60
        second = t - (minute * 60)
        if minute < 10:
            minute = '0' + str(minute)
        else:
            minute = str(minute)
        if second < 10:
            second = '0' + str(second)
        else:
            second = str(second)
        self.time = f'{minute}:{second}'


class Save:
    def __init__(self):
        if not os.path.isdir("C:/keyboard"):
            os.mkdir("C:/keyboard")
        self.file = shelve.open("C:/keyboard/data")

    def save(self):
        self.file['last_result'] = f'Предыдущий результат\nОшибок: {keyboard.error}\n' \
                                   f'Время: {keyboard.time}\nУровень: {keyboard.level}'

    def change(self):
        self.file['best_result'] = f'Лучший результат\nОшибок: {keyboard.record_miss}\n' \
                                   f'Время: {keyboard.record_time}\nУровень: {keyboard.record_level}'

    def get(self, name):
        try:
            return self.file[name]
        except:
            pass

    def __del__(self):
        self.file.close()


def anew():
    """Новая игра/заново"""
    global keyboard
    keyboard.root.destroy()
    keyboard = Keyboard(Tk())
    keyboard.root.mainloop()


user = os.getlogin()
keyboard = Keyboard(Tk())
keyboard.root.mainloop()
