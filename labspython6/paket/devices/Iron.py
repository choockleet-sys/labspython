class Iron:
     def __init__(self, power):
         self.power = power 
         self.name = "Утюг"
     def __str__(self):    
          return f"{self.name}: {self.power} Вт"