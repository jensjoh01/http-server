"""."""
import socket
import urllib.request


def server():
    """."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        address = ('127.0.0.1', 5002)
        server.bind(address)
        response_message = u''
        while True:
            server.listen(1)
            conn, addr = server.accept()
            buffer_length = 8
            message_complete = False
            message = b""
            while not message_complete:
                part = conn.recv(buffer_length)
                message += part
                if b'\r\n' in message:
                    message = message.decode('utf8')
                    response_message = parse_request(message)
                    message = b""
                    break        
            prepare_client_response = '{}{}'.format(response_message, '\r\n')
            conn.sendall(prepare_client_response.encode('utf8'))
            conn.close()

    except KeyboardInterrupt:
        try:
            conn.close()
            server.close()
        except UnboundLocalError:
            server.close()
        raise
      

def response_ok(URI):
    '''.'''
    request_200 = 'HTTP 200 OK'
    request_ok = '{} {}'.format(URI, request_200)
    return request_ok


def response_error(protocol):
    '''.'''
    error_400 = 'HTTP Error 400 - Bad Request'
    error_message = '{} {}'.format(protocol, error_400)
    return error_message


def parse_request(client_message):
    """."""
    parsed_client_message = client_message.split()
    try:
        method = parsed_client_message[0]
        URI = parsed_client_message[1]
        protocol = parsed_client_message[2]
        is_valid_host = check_valid_host(parsed_client_message)
        is_valid_request = method == 'GET' and protocol == 'HTTP/1.1'
        if is_valid_request is True and is_valid_host is True:
            #  is valid request and URL
            return response_ok(URI)
        else:
            #  is not valid
            return response_error(protocol)
    except IndexError:
        return response_error(protocol)


def check_valid_host(parsed_client_message):
    """."""
    if parsed_client_message[3] != 'Host:':
        return False
    req = urllib.request.Request('http://' + parsed_client_message[4])
    try:
        res = urllib.request.urlopen(req).getcode()
        if res == 200:
            return True
        else:
            return False
    except urllib.error.URLError:
        return False

