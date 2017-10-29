"""HTTP Server to handle simple GET requests from client."""
import socket
import urllib.request
import mimetypes
import email.utils
import os


def server():
    """HTTP Server receives simple GET requests from client, parses them,
    and returns an HTTP response message."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                               socket.IPPROTO_TCP)
        address = ('127.0.0.1', 5001)
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
                if b'\r\n\r\n' in message:
                    message = message.decode('utf8')
                    response_message = parse_request(message)
                    message = b""
                    break
            print(response_message.encode('utf8'))
            conn.sendall(response_message.encode('utf8'))
            conn.close()
    except KeyboardInterrupt:
        try:
            conn.close()
            server.close()
        except UnboundLocalError:
            server.close()
        raise


def parse_request(client_message):
    """Parses the message from the client and handles the response message."""
    parsed_client_message = client_message.split()
    try:
        method = parsed_client_message[0]
        URI = parsed_client_message[1]
        protocol = parsed_client_message[2]
        is_valid_host = check_valid_host(parsed_client_message)
        is_uri_secure = secure_uri(URI)
        if method != 'GET':
            response_error_405()
        elif protocol != 'HTTP/1.1':
            response_error_505()
        elif not is_valid_host:
            return response_error_404()
        elif not is_uri_secure:
            return response_error_400()
        else:
            return resolve_uri(URI)
    except IndexError:
        return response_error_400()


def resolve_uri(URI):
    """Returns an HTTP 200 response with the protocol."""
    body_content = ''
    try:
        if os.path.isdir(URI):
            body_content = handle_dir(URI)
        else:
            body_content = handle_file(URI)
        file_type = mimetypes.guess_type(URI)
        date = email.utils.formatdate(usegmt=True)
        file_length = len(body_content)
        # this string isn't indented for testing purposes
        response_ok = '{protocol}{httpcode}\r\n\
Date:{date}\r\n\
Content Length:{length}\r\n\
Content Type:{type}; charset=utf-8\r\n\r\n\
{html}'\
                        .format(protocol='HTTP/1.1', httpcode='HTTP 200 OK',
                                date=date, length=file_length, type=file_type,
                                html=body_content)
    except OSError:
        return response_error_404()
    return response_ok


def check_valid_host(parsed_client_message):
    """Checks if the Host address is valid or not."""
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


def secure_uri(URI):
    """."""
    if URI.split('/')[1] == 'webroot':
        return True
    else:
        return False


def handle_dir(URI):
    """Function that takes in a URI and determines if path leads to a directory
    if it does, then it returns the contents."""
    dir_content = '\n'.join(os.listdir(URI))
    return dir_content.encode('utf8')


def handle_file(URI):
    """."""
    with open(URI, 'r') as file_handle:
        file_content = file_handle.read()
    return file_content.encode('utf8')
    # return compile_html(file_content)


# def compile_html(data):
#     """."""
#     html = """
#     <http>
#     <body>
#     <p>%s</p>
#     </body>
#     </html>
#     """ % data
#     return html


def response_error_400():
    """Returns an HTTP Error 400 Bad Request."""
    error_400 = 'HTTP Error 400 - Bad Request'
    error_message = '{}'.format(error_400)
    return error_message


def response_error_404():
    """Returns an HTTP Error 404 Not Found."""
    error_404 = 'HTTP Error 404 - Not Found'
    error_message = '{}'.format(error_404)
    return error_message


def response_error_405():
    """Returns an HTTP Error 405 - Method Not Allowed."""
    error_405 = 'HTTP Error 405 - Method Not Allowed'
    error_message = '{}'.format(error_405)
    return error_message


def response_error_505():
    """Returns an HTTP Error 505 - HTTP Version Not Supported."""
    error_505 = 'HTTP Error 505 - HTTP Version Not Supported'
    error_message = '{}'.format(error_505)
    return error_message
