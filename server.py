from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import sqlite3

DB_NAME = "url.db"


class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        short_code = parsed.path.lstrip("/")

        if not short_code:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"URL shortener server is running")
            return

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute("SELECT original FROM pair WHERE shorted = ?", (short_code,))
        row = cur.fetchone()
        con.close()

        if row:
            original_url = row[0]
            self.send_response(302)
            self.send_header("Location", original_url)
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Short URL not found")


def run(server_class=HTTPServer, handler_class=RedirectHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on http://localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()