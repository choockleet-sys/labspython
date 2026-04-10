# Лабораторная работа №6

**Цель работы:** Создать приложение с графическим интерфейсом для расчёта потребления электроэнергии бытовыми приборами, используя пакеты, классы и сохранение результата в отчёт Word.

---

## Вывод при расчёте (Утюг, 2 часа, 6.0 руб/кВт·ч):

```
Прибор: Утюг: 1200 Вт
Мощность: 1200Вт
Время использования: 2.0 часов

Потребление энергии: 2.40 кВт·ч
Цена за кВт·ч: 6.0 руб.
Общая стоимость: 14.40 руб.
```

**Вывод:** Создал GUI-приложение на `tkinter` с пакетной структурой. Классы `Iron`, `Tv`, `Washer` описывают приборы, класс `Calculator` выполняет расчёт энергии и стоимости. Результат сохраняется в `.docx`-файл с таблицей через библиотеку `python-docx`.

---

## Код

```python
# paket/calculator.py
class Calculator:
    def __init__(self, cost_hours=6.0):
        self.cost_hours = cost_hours

    def calc_energy(self, power, hours):
        return (power * hours) / 1000

    def calc_cost(self, power, hours):
        energy = self.calc_energy(power, hours)
        return energy * self.cost_hours
```

```python
# paket/devices/Iron.py
class Iron:
    def __init__(self, power):
        self.power = power
        self.name = "Утюг"

    def __str__(self):
        return f"{self.name}: {self.power} Вт"
```

```python
# labspython6.py (фрагмент — расчёт)
device = self.devices[device_key]
self.calc.cost_hours = price

energy = self.calc.calc_energy(device.power, hours)
cost = self.calc.calc_cost(device.power, hours)
```

---

## Использованные источники:

1. [tkinter — документация Python](https://docs.python.org/3/library/tkinter.html)
2. [python-docx — документация](https://python-docx.readthedocs.io/en/latest/)
3. [Пакеты в Python](https://docs.python.org/3/tutorial/modules.html#packages)
4. Пакет — это папка с файлом `__init__.py`, которая позволяет группировать модули и импортировать их как единое целое.
5. `tkinter` — стандартная библиотека Python для создания графических интерфейсов (окна, кнопки, поля ввода).
6. `python-docx` — библиотека для создания и редактирования файлов `.docx`, позволяет добавлять заголовки, таблицы и форматированный текст.
