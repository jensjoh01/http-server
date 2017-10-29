# http-server

This HTTP server accepts a valid GET request and returns an HTTP 200 OK message and the file/directory include in the URI of the get request.  If there is an error the server returns an appropriate response. 
This was built using gevent to handle concurrency.  Run gevent_server from the command line first and then run the client with your requests.

