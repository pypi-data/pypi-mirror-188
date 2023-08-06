import threading
import socket

from . import communication


def exit_thread(server):
    exit_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    exit_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    exit_client.connect((server, 5055))
    communication.send(exit_client, '!EndThread')


def handle_client(conn, addr):
    connected_cards = []
    CARD_PORTS = [5055, 5056, 5057, 5058]

    def relay_data(cryptnox, card):
        print(f'Receiving command from cryptnox, relaying it to card client')
        pickled_data = cryptnox.recv(1024)
        send_data(card, pickled_data)
        while True:
            msg_length = card.recv(64).decode('utf-8')
            if msg_length:
                msg_length = int(msg_length)
                msg = card.recv(msg_length).decode('utf-8')
                if msg == "!Data":
                    resp = card.recv(1024)
                    send_data(cryptnox, resp)
                    break
                else:
                    print(f'Else:{msg}')

    print(f'New connection {addr} connected')
    card_server = None
    print(f"Card is now connected.")
    try:
        card_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        card_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        card_server.bind((SERVER, 5055))
        card_server.listen()
        print(f'Card awaiting connection from cryptnox')
        while True:
            connection, address = card_server.accept()
            try:
                while True:
                    msg_length = connection.recv(HEADER).decode(FORMAT)
                    if msg_length:
                        msg_length = int(msg_length)
                        msg = connection.recv(msg_length).decode(FORMAT)
                        print(f'Incoming to relay interface -> {msg}')
                        if msg == "!Data":
                            relay_data(connection, conn)
                        elif msg == "!EndThread":
                            raise KeyboardInterrupt()
                        else:
                            raise
            except KeyboardInterrupt as e:
                print(f'Breaking connection , exiting loop')
                connection.close()
                raise
            except Exception as e:
                print(f'Breaking connection to cryptnoxpro')
                connection.close()
    except (KeyboardInterrupt, Exception) as e:
        print(f'Ending card handler thread {e}')
        if card_server:
            card_server.shutdown(socket.SHUT_RDWR)
            card_server.close()


def start(ip, port):
    print(f'Starting server')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen()
    print(f'[Listening] Server is listening on {server}')
    connections = []
    threads = []
    while True:
        try:
            conn, addr = server.accept()
            connections.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            threads.append(thread)
            print(f'Active connections: {threading.activeCount() - 1}')
        except (KeyboardInterrupt, Exception):
            for each in connections:
                each.close()

            for each in threads:
                try:
                    exit_thread(server)
                except Exception as error:
                    print(f'No card_handle thread connection {error}')
                print('\nJoining sub-thread')
                each.join()

            print('Server is closing')
            server.shutdown(socket.SHUT_RDWR)
            server.close()
            break
