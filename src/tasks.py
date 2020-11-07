  
from typing import Tuple
import random

k_tpl = tuple([n for n in range(-10, 11) if n != 0])


def get_task() -> Tuple[str, str]:
    functions = (get_linear, get_quadratic)
    return random.choice(functions)()


def get_linear() -> Tuple[str, str]:
    x = random.randint(-50, 50)
    a = random.randint(0, 100)
    k = random.choice(k_tpl)
    b = a + (k * x)
    sign = "+" if k >= 0 else ""
    equation = f"{str(a)+f'{sign}' if a != 0 else ''}{k if k != 1 else ''}x={b}"
    return (equation, str(x))


def get_quadratic() -> Tuple[str, str]:
    a = random.randint(1, 10)
    x1 = random.randint(-10, 10)
    x2 = random.randint(-10, 10)
    b = -1 * a * (x1 + x2)
    c = a * (x1 * x2)
    b_sign = "+" if b > 0 else ""
    c_sign = "+" if c > 0 else ""

    equation = f"{a if a != 1 else ''}x\u00B2{f'{b_sign}'+str(b)+'x' if b != 0 else ''}{f'{c_sign}'+str(c) if c != 0 else ''}=0"
    return (equation, "{} {}".format(*sorted((x1, x2))))
