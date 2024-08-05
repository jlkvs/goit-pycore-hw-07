from collections import UserDict
from datetime import datetime

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {str(e)}"
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        return phone.isdigit() and len(phone) == 10

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%Y.%m.%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY.MM.DD")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for idx, ph in enumerate(self.phones):
            if ph.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ', '.join(str(phone) for phone in self.phones)
        birthday = self.birthday if self.birthday else "No birthday"
        return f"Contact name: {self.name}, phones: {phones}, birthday: {birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                days_until_birthday = (birthday_this_year - today).days
                if 0 <= days_until_birthday <= days:
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": birthday_this_year.strftime("%Y.%m.%d")
                    })

        return upcoming_birthdays

    def __iter__(self):
        return iter(self.data.values())

@input_error
def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return f"Added birthday {date} for {name}."
    return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value.strftime('%Y.%m.%d')}."
    return "Contact or birthday not found."

@input_error
def birthdays(args, book):
    days = int(args[0])
    upcoming_birthdays = book.get_upcoming_birthdays(days)
    if upcoming_birthdays:
        return "\n".join([f"{item['name']}: {item['birthday']}" for item in upcoming_birthdays])
    return "No upcoming birthdays."

if __name__ == "__main__":
    book = AddressBook()

    users = [
        {"name": "John Doe", "birthday": "1985.08.07", "phones": ["1234567890", "5555555555"]},
        {"name": "Jane Smith", "birthday": "1990.08.10", "phones": ["9876543210"]}
    ]

    for user in users:
        record = Record(user["name"])
        record.add_birthday(user["birthday"])
        for phone in user.get("phones", []):
            record.add_phone(phone)
        book.add_record(record)

    for record in book:
        print(record)

    upcoming_birthdays = book.get_upcoming_birthdays()
    print("Список привітань на цьому тижні:")
    for birthday in upcoming_birthdays:
        print(birthday)

    print(add_birthday(["John Doe", "1985.08.07"], book))

    print(show_birthday(["John Doe"], book))

    print(birthdays(["7"], book))
