from typing import Tuple
import random

def get_task() -> Tuple[str, str]:
    tasks = [("2+2", "4"), ("5+5", "10")]
    return random.choice(tasks)
