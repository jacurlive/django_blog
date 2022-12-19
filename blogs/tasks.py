from random import randint

from django.core.mail import EmailMessage

from root.settings import EMAIL_HOST_USER


def send_email(email):
    num = randint(1000, 9999)
    res_email = [email]

    email = EmailMessage('subject', f'{num}', EMAIL_HOST_USER, res_email)
    result = email.send()

    return result
