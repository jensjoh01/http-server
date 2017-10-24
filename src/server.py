"""."""
import socket


def server():
    """."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        address = ('127.0.0.1', 5001)
        server.bind(address)
        while True:
            server.listen(1)
            conn, addr = server.accept()
            buffer_length = 8
            message_complete = False
            message = ""
            while not message_complete:
                part = conn.recv(buffer_length)
                message += part.decode('utf8')
                if len(part) < buffer_length:
                    print(message)
                    break
            conn.close()
    except:
        conn.close()
        server.close()
