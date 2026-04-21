# Лабораторная работа №7 (ООП)

**Цель работы:** Переписать приложение для расчёта потребления электроэнергии с использованием классов и объектов: абстрактный базовый класс, иерархия наследования, managed-атрибуты и dunder-методы. GUI-фреймворк заменён с `tkinter` на `Kivy`.

---

## Вывод при расчёте (Утюг, 2 часа, 6.0 руб/кВт·ч):

```
Прибор: Утюг: 1200 Вт
Мощность: 1200 Вт
Время: 2.0 ч

Потребление: 2.40 кВт·ч
Цена за кВт·ч: 6.0 руб.
Итого: 14.40 руб.
```

**Вывод:** Переписал приложение на `Kivy` с применением ООП. Абстрактный базовый класс `ElectricDevice` задаёт общий интерфейс для всех приборов. Классы `Iron`, `Washer` наследуются через `HouseholdAppliance`, класс `Tv` — через `EntertainmentDevice`. Атрибуты `power` и `name` реализованы как managed-атрибуты через `@property` с валидацией. Класс `Calculator` выполняет расчёт энергии и стоимости. Результат сохраняется в `.docx`-файл через библиотеку `python-docx`.

---

## Код

```python
# devices.py — абстрактный базовый класс
from abc import ABC, abstractmethod

class ElectricDevice(ABC):
    def __init__(self, power, name):
        self.power = power
        self.name = name

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        if value <= 0:
            raise ValueError("Мощность должна быть больше 0")
        self._power = value

    @abstractmethod
    def get_description(self):
        pass

    def __str__(self):
        return f"{self.name}: {self.power} Вт"

    def __repr__(self):
        return f"{self.__class__.__name__}(power={self.power})"
```

```python
# devices.py — конкретные классы приборов
class Iron(HouseholdAppliance):
    def __init__(self, power):
        super().__init__(power, "Утюг")

    def get_description(self):
        return f"Утюг, мощность {self.power} Вт"

    def __str__(self):
        return f"Утюг: {self.power} Вт"

    def __repr__(self):
        return f"Iron(power={self.power})"
```

```python
# calculator.py
class Calculator:
    def __init__(self, cost_per_kwh=6.0):
        self.cost_per_kwh = cost_per_kwh

    @property
    def cost_per_kwh(self):
        return self._cost_per_kwh

    @cost_per_kwh.setter
    def cost_per_kwh(self, value):
        if value <= 0:
            raise ValueError("Тариф должен быть больше 0")
        self._cost_per_kwh = value

    def calc_energy(self, power, hours):
        return (power * hours) / 1000

    def calc_cost(self, power, hours):
        energy = self.calc_energy(power, hours)
        return energy * self.cost_per_kwh
```

```python
# main.py (фрагмент — расчёт)
key = self.get_selected_key()
device = self.devices[key]
self.calc.cost_per_kwh = price

energy = self.calc.calc_energy(device.power, hours)
cost = self.calc.calc_cost(device.power, hours)
```

---

## Иерархия классов

```
ElectricDevice (ABC)
├── HouseholdAppliance
│   ├── Iron
│   └── Washer
└── EntertainmentDevice
    └── Tv
```

---

## Использованные источники:

1. [Kivy — документация](https://www.riverbankcomputing.com/static/Docs/Kivy/)
2. [python-docx — документация](https://python-docx.readthedocs.io/en/latest/)
3. [abc — модуль абстрактных базовых классов](https://docs.python.org/3/library/abc.html)
4. `ABC` (Abstract Base Class) — базовый класс из модуля `abc`, который запрещает создавать объекты напрямую и требует реализации абстрактных методов в наследниках.
5. `@property` — декоратор, позволяющий контролировать получение и установку значения атрибута (managed-атрибут).
6. `Kivy` — библиотека для создания графических интерфейсов, более современная альтернатива `tkinter`.
7. `python-docx` — библиотека для создания и редактирования файлов `.docx`, позволяет добавлять заголовки, таблицы и форматированный текст.
