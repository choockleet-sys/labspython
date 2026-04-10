class Calculator:
    def __init__(self, cost_hours = 6.0):
        self.cost_hours = cost_hours
    def calc_energy(self, power, hours):
        return (power * hours) / 1000
    def calc_cost(self, power, hours):
        energy = self.calc_energy(power, hours)
        return energy * self.cost_hours
