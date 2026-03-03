def br(k, x):
    if k == 0:
        return 1/(2*x)
    return br(k-1,x)*x**2
def yr(k,x):
    if k == 0:
        return 1
    return yr(k-1,x) * br(k, x)
print("рекусивный",yr(3, 2.0))

def y(k, x):
    y = 1
    b = 1/(2*x)
    for i in range(1, k+1):
        b *= x**2
        y *= b
    return y
print("нерекусивный", y(3,2.0))