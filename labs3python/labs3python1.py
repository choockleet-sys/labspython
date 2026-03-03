import copy
def rec(n, s):
    if n == 1:
        return [f"level {n}"] * s
    r = []
    for i in range(s):
        r.append(rec(n-1,s))
    return r
print("рекусривный",rec(2, 3))


def mas(n, s):
    if n <= 0:
        return []
    a = [f"level {n}"] * s
    for i in range(2, n + 1):
        r = []
        for l in range(s):
            r.append(copy.deepcopy(a))
        a = r
    return a 
print("нерекурсивный",mas(3,2))