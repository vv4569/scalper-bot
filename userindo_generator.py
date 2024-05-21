from random import choice 
from email_registration import email_registration

alphabetUP = 'QWERTYUIOPASDFGHJKLZXCVBNM'
alphabetLOW = 'qwertyuiopasdfghjklzxcvbnm'
number = '1234567890'
symbol = '!#$%_.+~`<>?'

def random_name_pw(username_digits: str = 12, password_digits: str = 8) -> list[str, str, str, str]:
    """
    Usage:
    Generate randomized username and password.

    Arguments:
    username_digits: str = digits of randomized username. Defaults to 12.
    password_digits: str = digits of randomized password. Defaults to 8.

    Return:
    List[str, str, str, str] = [username, gmail, password, pin8]
    """
    if not isinstance(username_digits, int) or not isinstance(password_digits, int): raise ValueError('username_digits and password_digits have to be integers.')
    if username_digits < 8: raise ValueError('Value of username_digits cannot be less than 8.')
    if password_digits < 8: raise ValueError('Value of password_digits cannot be less than 8.')

    result: list[str, str, str, str] = ['', '', '', '']

    result[0] = choice(alphabetUP + alphabetLOW) + ''.join([choice(alphabetUP + alphabetLOW + number) for _ in range(username_digits-1)])
    result[2] = choice(alphabetUP) + choice(symbol) + choice(number) + ''.join([choice(alphabetLOW) for _ in range(password_digits-3)])
    result[3] = ''.join([choice(number) for _ in range(8)])
    
    if email_registration(name = result[0], password = result[1]) == True:
        result[1] = result[0] + '@outlook.com'

    return result


if __name__ == "__main__":
    test_case = [[12, 12], 
                 [8, 8], 
                 [4, 8], 
                 [1, 2], 
                 [4, 1], 
                 ['p', 9], 
                 [9, 'p'], 
                 ['p', 'p']]
    for num, [ud, pd, pn] in enumerate(test_case):
        print(f'TEST CASE {num}:  ', end='')
        try:
            print(random_name_pw(ud, pd, pn))
        except Exception as e:
            print(e)
