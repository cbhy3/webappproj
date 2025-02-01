import shelve
from generateOTP import updateTicketStatus
import datetime
class Ticket:
    def __init__(self, user, head, body):
        self.user = user
        self.head = head
        self.body = body
        self.reply = []
        date = datetime.datetime.now()
        self.created_date = date.strftime("%d/%m/%Y")
        id = 0
        with shelve.open('tickets') as db:
            id = len(db)
            while True:
                try:
                    db[str(id)]
                    id += 1
                except KeyError:
                    self.id = id
                    self.change_status('Open')
                    db[str(id)] = self
                    break
    def add_reply(self,replied_by, reply_content):
        self.reply.append({
            "replied_by": replied_by,
            "reply_content": reply_content
        })
        with shelve.open('tickets') as db:
            db[str(self.id)] = self
            updateTicketStatus.sendEmail(email=self.user, ticket=self)


    def change_status(self,status):
        if status != 'Open' and status != 'Closed':
            pass
        else:
            self.status = status
            with shelve.open('tickets') as db:
                db[str(self.id)] = self
                updateTicketStatus.sendEmail(email=self.user, ticket=self)

    def __str__(self):
        return f'{self.user}, {self.head} ,{self.body}'

