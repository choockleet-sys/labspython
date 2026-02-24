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
            if i > 5:
                break
    else:
        return 0
    return k
for n in [200000040, 200000100, 200000160, 200000220, 200000280]:
    print(f"M({n}) = {m(n)}")

