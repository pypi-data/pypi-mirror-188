import pickle

import config


def send(connection, message, data: bool = False):
    if data:
        _send(connection, '!Data')

    _send(connection, message)

def _send(connection, message):
    message = message.encode(config.FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(config.FORMAT)
    send_length += b' ' * (config.HEADER - len(send_length))
    connection.send(send_length)
    connection.send(message)


def receive(conn, reader_connection):
    print(f'Receiving command from server')
    pickled_data = conn.recv(1024)
    command = pickle.loads(pickled_data)
    print(f'Transmitting APDU command to card')
    data, s1, s2 = reader_connection.transmit(command)
    response = [data, s1, s2]
    print(f'Responding back to server')
    pickled_response = pickle.dumps(response)
    send(conn, pickled_response, True)
