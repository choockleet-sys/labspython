import copy
def rec(n, s, k):
    i = "   " * k 
    if k == n-1:
        e = ",".join([f"'level {n}'"] * s)
        print (f"{i}[{e}]", end="")
    else:
        print(f"{i}[")
        for m in range(s):
            rec(n,s,k+1)
            if m < s- 1:
                print(",")
            else:
                print()
        print(f"{i}]", end="")
def mas(n, s):
    st = [(0, 0)]
    while st:
        le, ch = st[-1]
        i = "   " * le
        if le == n - 1:
            el = ",".join([f"'level {n}'"] * s)
            print(f"{i}{el}]", end="")
            st.pop()
            if st:
                if st[-1][1] < s:
                    print(",")
                else:
                    print()
            continue
        if ch == 0:
            print(f'{i}[')
        if ch < s:
            st[-1] = (le, ch+1)
            st.append((le + 1, 0))
        else:
            print(f"{i}]", end="")
            st.pop()
            if st:
                if st[-1][1] < s:
                    print(",")
                else:
                    print()
    print()
print("Рекурсивный")
rec(4, 2, 0)
print()

print("Нерекурсивный")
mas(4, 2)