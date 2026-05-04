# Лабораторная работа №8 (ООП)

**Цель работы:** Разработать приложение «Менеджер паролей» с
использованием объектно-ориентированного программирования: классы,
наследование, инкапсуляция, собственные исключения и графический
интерфейс.

------------------------------------------------------------------------

## Вывод при работе программы (пример)

    Запись: Gmail
    Логин: user@gmail.com
    Пароль: ********

    Данные успешно сохранены.

    Запись: Gmail
    Логин: user@gmail.com
    Пароль: ••••••••

    Пароль скопирован в буфер обмена.

**Вывод:** Приложение реализует менеджер паролей с GUI на tkinter.
Используется шифрование данных (Fernet), реализованы классы для хранения
данных, генерации паролей и управления интерфейсом. Применены
пользовательские исключения и принципы ООП.

------------------------------------------------------------------------

## Код

``` python
# собственные исключения
class InvalidPasswordError(Exception):
    pass

class RecordNotFoundError(Exception):
    pass

class EmptyFieldError(Exception):
    pass

class WeakPasswordError(Exception):
    pass

class DuplicateError(Exception):
    pass
```

``` python
# класс хранения
class Storage:

    def __init__(self):
        self.passwords = {}
        self.fernet = None

    def add(self, name, login, password):
        if name in self.passwords:
            raise DuplicateError("Запись уже существует")
        self.passwords[name] = {
            "логин": login,
            "пароль": password
        }
```

``` python
# генератор паролей
class PasswordGenerator:

    @staticmethod
    def generate(length=12):
        import random, string
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))
```

``` python
# использование
self.storage.add(name, login, password)
```

------------------------------------------------------------------------

## Иерархия классов

    App
    ├── Storage
    └── PasswordGenerator

------------------------------------------------------------------------

## Использованные источники:

1.  https://docs.python.org/3/library/tkinter.html\
2.  https://cryptography.io/en/latest/\
3.  https://docs.python.org/3/library/json.html\
4.  https://docs.python.org/3/library/abc.html\
5.  tkinter --- библиотека для создания GUI\
6.  cryptography --- библиотека для шифрования данных\
7.  JSON --- формат хранения данных
