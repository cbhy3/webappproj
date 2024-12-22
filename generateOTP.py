import random
from mailersend import emails

class generateOTP:
    def __call__(email):
        otp = random.randint(100000, 999999)
        mailer = emails.NewEmail("mlsn.fc2c26b3f492a4d1b8bc5fd6ccffc72f5d157521addd33a0f802b006be703986")

        mail_body = {}

        mail_from = {
            "name": "Tossed Out!",
            "email": "tossedout@trial-z3m5jgrz190ldpyo.mlsender.net",
        }
        recipients = [{
            "name" : "Customer",
            "email" : email,
        }]

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject("Tossed Out! One-Time Password", mail_body)
        mailer.set_html_content(f'<h1 style = "text-align: center">Welcome to Tossed Out!</h1><h2 style = "text-align: center">{otp}</h2><h3 style = "text-align: center">This is your One-Time Password (OTP) for your account. </h3><h6 style = "text-align: center; margin-top: 100px;">This is an automated e-mail. Please do not reply to this message.</h6>', mail_body)

        print(mailer.send(mail_body))
        return otp


class generateOTPforReset(generateOTP):
    def __call__(email):
        otp = random.randint(100000, 999999)
        mailer = emails.NewEmail("mlsn.fc2c26b3f492a4d1b8bc5fd6ccffc72f5d157521addd33a0f802b006be703986")

        mail_body = {}

        mail_from = {
            "name": "Tossed Out!",
            "email": "tossedout@trial-z3m5jgrz190ldpyo.mlsender.net",
        }
        recipients = [{
            "name": "Customer",
            "email": email,
        }]

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject("Tossed Out! One-Time Password", mail_body)
        mailer.set_html_content(
            f'<h1 style = "text-align: center">Tossed Out Account Recovery</h1><h2 style = "text-align: center">{otp}</h2><h3 style = "text-align: center">This is your One-Time Password (OTP) for your account. </h3><h6 style = "text-align: center; margin-top: 100px;">This is an automated e-mail. Please do not reply to this message.</h6>',
            mail_body)

        print(mailer.send(mail_body))
        return otp