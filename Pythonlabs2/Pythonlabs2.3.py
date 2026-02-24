def dl(x):
    d=[]
    for i in range(2, int(x**0.5)+1):
        if x % i == 0:
            d.append(i)
            if i != x // i:
               d.append(x // i)
    return(d)

def m(n):
    dp=dl(n)
    dp.sort()
    k=1
    if len(dp)>=5:
        for i in range (5):
            k *= dp[i]
    else:
        return 0
    return k
c = 0
for n in range (200000000, 3000000000):
    if 0 < m(n) < n:
        c += 1
        print(f"M({n}) = {m(n)}")
        if c > 5:
            break
            

