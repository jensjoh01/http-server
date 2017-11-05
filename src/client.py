# -*- coding: utf-8 -*-
"""Module for sending messages to a simple server application."""
import sys
import socket


def client(message):
    """Sends a message to the server and receives a response."""
    use_port = 5001
    infos = socket.getaddrinfo('127.0.0.1', use_port)
    if infos[0][1] == 0:
        infos = [(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, '',
                  ('127.0.0.1', use_port))]
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    prepare_message = '{}{}'.format(message, '|')
    if hasattr('', 'encode'):
        client.sendall(prepare_message.encode('utf8'))
    else:
        client.sendall(prepare_message)  # TODO get tests to pass in TOX
    buffer_length = 8
    reply = b''
    while True:
        part = client.recv(buffer_length)
        reply += part
        if b'|' in reply:
            reply = reply.decode('utf8')
            break
    client.close()
    return reply[:-1]


if __name__ == '__main__':
    print(client(sys.argv[1]))
