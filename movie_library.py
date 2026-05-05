import json
import os
from tkinter import *
from tkinter import ttk, messagebox

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("900x500")
        self.root.resizable(True, True)

        # Файл для хранения данных
        self.data_file = "movies.json"
        
        # Список фильмов
        self.movies = []
        
        # Загрузка данных из файла
        self.load_data()
        
        # Создание интерфейса
        self.create_input_frame()
        self.create_filter_frame()
        self.create_table_frame()
        
        # Обновление таблицы
        self.refresh_table()

    def create_input_frame(self):
        """Фрейм для ввода данных фильма"""
        input_frame = LabelFrame(self.root, text="Добавление нового фильма", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Название
        Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Жанр
        Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.genre_entry = Entry(input_frame, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)

        # Год выпуска
        Label(input_frame, text="Год выпуска:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.year_entry = Entry(input_frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)

        # Рейтинг
        Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.rating_entry = Entry(input_frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5)

        # Кнопка добавления
        self.add_button = Button(input_frame, text="Добавить фильм", command=self.add_movie, bg="green", fg="white")
        self.add_button.grid(row=1, column=4, padx=20, pady=5)

    def create_filter_frame(self):
        """Фрейм для фильтрации"""
        filter_frame = LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Фильтр по жанру
        Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.genre_filter = Entry(filter_frame, width=20)
        self.genre_filter.grid(row=0, column=1, padx=5, pady=5)

        # Фильтр по году
        Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.year_filter = Entry(filter_frame, width=10)
        self.year_filter.grid(row=0, column=3, padx=5, pady=5)

        # Кнопка применения фильтра
        self.filter_button = Button(filter_frame, text="Применить фильтр", command=self.refresh_table, bg="blue", fg="white")
        self.filter_button.grid(row=0, column=4, padx=20, pady=5)
        
        # Кнопка сброса фильтра
        self.reset_button = Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter, bg="gray", fg="white")
        self.reset_button.grid(row=0, column=5, padx=5, pady=5)

    def create_table_frame(self):
        """Фрейм для таблицы с фильмами"""
        table_frame = Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Создание таблицы (Treeview)
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Настройка заголовков
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150 if col != "Название" else 250)
        
        # Добавление полосы прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=LEFT, fill="both", expand=True)
        scrollbar.pack(side=RIGHT, fill="y")

    def validate_movie_data(self, title, genre, year, rating):
        """Проверка корректности введенных данных"""
        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр не могут быть пустыми!")
            return False
        
        try:
            year_int = int(year)
            current_year = 2026
            if year_int < 1888 or year_int > current_year:
                messagebox.showerror("Ошибка", f"Год должен быть от 1888 до {current_year}!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return False
        
        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return False
        
        return True

    def add_movie(self):
        """Добавление нового фильма"""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()
        
        if self.validate_movie_data(title, genre, year, rating):
            movie = {
                "title": title,
                "genre": genre,
                "year": int(year),
                "rating": float(rating)
            }
            self.movies.append(movie)
            self.save_data()
            self.refresh_table()
            
            # Очистка полей
            self.title_entry.delete(0, END)
            self.genre_entry.delete(0, END)
            self.year_entry.delete(0, END)
            self.rating_entry.delete(0, END)
            
            messagebox.showinfo("Успех", "Фильм успешно добавлен!")

    def refresh_table(self):
        """Обновление таблицы с учетом фильтров"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получение фильтров
        genre_filter = self.genre_filter.get().strip().lower()
        year_filter = self.year_filter.get().strip()
        
        # Фильтрация фильмов
        filtered_movies = self.movies.copy()
        
        if genre_filter:
            filtered_movies = [m for m in filtered_movies if genre_filter in m["genre"].lower()]
        
        if year_filter:
            try:
                year_int = int(year_filter)
                filtered_movies = [m for m in filtered_movies if m["year"] == year_int]
            except ValueError:
                if year_filter:  # Если введено не число, показываем ошибку
                    messagebox.showwarning("Предупреждение", "Фильтр по году должен быть числом!")
        
        # Сортировка по году (от новых к старым)
        filtered_movies.sort(key=lambda x: x["year"], reverse=True)
        
        # Заполнение таблицы
        for movie in filtered_movies:
            self.tree.insert("", END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))

    def reset_filter(self):
        """Сброс фильтров"""
        self.genre_filter.delete(0, END)
        self.year_filter.delete(0, END)
        self.refresh_table()

    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(self.movies, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as file:
                    self.movies = json.load(file)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
                self.movies = []
        else:
            # Создание примера данных для демонстрации
            self.movies = [
                {"title": "Побег из Шоушенка", "genre": "Драма", "year": 1994, "rating": 9.3},
                {"title": "Крестный отец", "genre": "Криминал", "year": 1972, "rating": 9.2},
                {"title": "Темный рыцарь", "genre": "Боевик", "year": 2008, "rating": 9.0},
                {"title": "Криминальное чтиво", "genre": "Криминал", "year": 1994, "rating": 8.9},
                {"title": "Властелин колец: Возвращение короля", "genre": "Фэнтези", "year": 2003, "rating": 9.0}
            ]
            self.save_data()

if __name__ == "__main__":
    root = Tk()
    app = MovieLibrary(root)
    root.mainloop()