from random import randint

from django.core.mail import EmailMessage

from root.settings import EMAIL_HOST_USER


# def send_email(email):
#     num = randint(10000, 99999)
#     res_email = [email]

#     email = EmailMessage('subject', f'{num}', EMAIL_HOST_USER, res_email)
#     email.send()

#     return num


# def ret(message):
#     return message
