"""Console bot helper"""

from classes import ObjectValidateError, AddressBook, Record


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectValidateError as e:
            return e
        except KeyError:
            return 'Enter user name'
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Invalid command format'
        except PermissionError as e:
            return f'No access rights! {e}'
    return wrapper


def handle_invalid_command(*args):
    return 'Invalid command format'


def handle_hello(*args):
    return 'How can I help you?'


def handle_end(*args):
    return 'Good bye!'


@handle_error
def handle_contact_add(command):
    name, phone, *birthday = command
    record = Record(name)

    record.add_phone(phone)

    if birthday:
        record.set_birthday(str(birthday[0]))

    address_book.add_record(record)

    if birthday:
        return f'Contact {name} added with phone number: {phone} and birthday: ' + str(birthday[0])
    else:
        return f'Contact {name} added with phone number: {phone}'


@handle_error
def handle_contact_change(command):
    name, old_phone, new_phone = command
    record = address_book.find(name)

    if not record:
        return f'Contact {name} not found'

    record.edit_phone(old_phone, new_phone)

    return f'Contact {name}. Phone number {old_phone} changed to {new_phone}'


@handle_error
def handle_contact_get_by_name(command):
    name = command[0]
    record = address_book.find(name)
    if record:
        return str(record)

    return f'Contact {name} not found'


@handle_error
def handle_contact_search(command):
    query = command[0]
    records = address_book.search_full(query)

    if records:
        return f'Founded contacts:\n' + '\n'.join([str(record) for record in records])

    return f'No contacts found for the request "{query}"'


@handle_error
def handle_contact_set_birthday(command):
    name, birthday = command
    record = address_book.find(name)

    if not record:
        return f'Contact {name} not found'

    record.set_birthday(birthday)
    return f'Birthday {birthday} added for contact {name}'


def handle_contact_get_all(*args):
    if not address_book.data:
        return 'No contacts found'

    result = ''
    for page in address_book.iterator():
        result += '\n'.join(str(record) for record in page) + '\n'
    return result


def get_handler(command: str) -> tuple:
    """
    Parse user input data
    :param command: user input
    :return: command handler and list of clean user data
    """
    # prepare user input
    user_command = command.lower().split()
    user_command_data = command.split()

    # try to get handler with one word command
    handler = command_handlers.get(user_command[0])
    # remove command word from user input
    user_data_list = user_command_data[1:]

    # try to get handler with two words command
    if not handler and len(user_command) > 1:
        two_words_command = user_command[0] + ' ' + user_command[1]
        handler = command_handlers.get(two_words_command)
        # remove command words from user input
        user_data_list = user_command_data[2:]

    return (handler, user_data_list) if handler \
        else (handle_invalid_command, None)


command_handlers = {
    'hello': handle_hello,
    'good bye': handle_end,
    'close': handle_end,
    'exit': handle_end,
    'add': handle_contact_add,
    'change': handle_contact_change,
    'phone': handle_contact_get_by_name,
    'birthday': handle_contact_set_birthday,
    'search': handle_contact_search,
    'show all': handle_contact_get_all
}

# initialize phonebook
address_book = AddressBook()
address_book.load_data_from_file()


def main():

    try:
        while True:
            user_input = input('Enter command: ')

            if not user_input:
                print(handle_invalid_command())
                continue

            handler, user_command_data = get_handler(user_input)

            answer = handler(user_command_data)

            print(answer)

            if answer == 'Good bye!':
                break
    finally:
        address_book.save_data_to_file()


if __name__ == '__main__':
    main()
