"""Test module for the basic client server response."""


def test_response_ok_from_server():
    """Response from server should be the standard OK response."""
    from client import client
    from server import response_ok
    assert client('message') == response_ok()[:-1].decode('utf8')


def test_response_ok_from_server_has_http():
    """Test that response has HTTP/1.1 protocol."""
    from client import client
    assert 'HTTP/1.1' in client('message')


def test_response_ok_from_server_has_proper_form():
    """Test that response has proper format."""
    from client import client
    response = client('message')
    parsed = response.split()
    assert parsed[0] == 'HTTP/1.1'
    assert parsed[1] == '200'
    assert parsed[2] == 'OK'
