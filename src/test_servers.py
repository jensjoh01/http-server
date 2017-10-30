"""Module to test if the request sent to the server is good, bad, or host not found."""

import pytest


test_messages = [
    ('../webroot/sample.txt',
     'GET ../webroot/sample.txt HTTP/1.1 Host: www.example.com'),
    ('../webroot/a_web_page.html',
     'GET ../webroot/a_web_page.html HTTP/1.1 Host: www.example.com'),


    # ('PUSH /path/index.html HTTP/1.1 Host: www.example.com', 'HTTP Error 400 - Bad Request'),
    # ('GET /path/index.html HTTP/1.0 Host: www.example.com', 'HTTP Error 400 - Bad Request'),
    # ('GET /path/index.html HTTP/1.1 www.example.com', 'HTTP Error 404 - Not Found'),
    # ('GET /path/index.html HTTP/1.1 Host: www.gobly/gook.com', 'HTTP Error 404 - Not Found'),
    # ('GET /path/index.html HTTP/1.1 Host: www.google.com', 'HTTP/1.1 HTTP 200 OK'),
    # ('hello?...anybody there?', 'HTTP Error 400 - Bad Request')
]

length_messages = [
     (b'testing 123\r\n\r\n1234567890', 10),
     (b'testing 123\r\n\r\nhello world', 11),
     ('testing 123\r\n\r\nhello worldŕ♔䌇'.encode('utf8'), 19)
]


# @pytest.mark.parametrize('file, message', test_messages)
# def test_client(file, message):
#     """Test that the message sent and received is the same as sent."""
#     from client import client
#     from client import get_body
#     with open(file, 'r') as file_handle:
#         file_content = file_handle.read().encode('utf8')
#     client_response = client(message).encode('utf8')
#     print(len(client_response))
#     try:
#         assert get_body(client_response) == file_content
#     except AssertionError:
#         print(b"RESPONSE:\n" + get_body(client_response) + b'\nEXPECTED:\n' +
#               file_content)
#         raise


@pytest.mark.parametrize('message, expected_value', length_messages)
def test_message_length(message, expected_value):
    from client import find_body_len
    length = find_body_len(message)
    try:
        assert length == expected_value
    except AssertionError:
        print(length)
        raise