"""Console bot helper"""

from classes import AddressBook, Record, Name, Phone

# phonebook
contacts = {}


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Enter user name'
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Invalid command format'
    return wrapper


def handle_invalid_command(*_):
    return 'Invalid command format'


def handle_hello(*_):
    return 'How can I help you?'


def handle_end(*_):
    return 'Good bye!'


@input_error
def handle_contact_add(command):
    name, phone = command
    if name not in contacts:
        contacts[name] = phone
        return f'Contact {name} added with phone number {phone}'
    else:
        return f'Contact {name} already exists!'


@input_error
def handle_contact_change(command):
    name, phone = command
    if contacts.get(name):
        contacts[name] = phone
        return f'Phone number for {name} changed to {phone}'
    else:
        return f'Contact {name} not found'


@input_error
def handle_contact_get_by_name(command):
    name = command[0]
    phone = contacts.get(name)
    if phone:
        return f'Phone number for {name} is {phone}'
    else:
        return f'Contact {name} not found'


def handle_contact_get_all(*_):
    if not contacts:
        return 'No contacts found'

    result = '{}{:<26}: {:<15}\n'.format(' ' * 3, 'Name', 'Phone number')
    result += '\n'.join(
        '{}{:<26}: {:<15}'.format(' ' * 3, name, phone)
        for name, phone in contacts.items()
    )

    return result


command_handlers = {
    'hello': handle_hello,
    'good bye': handle_end,
    'close': handle_end,
    'exit': handle_end,
    'add': handle_contact_add,
    'change': handle_contact_change,
    'phone': handle_contact_get_by_name,
    'show all': handle_contact_get_all
}


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


def main():

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


if __name__ == '__main__':
    main()
