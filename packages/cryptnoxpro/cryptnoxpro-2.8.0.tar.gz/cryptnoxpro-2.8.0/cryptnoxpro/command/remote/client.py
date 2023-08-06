import socket
from time import sleep

import cryptnoxpy

from . import communication
from . import config


def _process(client: socket.socket, connection: cryptnoxpy.Connection) -> None:
    try:
        message_length = int(client.recv(config.HEADER).decode(config.FORMAT))
    except ValueError:
        return

    message = client.recv(message_length).decode(config.FORMAT)

    if message != '!Data':
        return

    print(f'Incoming-> {message}')
    communication.receive(client, connection)

def receive(client: socket.socket, connection: cryptnoxpy.Connection) -> bool:
    try:
        _process(client, connection)
    except Exception as error:
        print(f'Error occurred while receiving: {error}')
        return False
    except KeyboardInterrupt:
        return False

    return True


def start(card, server, port):
    print(f'Starting client')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect((server, port))

    while receive(client, card.connection):
        sleep(0.01)

    communication.send(client, '!EndThread')
    client.close()
    print(f'Disconnecting')

    return 0
