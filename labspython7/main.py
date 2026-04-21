# Импортируем ABC и abstractmethod для создания абстрактного базового класса
from abc import ABC, abstractmethod


# Абстрактный базовый класс для всех электроприборов
class ElectricDevice(ABC):
    def __init__(self, power, name):
        # Устанавливаем мощность и название через property (с проверкой)
        self.power = power
        self.name = name

    # Геттер для мощности
    @property
    def power(self):
        return self._power

    # Сеттер для мощности — проверяем, что значение больше 0
    @power.setter
    def power(self, value):
        if value <= 0:
            raise ValueError("Мощность должна быть больше 0")
        self._power = value

    # Геттер для названия прибора
    @property
    def name(self):
        return self._name

    # Сеттер для названия — проверяем, что строка не пустая
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Имя не может быть пустым")
        self._name = value

    # Абстрактный метод — каждый наследник обязан его реализовать
    @abstractmethod
    def get_description(self):
        pass

    # Возвращает строку при print(объект)
    def __str__(self):
        return f"{self.name}: {self.power} Вт"

    # Возвращает строку при repr(объект) — для отладки
    def __repr__(self):
        return f"{self.__class__.__name__}(power={self.power})"


# Промежуточный класс для бытовой техники (утюг, стиралка)
class HouseholdAppliance(ElectricDevice):
    def __init__(self, power, name):
        # Вызываем конструктор родительского класса
        super().__init__(power, name)

    # Реализация абстрактного метода
    def get_description(self):
        return f"Бытовой прибор: {self.name}, мощность {self.power} Вт"

    def __str__(self):
        return f"{self.name}: {self.power} Вт"

    def __repr__(self):
        return f"HouseholdAppliance(name={self.name}, power={self.power})"


# Промежуточный класс для развлекательной техники (телевизор)
class EntertainmentDevice(ElectricDevice):
    def __init__(self, power, name):
        super().__init__(power, name)

    # Реализация абстрактного метода
    def get_description(self):
        return f"Развлекательный прибор: {self.name}, мощность {self.power} Вт"

    def __str__(self):
        return f"{self.name}: {self.power} Вт"

    def __repr__(self):
        return f"EntertainmentDevice(name={self.name}, power={self.power})"


# Класс утюга — наследуется от HouseholdAppliance
class Iron(HouseholdAppliance):
    def __init__(self, power):
        # Передаём название "Утюг" в родительский класс
        super().__init__(power, "Утюг")

    def get_description(self):
        return f"Утюг, мощность {self.power} Вт"

    def __str__(self):
        return f"Утюг: {self.power} Вт"

    def __repr__(self):
        return f"Iron(power={self.power})"


# Класс стиральной машины — наследуется от HouseholdAppliance
class Washer(HouseholdAppliance):
    def __init__(self, power):
        super().__init__(power, "Стиральная машина")

    def get_description(self):
        return f"Стиральная машина, мощность {self.power} Вт"

    def __str__(self):
        return f"Стиральная машина: {self.power} Вт"

    def __repr__(self):
        return f"Washer(power={self.power})"


# Класс телевизора — наследуется от EntertainmentDevice
class Tv(EntertainmentDevice):
    def __init__(self, power):
        super().__init__(power, "Телевизор")

    def get_description(self):
        return f"Телевизор, мощность {self.power} Вт"

    def __str__(self):
        return f"Телевизор: {self.power} Вт"

    def __repr__(self):
        return f"Tv(power={self.power})"
