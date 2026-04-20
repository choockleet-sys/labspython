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

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Имя не может быть пустым")
        self._name = value

    @abstractmethod
    def get_description(self):
        pass

    def __str__(self):
        return f"{self.name}: {self.power} Вт"

    def __repr__(self):
        return f"{self.__class__.__name__}(power={self.power})"


class HouseholdAppliance(ElectricDevice):
    def __init__(self, power, name):
        super().__init__(power, name)

    def get_description(self):
        return f"Бытовой прибор: {self.name}, мощность {self.power} Вт"

    def __str__(self):
        return f"{self.name}: {self.power} Вт"

    def __repr__(self):
        return f"HouseholdAppliance(name={self.name}, power={self.power})"


class EntertainmentDevice(ElectricDevice):
    def __init__(self, power, name):
        super().__init__(power, name)

    def get_description(self):
        return f"Развлекательный прибор: {self.name}, мощность {self.power} Вт"

    def __str__(self):
        return f"{self.name}: {self.power} Вт"

    def __repr__(self):
        return f"EntertainmentDevice(name={self.name}, power={self.power})"


class Iron(HouseholdAppliance):
    def __init__(self, power):
        super().__init__(power, "Утюг")

    def get_description(self):
        return f"Утюг, мощность {self.power} Вт"

    def __str__(self):
        return f"Утюг: {self.power} Вт"

    def __repr__(self):
        return f"Iron(power={self.power})"


class Washer(HouseholdAppliance):
    def __init__(self, power):
        super().__init__(power, "Стиральная машина")

    def get_description(self):
        return f"Стиральная машина, мощность {self.power} Вт"

    def __str__(self):
        return f"Стиральная машина: {self.power} Вт"

    def __repr__(self):
        return f"Washer(power={self.power})"


class Tv(EntertainmentDevice):
    def __init__(self, power):
        super().__init__(power, "Телевизор")

    def get_description(self):
        return f"Телевизор, мощность {self.power} Вт"

    def __str__(self):
        return f"Телевизор: {self.power} Вт"

    def __repr__(self):
        return f"Tv(power={self.power})"
