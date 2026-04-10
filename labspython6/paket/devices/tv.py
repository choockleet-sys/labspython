class Tv:
     def __init__(self, power):
         self.power = power 
         self.name = "Телевизор"
     def __str__(self):    
          return f"{self.name}: {self.power} Вт"