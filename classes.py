from datetime import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError(f"Invalid value: {value}")
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError(f"Invalid value: {new_value}")
        self.__value = new_value

    def is_valid(self, new_value):
        return True

    def __eq__(self, other):
        return self.__value == other

    def __ne__(self, other):
        return self.__value == other

    def __str__(self):
        return str(self.__value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)

    def is_valid(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            return False
        return True


class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(birthday)

    def is_valid(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise ValueError('Invalid birthday format. Right birthday like this 28.12.1994')
        else:
            return True


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        if birthday:
            self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        if phone not in self._get_phones_list():
            new_phone = Phone(phone)
            self.phones.append(new_phone)

    def remove_phone(self, phone):
        if phone not in self._get_phones_list():
            raise ValueError("Phone number not found")
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, desired_phone_number):
        for phone in self.phones:
            if phone.value == desired_phone_number:
                return phone

    def _get_phones_list(self) -> list:
        return [phone.value for phone in self.phones]

    def days_to_birthday(self):
        if not self.birthday:
            return
        birthday = datetime.strptime(self.birthday.value, "%d.%m.%Y")
        now = datetime.now()
        next_birthday = datetime(now.year, birthday.month, birthday.day)
        if next_birthday < now:
            next_birthday = datetime(now.year + 1, birthday.month, birthday.day)
        return (next_birthday - now).days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, n=2):
        start = 0
        end = n
        while start < len(self.data):
            yield {name: self.data[name] for name in list(self.data)[start:end]}
            start += n
            end += n


# def main():
#     # Створення нової адресної книги
#     book = AddressBook()
#
#     # Створення запису для John
#     john_record = Record("John", "19.10.2004")
#     john_record.add_phone("1234567890")
#     john_record.add_phone("5555555555")
#     # john_record.add_phone("77777777777")  # не валідний номер телефону
#     # john_record.add_phone("bd2345vxe")  # не валідний номер телефону
#     print(f'print john_record {john_record}')
#
#     # Додавання запису John до адресної книги
#     book.add_record(john_record)
#
#     # Створення та додавання нового запису для Jane
#     jane_record = Record("Jane")
#     jane_record.add_phone("9876543210")
#     book.add_record(jane_record)
#
#     # Виведення всіх записів у книзі
#     for book_record in book.data.values():
#         print(str(book_record))
#
#     # Знаходження та редагування телефону для John
#     john = book.find("John")
#     if john:
#         john.edit_phone("1234567890", "1112223333")
#
#     if john:
#         print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
#
#     # Пошук конкретного телефону у записі John
#     if john:
#         found_phone = john.find_phone("5555555555")
#         print(f"{john.name.value}: {found_phone}")  # Виведення: 5555555555
#         found_phone = john.find_phone("1234567890")
#         print(f"{john.name.value}: {found_phone}")  # Виведення: 5555555555
#
#     # Видалення запису Jane
#     book.delete("Jane")
#
#
# if __name__ == '__main__':
#     main()
