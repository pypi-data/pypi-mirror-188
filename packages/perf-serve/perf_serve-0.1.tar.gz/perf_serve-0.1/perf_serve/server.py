from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

import threading

class _RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, served_file: Path, *args, **kwargs) -> None:
        self.served_file = served_file
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        with self.served_file.open() as f:
            self.wfile.write(bytes(f.read(), "utf8"))

    def log_request(self, code='-', size='-'):
        return


def start_server(path: Path, address: str, port: int) -> HTTPServer:
    server_address = (address, port)
    http_server = HTTPServer(server_address, lambda *args, **kwargs: _RequestHandler(path, *args, **kwargs))
    print(f"Serving {path} at {http_server.server_address[0]}:{http_server.server_address[1]}")
    threading.Thread(target=lambda: http_server.serve_forever(), daemon=True).start()
    return http_server
