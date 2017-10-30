from gevent.server import StreamServer
from gevent.monkey import patch_all
from server import server

if __name__ == '__main__':
    patch_all()
    server = StreamServer(('127.0.0.1', 5000), server)
    print('starting gevent server on port 5000')
    server.serve_forever()