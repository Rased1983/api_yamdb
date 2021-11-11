import random
import string


def random_code_for_user():
    a  = "!$%^&*()-_=+"
    characters = string.ascii_letters + a + string.digits
    passcode =  "".join(random.choice(characters) for x in range(random.randint(15, 20)))
    return passcode
