from functools import*
def gen(*sequences):
    itera = [iter(s) for s in sequences]
    while itera:
        for i in itera[:]:
            try:
                yield next(i)
            except StopIteration:
                itera.remove(i)
def reduc(sequence):
    data = list(sequence)
    if not data:
        return None
    first = data[0]
    if isinstance(first, (int, float)):
        return reduce(lambda acc, x: acc + x, data)
    if isinstance(first, str):
        return reduce(lambda acc, x: f"{acc} {x}", data)
    return data
def mr(*sequences):
    ob = gen(*sequences)
    return reduc(ob)
print(mr(["hello"], ["world"]))