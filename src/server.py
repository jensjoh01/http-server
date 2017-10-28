"""HTTP Server to handle simple GET requests from client."""
import socket
import urllib.request
import mimetypes
import email.utils



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
            prepare_client_response = '{}{}'.format(response_message, '\r\n\r\n')
            conn.sendall(prepare_client_response.encode('utf8'))
            conn.close()

    except KeyboardInterrupt:
        try:
            conn.close()
            server.close()
        except UnboundLocalError:
            server.close()
        raise


def resolve_uri(URI):
    """Returns an HTTP 200 response with the protocol."""
    get_file = URI
    with open(URI, 'rb') as file_handle:
        file_content = file_handle.read()
    file_type = mimetypes.guess_type(get_file)
    date = email.utils.formatdate(usegmt=True)
    html = """
    <http>
    <body>
    <p>%s</p>
    </body>
    </html>
    """ % file_content
    file_length = len(html)
    response_ok = '{protocol}{httpcode}\r\n\
                    Date:{date}\r\n\
                    Content Length:{length}\r\n\
                    Content Type:{type}; charset=utf-8\r\n\r\n\
                    {html}'\
                    .format(protocol='HTTP/1.1', httpcode='HTTP 200 OK',
                            date=date, length=file_length, type=file_type,
                            html=html)
    return response_ok


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


def parse_request(client_message):
    """Parses the message from the client and handles the response message."""
    parsed_client_message = client_message.split()
    try:
        method = parsed_client_message[0]
        URI = parsed_client_message[1]
        protocol = parsed_client_message[2]
        is_valid_host = check_valid_host(parsed_client_message)
        is_valid_request = method == 'GET' and protocol == 'HTTP/1.1'
        if is_valid_host is False:
            return response_error_404()
        elif is_valid_request is False:
            return response_error_400()
        if is_valid_request and is_valid_host:
            return resolve_uri(URI)
    except IndexError:
        return response_error_400()


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


