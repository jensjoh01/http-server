"""Server side of http server."""
import socket
import sys


def server():
    """Server to handle requests from client
    and return either response ok or error."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                               socket.IPPROTO_TCP)
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
            conn.sendall(response_ok())
            conn.close()

    except KeyboardInterrupt:
        conn.close()
        server.close()
        sys.exit()

    except Exception:
        conn.close()
        server.close()
        raise


def response_ok():
    '''return a response code of 200 - OK'''
    response = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n'
    response += b'This is a complete response.\r\n|'
    return response


def response_error():
    '''return a response code of 500 - Internal Server Error'''
    return b'HTTP/1.1 500 Internal Server Error\r\n\r\n|'
