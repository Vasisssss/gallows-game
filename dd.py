import tkinter as tk
import random

# Слова для игры
WORDS = ["кант", "хроника", "зал", "галера", "балл", "вес", "кафель", "знак", "фильтр", "башня",
               "кондитер", "омар", "чан", "пламя", "банк", "тетерев", "муж", "камбала", "груз",
               "кино", "лаваш", "калач", "геолог", "бальзам", "бревно", "жердь", "борец", "самовар",
               "карабин", "подлокотник", "барак", "мотор", "шарж", "сустав", "амфитеатр", "скворечник",
               "подлодка", "затычка", "ресница", "спичка", "кабан", "муфта", "синоптик", "характер",
               "мафиози", "фундамент", "бумажник", "библиофил", "дрожжи", "развлечение", "конечность",
               "пробор", "дуст", "комбинация", "мешковина", "процессор", "крышка", "сфинкс", "пассатижи",
               "фунт", "кружево", "агитатор", "формуляр", "прокол", "абзац", "караван", "леденец", "кашпо",
               "баркас", "кардан", "вращение", "заливное", "метрдотель", "клавиатура", "радиатор", "сегмент",
               "обещание", "магнитофон", "кордебалет", "заварушка"]


class HangmanGame:
    def __init__(self, master):  #self позволяет получить доступ к атрибутам и методам объекта
        self.master = master
        self.master.title("Игра Виселица") #title - текст
        # self.master.geometry("400x350")
        self.master.attributes('-fullscreen', True)
        self.canvas_width = 200
        self.canvas_height = 200

        self.main_menu()

    def main_menu(self):
        self.clear_screen()
        label = tk.Label(self.master, text="Главное меню", font=("Arial", 18)) #label - статический текст без возможности редактирования. Pack - упаковщик, который имеется у всех виджет объектов(геометрия)
        label.pack(pady=20)

        play_button = tk.Button(self.master, text="Играть", command=self.start_game) #button - кнопка, command - оведенческий паттерн, позволяющий заворачивать запросы или простые операции в объекты.
        play_button.pack(pady=10)

        quit_button = tk.Button(self.master, text="Выйти", command=self.master.quit)
        quit_button.pack(pady=10)

    def start_game(self):#def - блок где лежат функции
        self.clear_screen()#очистка экрана
        self.word = random.choice(WORDS)#выбирается случайное слово из списка
        self.guesses = []
        self.attempts = 9

        self.create_word_display()#создание рабочего экрана
        self.create_guess_display()#создает текст где будут считаться попытки
        self.create_keyboard()#создание клавиатуры
        self.create_used_letters_display()
        self.create_hangman_canvas()

    def create_used_letters_display(self):
        self.used_letters_label = tk.Label(self.master, text="", font=("Arial", 10))
        self.used_letters_label.pack(pady=5)

    def create_word_display(self):
        self.word_label = tk.Label(self.master, text=" ".join("_" * len(self.word)), font=("Arial", 18)) #len -для нахождения длины списка
        self.word_label.pack(pady=10)

    def create_guess_display(self):
        self.guess_label = tk.Label(self.master, text=f"Осталось попыток: {self.attempts}", font=("Arial", 12))
        self.guess_label.pack(pady=5) #считает попытки

    def create_keyboard(self):
        self.keyboard_frame = tk.Frame(self.master)
        self.keyboard_frame.pack() #frame - отображает треугольник и обычно применяется для организации интерфейса в отдельные блоки.

        for letter in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
            button = tk.Button(self.keyboard_frame, text=letter.upper(), width=4, height=2, command=lambda l=letter: self.check_letter(l)) #lambda - аноним функции, объявленные с помощью ключевого слова lambda.
            # grid - здесь функция grid делает сетку и в каждой из отделов сетки, добавляет букву из списка
            button.grid(row=(ord(letter) - ord('а')) // 7, column=(ord(letter) - ord('а')) % 7)

    def check_letter(self, letter):
        if letter not in self.guesses:
            self.guesses.append(letter)
            if letter not in self.word:
                self.attempts -= 1
                self.update_hangman_canvas()
            self.update_word_display()
            self.update_guess_display()
            self.update_used_letters_display()
            self.check_game_over()

    def update_word_display(self):
        displayed_word = [char if char in self.guesses else "_" for char in self.word]
        self.word_label.config(text=" ".join(displayed_word))

    def update_guess_display(self):
        self.guess_label.config(text=f"Осталось попыток: {self.attempts}")

    def update_used_letters_display(self):
        used_letters = ", ".join(sorted(set(self.guesses) - set(self.word)))
        self.used_letters_label.config(text=f"Использованные неправильные буквы: {used_letters}")


    def create_hangman_canvas(self):
        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(pady=10)

    def update_hangman_canvas(self):
        if self.attempts == 8: #если правильно нажал на букву то попытка не отнимается
            self.canvas.create_line(20, self.canvas_height - 20, self.canvas_width - 20, self.canvas_height - 20)
        elif self.attempts == 7:
            self.canvas.create_line(60, 20, 60, self.canvas_height - 20)
        elif self.attempts == 6:
            self.canvas.create_line(60, 20, 130, 20)
        elif self.attempts == 5:
            self.canvas.create_line(130, 20, 130, 50)
        elif self.attempts == 4:
            self.canvas.create_oval(115, 50, 145, 80)
        elif self.attempts == 3:
            self.canvas.create_line(130, 80, 130, 130)
        elif self.attempts == 2:
            self.canvas.create_line(130, 100, 110, 130)
            self.canvas.create_line(130, 100, 150, 130)
        elif self.attempts == 1:
            self.canvas.create_line(130, 130, 110, 150)
            self.canvas.create_line(130, 130, 150, 150)
        elif self.attempts == 0:
            self.canvas.create_line(130, 80, 100, 110)
            self.canvas.create_line(130, 80, 160, 110)
#если не правильно то попытки будут уменьшаться с 9 до 0 и вы проиграете игру
    def check_game_over(self):
        if self.attempts <= 0:
            self.game_over("Поражение! Загаданное слово было: " + self.word) #если попытки были все исчерпаны то будет показано такое сообщение
        elif "_" not in self.word_label.cget("text"):
            self.game_over("Победа! Загаданное слово было: " + self.word) #такое сообщение будет показано при победе

    def game_over(self, message):
        self.clear_screen()
        label = tk.Label(self.master, text=message, font=("Arial", 18))
        label.pack(pady=20)

        play_again_button = tk.Button(self.master, text="Играть снова", command=self.start_game)
        play_again_button.pack(pady=10)

        back_to_menu_button = tk.Button(self.master, text="В главное меню", command=self.main_menu)
        back_to_menu_button.pack(pady=10)

        quit_button = tk.Button(self.master, text="Выйти", command=self.master.quit)
        quit_button.pack(pady=10)
    #после окончания игры очиститься экроан и будут кнопки: играть снова, в главное меню либо выход из игры.
    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
