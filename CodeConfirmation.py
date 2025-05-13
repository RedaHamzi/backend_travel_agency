
from email.message import EmailMessage
import ssl
import smtplib
import random
import datetime

def send_confirmation_code(email_receiver):
    code = str(random.randint(100000,999999))
    reset_expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=3)
    email_sender = ' skyvelia54@gmail.com'
    email_password = 'bfrb hzmp uula twhz'
    subject = 'Confirmation of your registration'
    body = "Hello, this is a confirmation email for your registration. Please enter the confirmation code below\n" + code+'\nCordially,'

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    return code, reset_expiry

