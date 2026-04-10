class Washer:
     def __init__(self, power):
         self.power = power 
         self.name = "Стиральная машина"
     def __str__(self):    
          return f"{self.name}: {self.power} Вт"