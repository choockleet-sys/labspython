from itertools import*
a = ["A", "B", "C", "D", "E"]
c = product(a, repeat = 5)
m = 0
for k in c:
    if k[0] != "E" and k[-1] != "A":
        m += 1
print(m)