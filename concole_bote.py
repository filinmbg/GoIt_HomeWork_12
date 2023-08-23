from collections import UserDict
from datetime import date, datetime
import pickle


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"
    
    # @property
    # def value(self):
    #     return self._value

    # @value.setter
    # def value(self, value):
    #     self._value = value


class Name(Field):
    def __init__(self, value: str) -> None:
        self.value = value


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def phone(self):
        return self.__value

    @phone.setter
    def phone(self, value):
        try:
            value.isdigit()
        except:
            raise ValueError("Please enter a number")
        self.__value = value


class AdressBook(UserDict):
    def dump(self):
        with open(self.file, 'wb') as file:
            pickle.dump((self.last_record_id, self.records), file)
 
    def load(self):
        if not self.file.exists():
            return
        with open(self.file, 'rb') as file:
            self.last_record_id, self.records = pickle.load(file)

    def search(self, search_str: str):
        result = []
        for record_id, record in self.records.items():
            if search_str in record:
                result.append(record_id)
        return resultввввввввлллллллллл

    def add_record(self, record):
        self.data[record.name.value] = record
    
    def delete_record(self, key):
        record = self.data.get(key)
        if record:
            self.data.pop(key)
            return record
           
    def iterator(self, step=2):
        keys = list(self.data.keys())
        for i in range(0, len(keys), step):
            yield [self.data[key] for key in keys[i:i + step]]


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if value:
            try:
                datetime.strptime((value), "%d.%m.%Y")
            except ValueError:
                raise ValueError("Please enter a date as day, moonth, year")
        self.__value = value


class Record:
    def __init__(self, name: str, phones=[], emails=[], birthday=None):
        self.name = name
        self.phone_list = phones
        self.email_list = emails
        self.birthday = birthday

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phone_list:
            self.phone_list.append(phone_number)

    def delete_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number in self.phone_list:
            self.phone_list.remove(phone_number)

    def update_phone(self, phone, new_phone):
        self.phone_list.remove(phone)
        self.phone_list.append(new_phone)

    def days_to_birthday(self):
        if self.birthday:
            start = date.today()
            b_date = datetime.strptime(str(self.birthday), "%d,%m,%y")
            end = date(year=start.year, month=b_date.date.month, day=b_date.date.date)
            days = (end - start).days
            if days < 0: 
                days +=365
                return f"{days} days to the Birthday!"
            elif days == 0:
                return "The birthday is today!"
            else:
                return "Unknown"
    

    def __str__(self) -> str:
        return f'User {self.name} has phone {", ".join([phone.value for phone in self.phone_list])}'


ADDRESSBOOK = AdressBook()


def input_error(inner):
    def wrap(*args):
        try:
            return inner(*args)
        except IndexError:
            return "Give me name and phone please"
        except KeyError:
            return f"This contact wasn`t found"
        except ValueError:
            return "Please enter a valid name and phone number separated by a space"

    return wrap


@input_error
def add_handler(data):  # Функції обробники команд
    name = data[0].title()
    phone = data[1]
    ADDRESSBOOK[name] = phone
    return f"Contact {name} with phone {phone} was saved"


@input_error
def change_handler(data):
    if data[0].title() in ADDRESSBOOK:
        ADDRESSBOOK[data[0].title()] = data[1]
        return f"Phone number for contact {data[0].title()} was changed to {data[1]}"
    else:
        print(f"Contact with name {data[0].title()} isn`t found.")


@input_error
def show_all_handler(data):
    if len(ADDRESSBOOK) == 0:
        return "The phone book is empty"
    text = []
    for name, phone in ADDRESSBOOK.items():
        _ = name.title() + " " + str(phone)
        text.append(_)
        result = ("\n").join(text)
    return f"Contacts list:\n{result}"


@input_error
def show_phone_handler(data):
    name = " ".join(data)
    return ADDRESSBOOK[name.title()]


def exit_handler(*args):
    return "Good bye!"


def hello_handler(*args):
    return "How can I help you?"


@input_error
def command_parser(raw_str: str):  # Парсер команд
    elements = raw_str.split()
    for key, value in COMMANDS.items():
        if elements[0].lower() in value:
            return key(elements[1:])
        for cmd in value:
            if cmd.startswith(elements[0].lower()):
                return key(elements[1:])
    return "Unknown command"


COMMANDS = {
    add_handler: ["add", "+"],
    exit_handler: ["good bye", "close", "exit"],
    hello_handler: ["hello"],
    change_handler: ["change"],
    show_phone_handler: ["phone"],
    show_all_handler: ["show all"],
    Birthday: ["birthday"],
    search: ["search"],
}


def main():  # Цикл запит-відповідь.
    while True:
        user_input = input(">>> ")
        result = command_parser(user_input)
        print(result)
        if result == "Good bye!":
            break


if __name__ == "__main__":
    main()