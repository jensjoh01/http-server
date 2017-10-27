"""test for the client"""
import pytest
# test that the message sent to the server
# is the same as the message received

# test_messages = ['hello', 'This is my test message', 'abcdefgh',
#                  'abcdefghabcdefgh', '!@#!^#%^ASDF;_', 'with__7',
#                  'tishasfourteen', 'specialchars∂ßå´´∂']


# @pytest.mark.parametrize('message', test_messages)
# def test_client(message):
#     """Test that the message sent and received is the same as sent."""
#     from client import client
#     assert message == client(message)

def test_response_ok_from_server():
    '''response from server should be the standard OK response'''
    from client import client
    from server import response_ok
    assert client('message') == response_ok()[:-1].decode('utf8')
