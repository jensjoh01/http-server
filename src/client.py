"""."""
import socket


def client(message):
    """."""
    infos = socket.getaddrinfo('127.0.0.1', 5001)
    if infos[0][1] == 0:
        infos = [(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, '', ('127.0.0.1', 5001))]
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(message.encode('utf8'))

    buffer_length = 8
    reply = ''
    while True:
        part = client.recv(buffer_length)
        reply += part.decode('utf8')
        if len(part) < buffer_length:
            print(reply)
            break

def lookat(sock = 5001):
    infos = socket.getaddrinfo('127.0.0.1', sock)
    print(infos)
