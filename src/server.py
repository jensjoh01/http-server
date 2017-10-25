"""."""
import socket
import requests


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
            conn.sendall(parse_request(full_message))
            conn.close()

    except KeyboardInterrupt:
        conn.close()
        server.close()
        raise


# def response_ok():
#     '''.'''
#     return b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nThis is a complete response.\r\n|'


# def response_error():
#     '''.'''
#     return b'HTTP/1.1 500 Internal Server Error\r\n\r\n|'


def parse_request(client_message):
    """."""
    parsed_client_message = client_message.split()
    method = parsed_client_message[0]
    URI = parsed_client_message[1]
    protocol = parsed_client_message[2]
    is_valid_host = check_valid_host(parsed_client_message)
    is_valid_message = method == 'GET' and protocol == 'HTTP/1.1'
    if method != 'GET':
        raise Exception  # TODO correct exc.
    if protocol != 'HTTP/1.1':
        raise Exception  # TODO
    if is_valid_message == True and is_valid_host == True:
        print('valid')
        return URI
    else:
        print('invalid')
        raise Exception
        

def check_valid_host(parsed_client_message):
    """."""
    if parsed_client_message[3] != 'Host:':
        return False
    request = requests.get('http://' + parsed_client_message[4])
    try:
        if request.status_code == 200:
            return True
        else:
            return False
    except:
        return False
