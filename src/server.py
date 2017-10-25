"""."""
import socket


def server():
    """."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        address = ('127.0.0.1', 5001)
        server.bind(address)
        full_message = u''
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
                    message = message.decode('utf8')[:-1]
                    print(message)
                    full_message += message
                    break
            # import pdb; pdb.set_trace()
            conn.sendall(response_ok())
            conn.close()

    except KeyboardInterrupt:

        # import pdb; pdb.set_trace()
        conn.close()
        server.close()
        raise

def response_ok():
    '''.'''
    return b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nThis is a complete response.\r\n|'

def response_error():
    '''.'''
    return b'HTTP/1.1 500 Internal Server Error\r\n\r\n|'
