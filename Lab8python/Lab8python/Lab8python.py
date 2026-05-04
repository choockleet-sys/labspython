import tkinter as tk
from tkinter import messagebox
import json
import os
import base64
import hashlib
import random
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


#  СВОИ ИСКЛЮЧЕНИЯ 
# Нужны, чтобы отличать «наши» ошибки от системных
# и показывать понятные сообщения пользователю.

class InvalidPasswordError(Exception):
    """Неверный мастер-пароль или файл хранилища повреждён."""
    pass

class RecordNotFoundError(Exception):
    """Запись с таким названием не найдена в словаре."""
    pass

class EmptyFieldError(Exception):
    """Обязательное поле (название или пароль) осталось пустым."""
    pass

class WeakPasswordError(Exception):
    """Мастер-пароль короче 6 символов — нельзя, это небезопасно."""
    pass

class DuplicateError(Exception):
    """Попытка добавить запись, которая уже существует."""
    pass


#  КЛАСС ДЛЯ ХРАНЕНИЯ ПАРОЛЕЙ 

class Storage:

    DATA_FILE = "passwords.enc"  # зашифрованный файл с паролями
    SALT_FILE = "salt.bin"       # файл с солью для создания ключа

    def __init__(self):
        # Все записи живут в обычном словаре:
        #   ключ   -> название записи (например "Gmail")
        #   значение -> {"логин": ..., "пароль": ..., "сайт": ...}
        self.passwords = {}
        # Объект шифрования Fernet появится после ввода мастер-пароля
        self.fernet = None

    # Создание нового хранилища 

    def create(self, master_password):
        """
        Вызывается один раз при первом запуске программы.
        1. Проверяет, что мастер-пароль >= 6 символов.
        2. Генерирует случайную соль (16 байт) и сохраняет в SALT_FILE.
        3. Превращает мастер-пароль в ключ (с помощью соли + PBKDF2).
        4. Сохраняет пустое хранилище на диск.
        """
        if len(master_password) < 6:
            raise WeakPasswordError("Мастер-пароль должен быть не менее 6 символов!")

        # os.urandom(16) — криптографически безопасная случайная строка
        salt = os.urandom(16)
        with open(self.SALT_FILE, "wb") as f:
            f.write(salt)

        key = self._derive_key(master_password, salt)
        self.fernet = Fernet(key)   # Готово, теперь можно шифровать / расшифровывать
        self.passwords = {}
        self._save()                # Сохраняем пустой словарь (в зашифрованном виде)

    #  Загрузка существующего хранилища 

    def load(self, master_password):
        """
        Вызывается при входе в программу.
        1. Читает соль из SALT_FILE.
        2. Из мастер-пароля и соли получает ключ.
        3. Пытается расшифровать DATA_FILE, преобразует JSON в словарь.
        4. Если расшифровка не удалась — значит пароль неверный.
        """
        if not os.path.exists(self.SALT_FILE):
            raise InvalidPasswordError("Файл хранилища не найден!")

        with open(self.SALT_FILE, "rb") as f:
            salt = f.read()

        key = self._derive_key(master_password, salt)
        self.fernet = Fernet(key)

        try:
            with open(self.DATA_FILE, "rb") as f:
                encrypted_data = f.read()
            # decrypt() сам проверяет подпись и выбросит исключение,
            # если ключ не подходит или данные испорчены
            decrypted_data = self.fernet.decrypt(encrypted_data)
            self.passwords = json.loads(decrypted_data)
        except Exception:
            raise InvalidPasswordError("Неверный мастер-пароль!")

    # Создание ключа из пароля 

    def _derive_key(self, password, salt):
        """
        PBKDF2HMAC:
        - Берёт пароль и соль.
        - 100 000 раз применяет SHA-256 (это замедляет перебор).
        - На выходе даёт 32 байта ключа.
        - Кодирует в Base64, чтобы Fernet мог его использовать.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,              # 32 байта = 256 бит
            salt=salt,
            iterations=100000       # Достаточно, чтобы перебор был медленным
        )
        key = kdf.derive(password.encode())
        # Fernet требует ключ в виде Base64-строки
        return base64.urlsafe_b64encode(key)

    #  Сохранение на диск 

    def _save(self):
        """
        Превращает словарь self.passwords в JSON,
        шифрует его текущим ключом и записывает в DATA_FILE.
        Вызывается после каждого изменения (добавление, удаление).
        """
        # ensure_ascii=False чтобы корректно сохранять кириллицу
        data = json.dumps(self.passwords, ensure_ascii=False).encode()
        encrypted = self.fernet.encrypt(data)
        with open(self.DATA_FILE, "wb") as f:
            f.write(encrypted)

    # Операции с записями 

    def add(self, name, login, password, website=""):
        """Добавляет новую запись, проверяет поля и уникальность."""
        if name.strip() == "":
            raise EmptyFieldError("Поле 'Название' не может быть пустым!")
        if password.strip() == "":
            raise EmptyFieldError("Поле 'Пароль' не может быть пустым!")
        if name in self.passwords:
            raise DuplicateError(f"Запись '{name}' уже существует!")

        # Каждая запись — это вложенный словарь внутри self.passwords
        self.passwords[name] = {
            "логин": login,
            "пароль": password,
            "сайт": website
        }
        self._save()

    def delete(self, name):
        """Удаляет запись по названию."""
        if name not in self.passwords:
            raise RecordNotFoundError(f"Запись '{name}' не найдена!")
        del self.passwords[name]
        self._save()

    def get(self, name):
        """Возвращает полную информацию о записи (логин, пароль, сайт)."""
        if name not in self.passwords:
            raise RecordNotFoundError(f"Запись '{name}' не найдена!")
        return self.passwords[name]

    def get_all_names(self):
        """Возвращает отсортированный список названий всех записей."""
        return sorted(self.passwords.keys())

    def exists(self):
        """Проверяет, создано ли уже хранилище на диске."""
        return os.path.exists(self.DATA_FILE) and os.path.exists(self.SALT_FILE)


#  КЛАСС ГЕНЕРАТОРА ПАРОЛЕЙ 

class PasswordGenerator:

    @staticmethod
    def generate(length=12, special_chars=True):
        """
        Создаёт случайный пароль заданной длины.
        Использует буквы (A-Z, a-z), цифры и, если нужно, спецсимволы.
        random.choice() выбирает случайный символ из набора.
        """
        chars = string.ascii_letters + string.digits
        if special_chars:
            chars += "!@#$%^&*"
        # Генераторное выражение — короткий способ создать строку из случайных символов
        password = "".join(random.choice(chars) for _ in range(length))
        return password


# ГЛАВНОЕ ОКНО 
# Управляет всеми экранами и диалогами.

class App:

    def __init__(self):
        # Создаём «мозг» (хранилище) и генератор
        self.storage = Storage()
        self.generator = PasswordGenerator()
        self.selected_record = ""   # Какая запись выбрана сейчас

        # Главное окно Tkinter
        self.window = tk.Tk()
        self.window.title("Менеджер паролей")
        self.window.geometry("700x500")
        self.window.resizable(False, False)   # Фиксированный размер

        # Если файлы хранилища уже есть — показываем экран входа,
        # иначе — экран создания мастер-пароля
        if self.storage.exists():
            self._login_screen()
        else:
            self._create_screen()

    #  Утилита: полная очистка окна 

    def _clear_window(self):
        """Удаляет все виджеты из окна, чтобы нарисовать новый экран."""
        for widget in self.window.winfo_children():
            widget.destroy()

    # Экран создания мастер-пароля 

    def _create_screen(self):
        """
        Показывается при первом запуске.
        Два поля для пароля, проверка на совпадение,
        минимальная длина 6 символов.
        """
        self._clear_window()

        tk.Label(self.window, text="Создайте мастер-пароль",
                 font=("Arial", 16, "bold")).pack(pady=30)
        tk.Label(self.window,
                 text="Этот пароль будет защищать все ваши пароли.\n"
                      "Запомните его — восстановить нельзя!",
                 font=("Arial", 10), justify="center").pack()

        tk.Label(self.window, text="Мастер-пароль (мин. 6 символов):",
                 font=("Arial", 10)).pack(pady=(20, 2))
        entry1 = tk.Entry(self.window, show="*", font=("Arial", 12), width=25)
        entry1.pack()

        tk.Label(self.window, text="Повторите пароль:",
                 font=("Arial", 10)).pack(pady=(10, 2))
        entry2 = tk.Entry(self.window, show="*", font=("Arial", 12), width=25)
        entry2.pack()

        message = tk.Label(self.window, text="", fg="red", font=("Arial", 10))
        message.pack(pady=5)

        def create():
            p1 = entry1.get()
            p2 = entry2.get()
            if p1 != p2:
                message.config(text="Пароли не совпадают!")
                return
            try:
                self.storage.create(p1)             # Создаём хранилище
                self._main_screen()                 # Переходим в главное окно
            except WeakPasswordError as e:
                message.config(text=str(e))

        tk.Button(self.window, text="Создать", font=("Arial", 12),
                  command=create, width=15).pack(pady=10)

    #  Экран входа

    def _login_screen(self):
        """
        Показывается, если хранилище уже существует.
        Одно поле для ввода мастер-пароля.
        """
        self._clear_window()

        tk.Label(self.window, text="🔐 Менеджер паролей",
                 font=("Arial", 18, "bold")).pack(pady=40)
        tk.Label(self.window, text="Введите мастер-пароль:",
                 font=("Arial", 11)).pack()

        entry = tk.Entry(self.window, show="*", font=("Arial", 13), width=25)
        entry.pack(pady=8)
        entry.focus_set()   # Курсор сразу в поле ввода

        message = tk.Label(self.window, text="", fg="red", font=("Arial", 10))
        message.pack()

        def login():
            try:
                self.storage.load(entry.get())      # Пытаемся расшифровать
                self._main_screen()                 # Успешно — в главное окно
            except InvalidPasswordError as e:
                message.config(text=str(e))

        # Enter на клавиатуре тоже вызывает вход
        entry.bind("<Return>", lambda e: login())
        tk.Button(self.window, text="Войти", font=("Arial", 12),
                  command=login, width=15).pack(pady=5)

    #  Главный экран

    def _main_screen(self):
  
        self._clear_window()

        #  Верхняя панель 
        top = tk.Frame(self.window)
        top.pack(fill="x", padx=10, pady=5)
        tk.Label(top, text="🔐 Менеджер паролей",
                 font=("Arial", 13, "bold")).pack(side="left")
        tk.Button(top, text="Выйти", command=self._login_screen,
                  font=("Arial", 9)).pack(side="right")

        # Разделительная линия
        tk.Frame(self.window, height=1, bg="gray").pack(fill="x")

        # Основная область
        base = tk.Frame(self.window)
        base.pack(fill="both", expand=True, padx=10, pady=8)

        # Левая колонка: список записей 
        left = tk.Frame(base, width=220)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)  # Запрещаем фрейму сжиматься под содержимое

        tk.Label(left, text="Мои записи:", font=("Arial", 10, "bold")).pack(anchor="w")

        # Поле поиска в реальном времени
        search_var = tk.StringVar()
        tk.Entry(left, textvariable=search_var, font=("Arial", 10)).pack(fill="x", pady=3)

        # Список записей с прокруткой
        scrollbar = tk.Scrollbar(left)
        scrollbar.pack(side="right", fill="y")
        self.listbox = tk.Listbox(left, font=("Arial", 10),
                                  yscrollcommand=scrollbar.set,
                                  selectmode="single")
        self.listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)  # Клик по элементу

        # Логика поиска: фильтрует список при каждом изменении текста
        def update_search(*args):
            query = search_var.get().lower()
            self.listbox.delete(0, "end")
            for name in self.storage.get_all_names():
                if query in name.lower():
                    self.listbox.insert("end", name)

        # trace вызывает update_search каждый раз, когда меняется search_var
        search_var.trace("w", update_search)

        tk.Button(left, text="+ Добавить запись",
                  command=self._add_dialog,
                  font=("Arial", 10)).pack(fill="x", pady=4)

        #  Правая колонка: детали записи 
        right = tk.Frame(base, padx=15)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Детали записи",
                 font=("Arial", 11, "bold")).grid(row=0, column=0,
                 columnspan=2, sticky="w", pady=(0, 8))

        labels = ["Название:", "Логин:", "Пароль:", "Сайт:"]
        self.value_fields = {}   # Словарь: подпись -> StringVar

        for i, text in enumerate(labels):
            tk.Label(right, text=text, font=("Arial", 10),
                     width=10, anchor="w").grid(row=i+1, column=0,
                     sticky="w", pady=4)
            var = tk.StringVar()
            self.value_fields[text] = var

            # Поле «Пароль» особенное: скрыто, есть кнопки показать/копировать
            if text == "Пароль:":
                password_frame = tk.Frame(right)
                password_frame.grid(row=i+1, column=1, sticky="w")
                self.password_label = tk.Label(password_frame,
                                               textvariable=var,
                                               font=("Arial", 10), width=22,
                                               anchor="w")
                self.password_label.pack(side="left")
                self._password_visible = False
                tk.Button(password_frame, text="👁",
                          command=self._show_password,
                          font=("Arial", 9)).pack(side="left", padx=4)
                tk.Button(password_frame, text="Копировать",
                          command=self._copy_password,
                          font=("Arial", 9)).pack(side="left")
            else:
                tk.Label(right, textvariable=var,
                         font=("Arial", 10), width=28,
                         anchor="w").grid(row=i+1, column=1, sticky="w")

        # Пустая строка для отступа перед кнопками
        tk.Frame(right, height=10).grid(row=6, column=0)

        # Кнопки «Изменить» и «Удалить»
        buttons = tk.Frame(right)
        buttons.grid(row=7, column=0, columnspan=2, sticky="w")
        tk.Button(buttons, text="✏ Изменить",
                  command=self._edit_dialog,
                  font=("Arial", 10)).pack(side="left", padx=(0, 8))
        tk.Button(buttons, text="🗑 Удалить",
                  command=self._delete_record,
                  fg="red", font=("Arial", 10)).pack(side="left")

        # Строка статуса (внизу окна)
        self.status = tk.Label(self.window, text="", fg="green",
                                font=("Arial", 9))
        self.status.pack(pady=3)

        # Заполняем список записей
        self._update_list()

    # Обновление списка записей 

    def _update_list(self):
        """Очищает и заново заполняет Listbox всеми названиями."""
        self.listbox.delete(0, "end")
        for name in self.storage.get_all_names():
            self.listbox.insert("end", name)

    #  Выбор записи в списке 

    def _on_select(self, event=None):
        """
        Когда пользователь кликает по записи в списке —
        достаём её данные из хранилища и заполняем правую панель.
        """
        selection = self.listbox.curselection()
        if not selection:
            return
        name = self.listbox.get(selection[0])
        self.selected_record = name
        try:
            record = self.storage.get(name)
            self.value_fields["Название:"].set(name)
            self.value_fields["Логин:"].set(record["логин"])
            self.value_fields["Сайт:"].set(record["сайт"])
            # Пароль всегда сначала скрыт
            self._password_visible = False
            self.value_fields["Пароль:"].set("••••••••")
        except RecordNotFoundError as e:
            messagebox.showerror("Ошибка", str(e))

    #  Показать/скрыть пароль

    def _show_password(self):
        """Переключает видимость пароля между звёздочками и текстом."""
        if not self.selected_record:
            return
        try:
            record = self.storage.get(self.selected_record)
            self._password_visible = not self._password_visible
            if self._password_visible:
                self.value_fields["Пароль:"].set(record["пароль"])
            else:
                self.value_fields["Пароль:"].set("••••••••")
        except RecordNotFoundError as e:
            messagebox.showerror("Ошибка", str(e))

    #  Копирование пароля 

    def _copy_password(self):
        """Копирует пароль выбранной записи в буфер обмена."""
        if not self.selected_record:
            return
        try:
            record = self.storage.get(self.selected_record)
            self.window.clipboard_clear()
            self.window.clipboard_append(record["пароль"])
            # Показываем уведомление на 3 секунды
            self.status.config(text="Пароль скопирован в буфер обмена!")
            self.window.after(3000, lambda: self.status.config(text=""))
        except RecordNotFoundError as e:
            messagebox.showerror("Ошибка", str(e))

    #  Удаление записи 

    def _delete_record(self):
        """Удаляет выбранную запись после подтверждения."""
        if not self.selected_record:
            messagebox.showwarning("Внимание", "Сначала выберите запись!")
            return
        answer = messagebox.askyesno("Удалить",
                    f"Удалить запись '{self.selected_record}'?")
        if not answer:
            return
        try:
            self.storage.delete(self.selected_record)
            self.selected_record = ""
            # Очищаем все поля справа
            for var in self.value_fields.values():
                var.set("")
            self._update_list()
        except RecordNotFoundError as e:
            messagebox.showerror("Ошибка", str(e))

    #  Диалог добавления записи 

    def _add_dialog(self):
     
        dialog = tk.Toplevel(self.window)       # Дочернее окно
        dialog.title("Новая запись")
        dialog.geometry("350x320")
        dialog.resizable(False, False)
        dialog.grab_set()   # Захватывает фокус, пока окно открыто

        tk.Label(dialog, text="Добавить новую запись",
                 font=("Arial", 12, "bold")).pack(pady=10)

        # Создаём поля ввода
        entry_fields = {}
        for label in ["Название *", "Логин *", "Пароль *", "Сайт"]:
            tk.Label(dialog, text=label + ":",
                     font=("Arial", 10), anchor="w").pack(fill="x", padx=20)
            field = tk.Entry(dialog, font=("Arial", 10),
                            show="*" if "Пароль" in label else "")
            field.pack(fill="x", padx=20, pady=2)
            entry_fields[label] = field

        # Кнопка-генератор пароля
        gen_frame = tk.Frame(dialog)
        gen_frame.pack(padx=20, pady=3, fill="x")
        tk.Button(gen_frame, text="⚡ Сгенерировать пароль",
                  font=("Arial", 9),
                  command=lambda: (
                      # Очищаем поле и вставляем сгенерированный пароль
                      entry_fields["Пароль *"].delete(0, "end"),
                      entry_fields["Пароль *"].insert(0,
                          self.generator.generate())
                  )).pack(side="left")

        message = tk.Label(dialog, text="", fg="red", font=("Arial", 9))
        message.pack()

        def save():
            try:
                # Передаём данные в хранилище
                self.storage.add(
                    name=entry_fields["Название *"].get(),
                    login=entry_fields["Логин *"].get(),
                    password=entry_fields["Пароль *"].get(),
                    website=entry_fields["Сайт"].get()
                )
                dialog.destroy()        # Закрываем окно
                self._update_list()     # Обновляем список в главном окне
            except (EmptyFieldError, DuplicateError) as e:
                message.config(text=str(e))

        tk.Button(dialog, text="Сохранить", font=("Arial", 11),
                  command=save, width=15).pack(pady=8)

    # Диалог редактирования записи 

    def _edit_dialog(self):

        if not self.selected_record:
            messagebox.showwarning("Внимание", "Сначала выберите запись!")
            return

        try:
            old_record = self.storage.get(self.selected_record)
        except RecordNotFoundError as e:
            messagebox.showerror("Ошибка", str(e))
            return

        dialog = tk.Toplevel(self.window)
        dialog.title("Редактировать запись")
        dialog.geometry("350x280")
        dialog.resizable(False, False)
        dialog.grab_set()

        tk.Label(dialog, text="Редактировать запись",
                 font=("Arial", 12, "bold")).pack(pady=10)

        entry_fields = {}
        data = {
            "Логин": old_record["логин"],
            "Пароль": old_record["пароль"],
            "Сайт": old_record["сайт"]
        }

        # Создаём поля и сразу вставляем старые значения
        for label, value in data.items():
            tk.Label(dialog, text=label + ":",
                     font=("Arial", 10), anchor="w").pack(fill="x", padx=20)
            field = tk.Entry(dialog, font=("Arial", 10),
                            show="*" if label == "Пароль" else "")
            field.insert(0, value)
            field.pack(fill="x", padx=20, pady=2)
            entry_fields[label] = field

        message = tk.Label(dialog, text="", fg="red", font=("Arial", 9))
        message.pack()

        def save():
            try:
                # Так как название — это ключ, мы удаляем старую запись
                # и создаём новую с тем же названием, но новыми данными
                self.storage.delete(self.selected_record)
                self.storage.add(
                    name=self.selected_record,
                    login=entry_fields["Логин"].get(),
                    password=entry_fields["Пароль"].get(),
                    website=entry_fields["Сайт"].get()
                )
                dialog.destroy()
                self._update_list()
                self._on_select()   # Заново выделяем запись в списке
            except (EmptyFieldError, RecordNotFoundError) as e:
                message.config(text=str(e))

        tk.Button(dialog, text="Сохранить", font=("Arial", 11),
                  command=save, width=15).pack(pady=8)

    # Запуск приложения 

    def run(self):
        self.window.mainloop()


# ЗАПУСК

if __name__ == "__main__":
    app = App()
    app.run()