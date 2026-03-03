import copy
import pprint
def rec(n, s):
    def b(d):
        if d == 1:
            return [f"level {n}"] * s
        return [b(d - 1) for _ in range(s)]
    def format_ndim(arr, level=0):
        indent = '    ' * level
        if isinstance(arr, list):
            if not arr:
                return indent + '[]'
            if all(not isinstance(e, list) for e in arr):
                return indent + '[' + ', '.join(repr(e) for e in arr) + ']'
            else:
                lines = [indent + '[']
                for i, e in enumerate(arr):
                    lines.append(format_ndim(e, level + 1))
                    if i < len(arr) - 1:
                        lines[-1] += ','
                lines.append(indent + ']')
                return '\n'.join(lines)
        else:
            return indent + repr(arr)
    print(format_ndim(b(n)))



def mas(n, s):
    if n <= 0:
        return []
    a = [f"level {n}"] * s
    for i in range(2, n + 1):
        a = [copy.deepcopy(a) for _ in range(s)]
    def format_ndim(arr, level=0):
        indent = '    ' * level
        if isinstance(arr, list):
            if not arr:
                return indent + '[]'
            if all(not isinstance(e, list) for e in arr):
                return indent + '[' + ', '.join(repr(e) for e in arr) + ']'
            else:
                lines = [indent + '[']
                for i, e in enumerate(arr):
                    lines.append(format_ndim(e, level + 1))
                    if i < len(arr) - 1:
                        lines[-1] += ','
                lines.append(indent + ']')
                return '\n'.join(lines)
        else:
            return indent + repr(arr)
    print(format_ndim(a)) 
    
def format_ndim(arr, level=0):
    indent = '    ' * level
    if isinstance(arr, list):
        if not arr:
            return indent + '[]'
        if all(not isinstance(e, list) for e in arr):
            return indent + '[' + ', '.join(repr(e) for e in arr) + ']'
        else:
            lines = [indent + '[']
            for i, e in enumerate(arr):
                lines.append(format_ndim(e, level + 1))
                if i < len(arr) - 1:
                    lines[-1] += ','
            lines.append(indent + ']')
            return '\n'.join(lines)
    else:
        return indent + repr(arr)

print("Рекурсивный")
rec(4, 2)


print("Нерекурсивный")
mas(4, 2)