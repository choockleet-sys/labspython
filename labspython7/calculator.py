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

    def __str__(self):
        return f"Калькулятор, тариф: {self.cost_per_kwh} руб./кВт·ч"

    def __repr__(self):
        return f"Calculator(cost_per_kwh={self.cost_per_kwh})"
