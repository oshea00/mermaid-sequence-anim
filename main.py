"""Serve mcp-flow.html on localhost."""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 8000))


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/mcp-flow.html"
        return super().do_GET()


if __name__ == "__main__":
    server = HTTPServer(("", PORT), Handler)
    print(f"Serving mcp-flow.html at http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
