import random
from mailersend import emails
class generateOTP:
    @staticmethod
    def __call__(email):
        otp = random.randint(100000, 999999)
        mailer = emails.NewEmail("mlsn.93ae3ad51cbd77064dbbce49b6ec7b6cef74a480379e24e8dbfdc43564da1798")

        mail_body = {}

        mail_from = {
            "name": "Tossed Out!",
            "email": "tossedout@trial-zr6ke4n39y9lon12.mlsender.net",
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
    @staticmethod
    def __call__(email):
        otp = random.randint(100000, 999999)
        mailer = emails.NewEmail("mlsn.93ae3ad51cbd77064dbbce49b6ec7b6cef74a480379e24e8dbfdc43564da1798")

        mail_body = {}

        mail_from = {
            "name": "Tossed Out!",
            "email": "tossedout@trial-zr6ke4n39y9lon12.mlsender.net",
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


class updateOrderStatus(generateOTP):
    @staticmethod
    def sendEmail(email, order):
        mailer = emails.NewEmail("mlsn.93ae3ad51cbd77064dbbce49b6ec7b6cef74a480379e24e8dbfdc43564da1798")

        mail_body = {}

        mail_from = {
            "name": "Tossed Out!",
            "email": "tossedout@trial-zr6ke4n39y9lon12.mlsender.net",
        }
        recipients = [{
            "name": "Customer",
            "email": email,
        }]

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject("Tossed Out! Order Update", mail_body)
        mailer.set_html_content(
            f'<h1 style= "text-align:center;">Tossed Out!</h1><br><h3 style = "text-align:center;">Your Order Number {order.id} has been updated</h3><p style="text-align:center">Your order has been updated to: {order.status}</p><div style = "text-align:center;"><h4>Your Order:</h4><br><div>{updateOrderStatus.get_products(order)}</div>',
            mail_body)

        print(mailer.send(mail_body))


    @staticmethod
    def get_products(order) -> str:
        result = ""
        for i in order.Products:
            result += f'<strong>{ order.Products[i][0] } x</strong> - { order.Products[i][1].name }</div><div>${ order.Products[i][1].price }</div> <br>'
        print(result)
        return result