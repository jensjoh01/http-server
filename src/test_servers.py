"""Module to test if the request sent to the server is good, bad, or host not found."""

import pytest


test_messages = [
    ('GET /path/index.html HTTP/1.1 Host: www.example.com', 'HTTP/1.1 HTTP 200 OK'),
    ('PUSH /path/index.html HTTP/1.1 Host: www.example.com', 'HTTP Error 400 - Bad Request'),
    ('GET /path/index.html HTTP/1.0 Host: www.example.com', 'HTTP Error 400 - Bad Request'),
    ('GET /path/index.html HTTP/1.1 www.example.com', 'HTTP Error 404 - Not Found'),
    ('GET /path/index.html HTTP/1.1 Host: www.gobly/gook.com', 'HTTP Error 404 - Not Found'),
    ('GET /path/index.html HTTP/1.1 Host: www.google.com', 'HTTP/1.1 HTTP 200 OK'),
    ('hello?...anybody there?', 'HTTP Error 400 - Bad Request'),
    ('', 'HTTP Error 400 - Bad Request'),
    ('Host: www.example.com GET /path/index.html HTTP/1.1', 'HTTP Error 400 - Bad Request')
]


@pytest.mark.parametrize('message, response', test_messages)
def test_client(message, response):
    """Test that the message sent and received is the same as sent."""
    from client import client
    assert client(message) == response

