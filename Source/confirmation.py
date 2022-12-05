import os 
from email.message import EmailMessage
import ssl
import smtplib

email_sender = 'skysoarercs50@gmail.com'
email_password = 'crsqtopyamuwnwdm'
email_receiver = 'christopherperez@college.harvard.edu'

subject = 'SkySoarer: Account Created'
body = """
Hey there! Just to let you know, someone has created an account for SkySoarer under your email address. See you in the sky! 
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender,email_receiver, em.as_string())
