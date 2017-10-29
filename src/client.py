"""Module for client side of http server."""

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
    prepare_message = '{}{}'.format(message, u'\r\n\r\n')
    client.sendall(prepare_message.encode('utf8'))
    buffer_length = 8
    reply = b''
    body_len = 0

    while True:
        part = client.recv(buffer_length)
        reply += part
        if body_len == 0 and parse_body_len(reply) > 0:
            body_len = parse_body_len(reply)
        if body_len > 0 and find_body_len(reply) >= body_len:
            reply = reply.decode('utf8')
            break

    client.close()
    print(reply)
    return(reply)


if __name__ == '__main__':
    client(sys.argv[1])


def find_body_len(message):
    body = get_body(message)
    if body is None:
        return -1
    return len(body)


def get_body(message):
    divider_index = message.find(b'\r\n\r\n')
    if divider_index < 0:
        return None
    divider_index += 4
    print(message[divider_index:])
    return message[divider_index:]


def parse_body_len(message):
    length_start = message.find(b'Content Length:')
    if length_start < 0:
        return -1
    length_start += len(b'Content Length:')
    lengh_end = message[length_start:].find(b'\r')
    if lengh_end < 0:
        return -1
    number = int(message[length_start: length_start + lengh_end])
    return number
