from collections import UserDict
from datetime import datetime, timedelta

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

    def delete_phone(self, phone):
        self.phones = [ph for ph in self.phones if ph.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for idx, ph in enumerate(self.phones):
            if ph.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone):
        return next((ph for ph in self.phones if ph.value == phone), None)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ', '.join(str(phone) for phone in self.phones)
        birthday = self.birthday if self.birthday else "No birthday"
        return f"Contact name: {self.name}, phones: {phones}, birthday: {birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Contact not found.")

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value
                birthday_this_year = birthday_date.replace(year=today.year)

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

if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("1990.01.01")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("1995.08.10")
    book.add_record(jane_record)

    for record in book:
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)  

    found_phone = john.find_phone("5555555555")
    if found_phone:
        print(f"{john.name}: {found_phone}") 

    book.delete("Jane")
    print("After deleting Jane:")
    for record in book:
        print(record)   

    upcoming_birthdays = book.get_upcoming_birthdays()
    print("Upcoming birthdays:")
    for record in upcoming_birthdays:
        print(record)
