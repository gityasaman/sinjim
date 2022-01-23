import random
from django.conf import settings
from django.core.mail import send_mail
from random import choice

def generate_code():

    seeds = "1234567890"
    random_str = []
    for i in range(6):
        random_str.append(choice(seeds))
    return "".join(random_str)

def send_verification_mail(email, code):
    
    subject = 'Sinjim verification code'
    message = f'Your verification code:\n{code}\nThanks for using sinjim.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list=[email, ]
    send_mail(subject, message, from_email, recipient_list)


