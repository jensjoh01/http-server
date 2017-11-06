# http-server
This HTTP server accepts a valid GET request and returns an HTTP 200 OK message.  If the request is invalid it returns the appropriate message.

**To Run**

* Set up an virtual environment for python.
* Load dependencies with `pip install -e .[testing]`
* In your terminal, navigate into the `src` folder.
* Open a second terminal window and run `python server.py` from terminal line.
* In the other terminal run `python client.py <message>`.