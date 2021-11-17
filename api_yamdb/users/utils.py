from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail


def username_validator(username):
    if username == 'me':
        raise ValidationError('Имя "me" зарезирвировано для системных нужд')


def send_confirmation_code(user):
    send_mail(
        subject='Request of token',
        message=(f'Приятного времени суток!\n'
                 f'username: {user.username}\n'
                 f'confirmation_code: {user.confirmation_code}'),
        from_email=settings.EMAIL_HOST,
        recipient_list=(user.email, ),
    )
