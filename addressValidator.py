file = open("address", "r")
thing = file.read().upper()
addresses = thing.split("\n")

class streetValidator:

    @staticmethod
    def validate(street):
        if street.upper() not in addresses:
            return False
        else:
            return True