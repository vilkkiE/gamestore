from django.core.mail import send_mail

from . import models

MESSAGE = '''
Hello!\n\n

Welcome to our webstore! To be able to use your
account please click the link below!\n
Your username is: {:s}\n\n

http://morning-hollows-34668.herokuapp.com/activate?id={:s}&email={:s}
'''


def send_auth_email(username_string):
    user = models.User.objects.get(username=username_string)
    email_address = user.email
    user_id = user.id*42
    subject = 'Activate your webstore profile now!'
    message = MESSAGE.format(username_string, str(user_id), email_address)
    from_email = 'Kaljamies<eetu.joona.lauri@gmail.com>'
    send_mail(subject, message, from_email, [email_address])
