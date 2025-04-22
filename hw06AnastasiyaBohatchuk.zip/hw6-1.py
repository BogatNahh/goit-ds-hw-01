from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Record:
    def __init__(self, name: str):
        self.name = Name(name)  
        self.phones = []        

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return
        raise ValueError("Phone number not found.")

    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone_number:
                self.phones[i] = Phone(new_phone_number)
                return
        raise ValueError("Old phone number not found.")

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name, None)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Contact not found.")

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

print("Address Book:")
print(book)

john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print("\nUpdated Record for John:")
print(john)

found_phone = john.find_phone("5555555555")
if found_phone:
    print(f"\nFound phone for {john.name.value}: {found_phone.value}")

book.delete("Jane")
print("\nAddress Book after deleting Jane:")
print(book)
