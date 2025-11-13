from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

def _create_handler(opn_handler):
    """
    Dynamically creates a request handler class that uses the provided
    OPN function to handle GET requests.
    """
    class OPNRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            """
            When a GET request comes in, this method calls the user's OPN function,
            passing `self` so the OPN code can access `path`, `send_response`, etc.
            """
            try:
                opn_handler(self)
            except Exception as e:
                print(f"Error in OPN request handler: {e}")
                self.send_error(500, f"Server error in OPN handler: {e}")

        def log_message(self, format, *args):
            """Suppresses the default server logging to keep the console clean."""
            return

    return OPNRequestHandler

def start(port: int, opn_handler):
    """
    Starts the HTTP server on the given port, using the OPN function
    as the request handler.
    """
    handler_class = _create_handler(opn_handler)
    server_address = ('', port)
    
    httpd = HTTPServer(server_address, handler_class)
    httpd.serve_forever()