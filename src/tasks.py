from typing import Tuple
import random

k_tpl = tuple(n for n in range(-10, 11) if n != 0)

class Task:

    def __init__(self, task, answers_):
        self.task = task
        self.answers = answers_

    def __repr__(self):
        return self.out

    def check_asnwer(self, answers):
        if set(int(i) for i in answers.split()) == self.answers:
            return True
        return False

    @staticmethod
    def get_linear():
        x = random.randint(-50, 50)
        a = random.randint(0, 100)
        k = random.choice(k_tpl)
        b = a + (k * x)
        sign = "+" if k >= 0 else ""
        equation = f"{str(a)+f'{sign}' if a != 0 else ''}{k if abs(k) != 1 else ''}x={b}"
        
        return Task(equation, set(x))


    @staticmethod
    def get_quadratic():
        a = random.randint(1, 10)
        x1 = random.randint(-10, 10)
        x2 = random.randint(-10, 10)
        b = -1 * a * (x1 + x2)
        c = a * (x1 * x2)
        b_sign = "+" if b > 0 else ""
        c_sign = "+" if c > 0 else ""

        equation = f"{a if a != 1 else ''}x\u00B2{f'{b_sign}'+str(b)+'x' if b != 0 else ''}{f'{c_sign}'+str(c) if c != 0 else ''}=0"
        return Task(equation, set(str(x1), str(x2)))
