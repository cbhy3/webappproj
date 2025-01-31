import shelve

class Ticket:
    def __init__(self, user, head, body):
        self.user = user
        self.head = head
        self.body = body
        self.status = "Open"
        id = 0
        with shelve.open('tickets') as db:
            id = len(db)
            while True:
                try:
                    db[str(id)]
                    id += 1
                except KeyError:
                    self.id = id
                    db[str(id)] = self
                    break
    def add_reply(self,replied_by, reply_content):
        self.reply = {
            "replied_by": replied_by,
            "reply_content": reply_content
        }
        with shelve.open('tickets') as db:
            db[self.id] = self

    def change_status(self,status):
        if status != 'Open' or status != 'Closed':
            pass
        else:
            self.status = status
            with shelve.open('tickets') as db:
                db[self.id] = self

    def __str__(self):
        return f'{self.user}, {self.head} ,{self.body}'