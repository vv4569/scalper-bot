import random
from typing import Literal

alphabetUP = 'QWERTYUIOPASDFGHJKLZXCVBNM'
alphabetLOW = 'qwertyuiopasdfghjklzxcvbnm'
number = '1234567890'
symbol = '!#$%_.+~`<>?'

def random_name_pw(username_digits: str = 12, password_digits: str = 8, requirement: Literal['uppercase', 'symbol', 'both', None] = None) -> list[str, str]:
    """
    Usage:
    Generate randomized username and password

    Arguments:
    username_digits: str = digits of randomized username. Defaults to 12.
    password_digits: str = digits of randomized password. Defaults to 8.
    requirement: list = special requirement on password. Defaults to None.

    Return:
    List[str, str] = [username, password]
    """
    char: str = alphabetUP + alphabetLOW + number + symbol
    result: list[str, str] = ['', '']
    match requirement:
        case 'uppercase':
            result = [random.choice(alphabetUP), random.choice(alphabetUP)]
        case 'symbol':
            result = [random.choice(symbol), random.choice(symbol)]
        case 'both':
            result = [random.choice(alphabetUP) + random.choice(symbol), random.choice(alphabetUP) + random.choice(symbol)]
    
    result[0] += ''.join([random.choice(char) for _ in range(username_digits-len(result[0])) ])
    result[1] += ''.join([random.choice(char) for _ in range(password_digits-len(result[1])) ])

    return result


if __name__ == "__main__":
    print('Test:', random_name_pw())