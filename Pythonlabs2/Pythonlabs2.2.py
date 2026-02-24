c = 4**511 + 2**511 - 511
d = bin(c)[2:]
m = 0
for k in d:
    if k == "1":
        m+=1
        print(k, m)