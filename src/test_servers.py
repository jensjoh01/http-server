"""Module to test if the request sent to the server is good, bad, or host not found."""

import pytest


test_messages = [
    ('GET ../webroot/sample.txt HTTP/1.1 Host: www.example.com', 
    'HTTP/1.1HTTP 200 OK\r\nDate:Sat, 28 Oct 2017 22:42:23 GMT\r\n\
    Content Length:158\r\nContent Type:(\'text/plain\', None); charset=utf-8\
    \r\n\r\n\
    <http>\r\n<body>\r\n<p>This is a very simple text file.\r\n\
    Just to show that we can serve it up.\r\nIt is three lines long.\r\n</p>\
    </body>\r\n</html>'),
    # ('PUSH /path/index.html HTTP/1.1 Host: www.example.com', 'HTTP Error 400 - Bad Request'),
    # ('GET /path/index.html HTTP/1.0 Host: www.example.com', 'HTTP Error 400 - Bad Request'),
    # ('GET /path/index.html HTTP/1.1 www.example.com', 'HTTP Error 404 - Not Found'),
    # ('GET /path/index.html HTTP/1.1 Host: www.gobly/gook.com', 'HTTP Error 404 - Not Found'),
    # ('GET /path/index.html HTTP/1.1 Host: www.google.com', 'HTTP/1.1 HTTP 200 OK'),
    # ('hello?...anybody there?', 'HTTP Error 400 - Bad Request')
]


@pytest.mark.parametrize('message, expected_response', test_messages)
def test_client(message, expected_response):
    """Test that the message sent and received is the same as sent."""
    from client import client
    client_response = client(message)
    assert len(client_response) == 158

