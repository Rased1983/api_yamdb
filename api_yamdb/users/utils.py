from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

import random
import string


def username_validator(username):
    if username == 'me':
        raise ValidationError('Имя "me" зарезирвировано для системных нужд')


def random_code_for_user():
    a = "!$%^&*()-_=+"
    characters = string.ascii_letters + a + string.digits
    passcode = "".join(
        random.choice(characters) for x in range(random.randint(15, 20)))
    return passcode

def send_confirmation_code(user):
    send_mail(
        subject='Request of token',
        message=(f'Приятного времени суток!\n'
                    f'username: {user.username}\n'
                    f'confirmation_code: {user.confirmation_code}'),
        from_email=settings.EMAIL_HOST,
        recipient_list=(user.email, ),
    )
