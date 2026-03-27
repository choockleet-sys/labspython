# Вариант 7

**Цель работы:** Сделать генератор для объединения последовательностей по заданной стратегии и свернуть возвращаемые последовательности в зависимости от типа данных в них.

---

## Вывод без фильтрации по типу:

```
[1, 2, 3, 4, 5, 6]
```

## Вывод с фильтрацией и свёрткой по типу:

```
21
Press any key...
```

**Вывод:** Сделал генератор с стратегией `interleave` для объединения последовательностей и применил `reduce` для свёртки результата в зависимости от типа данных (числа — сумма, строки — склейка).

---

## Код

```python
from functools import *

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

print(mr([1, 2, 3], [4, 5, 6]))       # 21
print(mr(["hello"], ["world"]))        # hello world
```

---

## Использованные источники:

1. [Генераторы в Python](https://docs.python.org/3/glossary.html#term-generator)
2. [functools.reduce](https://docs.python.org/3/library/functools.html#functools.reduce)
3. Генератор — это функция, использующая `yield` для пошагового возврата значений, сохраняя своё состояние между вызовами.
4. `interleave` — стратегия объединения, которая чередует элементы из нескольких последовательностей по одному.
5. `reduce` — функция свёртки, которая накапливает результат, применяя функцию к парам элементов слева направо.
