# -*- coding: utf-8 -*-
"""Simple server module that repeats messages back to the sender."""
import socket


def server():
    """Echo server. Decodes and prints message, then resends the same message
    back through the connection."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                               socket.IPPROTO_TCP)
        address = ('127.0.0.1', 5001)
        server.bind(address)
        while True:
            server.listen(1)
            conn, addr = server.accept()
            buffer_length = 8
            message_complete = False
            message = b""
            while not message_complete:
                part = conn.recv(buffer_length)
                message += part
                if b'|' in message:
                    message = message.decode('utf8')
                    break
            conn.sendall(message.encode('utf8'))
            conn.close()
            print(message[:-1])

    except KeyboardInterrupt:
        server.close()


if __name__ == '__main__':
    server()
