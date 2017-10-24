"""."""
import socket


def client(message):
    """."""
    infos = socket.getaddrinfo('127.0.0.1', 5001)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(message.encode('utf8'))


