import random
import shelve

from mailersend import emails
class generateOTP:
    @staticmethod
    def __call__(email):
        otp = random.randint(100000, 999999)
        mailer = emails.NewEmail("mlsn.09be3e7396b1e6326e1e88fb1917190f1dcb2c35e55991c736a52b1d8810aaf8")
        mail_body = {}

        mail_from = {
            "name": "Tossed Out!",
            "email": "tossedout@trial-vywj2lpr3oq47oqz.mlsender.net ",
        }
        recipients = [{
            "name" : "Customer",
            "email" : email,
        }]

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject("Tossed Out! One-Time Password", mail_body)
        mailer.set_html_content(f"""<style>body{{font-family:'Arial',sans-serif;background:#f4f4f9;margin:0;padding:0;color:#333}}.container{{max-width:600px;margin:40px auto;padding:20px;background:#fff;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.1);text-align:center}}h1{{font-size:24px;color:#2c3e50;margin-bottom:10px}}h2{{font-size:32px;color:#3498db;margin:20px 0;padding:10px;background:#ecf5ff;border-radius:6px;display:inline-block}}h3{{font-size:16px;color:#666;margin-bottom:30px}}.footer{{margin-top:40px;font-size:12px;color:#999}}</style><body><div class="container"><h1>Welcome to Tossed Out!</h1><h2>{otp}</h2><h3>This is your One-Time Password (OTP) for your account.</h3><div class="footer">This is an automated e-mail. Please do not reply to this message.</div></div></body>""", mail_body)

        print(mailer.send(mail_body))
        return otp


class generateOTPforReset(generateOTP):
    @staticmethod
    def __call__(email):
        otp = random.randint(100000, 999999)
        mailer = emails.NewEmail("mlsn.09be3e7396b1e6326e1e88fb1917190f1dcb2c35e55991c736a52b1d8810aaf8")
        mail_body = {}

        mail_from = {
            "name": "Tossed Out!",
            "email": "tossedout@trial-vywj2lpr3oq47oqz.mlsender.net ",
        }
        recipients = [{
            "name": "Customer",
            "email": email,
        }]

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject("Tossed Out! One-Time Password", mail_body)
        mailer.set_html_content(
            f"""<style>body{{font-family:'Arial',sans-serif;background:#f4f4f9;margin:0;padding:0;color:#333}}.container{{max-width:600px;margin:40px auto;padding:20px;background:#fff;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.1);text-align:center}}h1{{font-size:24px;color:#2c3e50;margin-bottom:10px}}h2{{font-size:32px;color:#3498db;margin:20px 0;padding:10px;background:#ecf5ff;border-radius:6px;display:inline-block}}h3{{font-size:16px;color:#666;margin-bottom:30px}}.footer{{margin-top:40px;font-size:12px;color:#999}}</style><body><div class="container"><h1>Tossed Out! Account Recovery</h1><h2>{otp}</h2><h3>This is your One-Time Password (OTP) for your account.</h3><div class="footer">This is an automated e-mail. Please do not reply to this message.</div></div></body>""",mail_body)

        print(mailer.send(mail_body))
        return otp


class updateOrderStatus(generateOTP):
    @staticmethod
    def sendEmail(email, order):
        mailer = emails.NewEmail("mlsn.09be3e7396b1e6326e1e88fb1917190f1dcb2c35e55991c736a52b1d8810aaf8")
        mail_body = {}

        mail_from = {
            "name": "Tossed Out!",
            "email": "tossedout@trial-vywj2lpr3oq47oqz.mlsender.net ",
        }
        recipients = [{
            "name": "Customer",
            "email": email,
        }]

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject("Tossed Out! Order Update", mail_body)
        mailer.set_html_content(
            f"""
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 0;
                    color: #333;
                    text-align: center;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    font-size: 28px;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }}
                h3 {{
                    font-size: 20px;
                    color: #555;
                    margin-bottom: 15px;
                }}
                p {{
                    font-size: 16px;
                    color: #444;
                    margin-bottom: 20px;
                }}
                .order-summary {{
                    text-align: left;
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 6px;
                    margin-top: 15px;
                }}
                .order-item {{
                    display: flex;
                    justify-content: space-between;
                    padding: 8px 0;
                    border-bottom: 1px solid #ddd;
                }}
                .order-item:last-child {{
                    border-bottom: none;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 12px;
                    color: #777;
                }}
            </style>

            <body>
                <div class="container">
                    <h1>Tossed Out!</h1>
                    <h3>Your Order Number {order.id} has been updated</h3>
                    <p>Your order status is now: <strong>{order.status}</strong></p>

                    <div class="order-summary">
                        <h4>Order Summary:</h4>
                        {updateOrderStatus.get_products(order)}
                    </div>

                    <div class="footer">
                        This is an automated email. Please do not reply.
                    </div>
                </div>
            </body>
            """, mail_body)

        print(mailer.send(mail_body))


    @staticmethod
    def get_products(order) -> str:
        result = ""
        for i in order.Products:
            result += f"""
        <div class="order-item">
            <div><strong>{order.Products[i][0]} x</strong> {order.Products[i][1].name}</div>
            <div>${order.Products[i][1].price:.2f}</div>
        </div>
        """
        print(result)
        return result


#email for tickets
class updateTicketStatus(generateOTP):
    @staticmethod
    def sendEmail(email, ticket):
        print("sending")
        mailer = emails.NewEmail("mlsn.09be3e7396b1e6326e1e88fb1917190f1dcb2c35e55991c736a52b1d8810aaf8")

        mail_body = {}

        mail_from = {
            "name": "Tossed Out!",
            "email": "tossedout@trial-vywj2lpr3oq47oqz.mlsender.net ",
        }
        recipients = [{
            "name": "Customer",
            "email": email,
        }]

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject(f"An update on your support request", mail_body)
        mailer.set_html_content(
            f"""
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 0;
                    color: #333;
                    text-align: center;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    font-size: 28px;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }}
                h3 {{
                    font-size: 20px;
                    color: #555;
                    margin-bottom: 15px;
                }}
                p {{
                    font-size: 16px;
                    color: #444;
                    margin-bottom: 20px;
                }}
                .ticket-summary {{
                    text-align: left;
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 6px;
                    margin-top: 15px;
                }}
                .ticket-section {{
                    padding: 10px;
                    border-bottom: 1px solid #ddd;
                }}
                .ticket-section:last-child {{
                    border-bottom: none;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 12px;
                    color: #777;
                }}
            </style>

            <body>
                <div class="container">
                    <h1>Tossed Out!</h1>
                    <h3>Your Ticket Number {ticket.id} has been updated</h3>
                    <p>Your ticket status is now: <strong>{ticket.status}</strong></p>

                    <div class="ticket-summary">
                        <h4>Ticket Details:</h4>
                        {updateTicketStatus.get_ticket(ticket)}
                    </div>

                    <div class="footer">
                        This is an automated email. Please do not reply.
                    </div>
                </div>
            </body>
            """,  mail_body)

        print(mailer.send(mail_body))


    @staticmethod
    def get_ticket(ticket) -> str:
        result = f"""
            <div class="ticket-section">
                <h2>{ticket.head}</h2>
                <p>{ticket.body}</p>
            </div>
            """

        if ticket.reply:
            for replies in ticket.reply:
                result += f"""
                    <div class="ticket-section">
                        <h3>Replied By: {replies['replied_by']}</h3>
                        <p>{replies['reply_content']}</p>
                    </div>
                    """
        return result