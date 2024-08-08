from collections import UserDict
from datetime import datetime

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

    def __str__(self):
        phones = ', '.join(str(phone) for phone in self.phones)
        birthday = self.birthday if self.birthday else "No birthday"
        return f"Contact name: {self.name}, phones: {phones}, birthday: {birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        return iter(self.data.values())

# Decorator to handle errors
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            if isinstance(e, KeyError):
                return "This contact does not exist."
            elif isinstance(e, ValueError):
                return "Give me name and phone please."
            elif isinstance(e, IndexError):
                return "Enter user name."
    return inner

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError
    name, phone = args[0], args[1]
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return f"Contact {name} added with phone number {phone}."

@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise ValueError
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.data.get(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Phone number for {name} updated to {new_phone}."
    else:
        raise KeyError

@input_error
def show_phone(args, book):
    if not args:
        raise IndexError
    name = args[0]
    record = book.data.get(name)
    if record:
        phones = ', '.join(str(phone) for phone in record.phones)
        return f"{name}'s phone numbers are: {phones}."
    else:
        raise KeyError

@input_error
def show_all_contacts(_, book):
    if book.data:
        return "\n".join(str(record) for record in book)
    else:
        return "No contacts available."

def parse_input(user_input):
    tokens = user_input.strip().split()
    cmd = tokens[0].lower() if tokens else ""
    args = tokens[1:]
    return cmd, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "show":
            print(show_all_contacts(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
