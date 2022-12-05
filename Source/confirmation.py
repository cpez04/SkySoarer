import os 
from email.message import EmailMessage
import ssl
import smtplib
import random
import emoji

email_sender = 'skysoarercs50@gmail.com'
email_password = 'crsqtopyamuwnwdm'
email_receiver = 'hleong@college.harvard.edu'
code = random.randint(0,999999)

subject = 'SkySoarer: Account Created'
body = "Email Verification code: "+ str(code) + "\nSincerely, SkySoarer " + emoji.emojize(':airplane:')

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender,email_receiver, em.as_string())
