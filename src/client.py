"""Module for client side of http server."""

import sys
import socket


def client(message):
    """Sends a message to the server and receives a response."""

    use_port = 5001

    infos = socket.getaddrinfo('127.0.0.1', use_port)
    if infos[0][1] == 0:
        infos = [(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, '',
                 ('127.0.0.1', use_port))]
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    prepare_message = '{}{}'.format(message, u'\r\n\r\n')
    client.sendall(prepare_message.encode('utf8'))
    buffer_length = 1024
    response_header_dict = {}
    reply = b''
    reply = client.recv(buffer_length)
    print(reply.decode('utf-8'))
    response_split = reply.split(b'\r\n')
    print(response_split)

    # while True:
    #     part = client.recv(buffer_length)
    #     reply += part
    #     if b'\r\n\r\n' in reply:
    #         parsed_reply = reply.split(b'\r\n')
    #         for header_key in parsed_reply:
    #             temp = header_key.split(b':')
    #             print(temp)
    #             try:
    #                 response_header_dict[temp[0]] = temp[1]
    #             except IndexError:
    #                 response_header_dict[temp[0]] = ''
    #         print(response_header_dict.keys())         
    #         # content_length = response_header_dict[b'Content Length']
    #         content_length = 77
    #         response_body = reply.split(b'\r\n\r\n')
    #         import pdb; pdb.set_trace()
    #         print(response_body)
    #         try:
                
    #             if len(response_body[-1].decode('utf-8')) == content_length:
    #                 reply = reply.decode('utf8')
    #                 print(reply)
    #                 break
    #         except:
    #             raise

            
            
    client.close()
    return reply[:-2]


if __name__ == '__main__':
    client(sys.argv[1])
