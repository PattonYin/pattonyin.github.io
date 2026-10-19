#!/usr/bin/env python3
"""Local dev server for the site, with caching disabled.

`python -m http.server` sends no cache headers, so Chrome caches index.html,
CSS and JS aggressively — which shows up as "my edits aren't appearing"
long after the files on disk are correct. Note
that http://localhost and http://127.0.0.1 are *separate* cache origins, so a
stale copy on one is invisible from the other.

This sends no-store on every response, so a normal reload always gets fresh
files.

Usage:
    python serve.py           # serves on port 8000
    python serve.py 9000      # custom port

Then open the URL it prints. Ctrl+C to stop.
"""

import http.server
import os
import re
import socketserver
import sys

DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Browsers request byte ranges when loading and seeking through videos.
        byte_range = re.fullmatch(r"bytes=(\d*)-(\d*)", self.headers.get("Range", ""))
        path = self.translate_path(self.path)
        if (not byte_range or not any(byte_range.groups())
                or self.headers.get("If-Range") or not os.path.isfile(path)):
            return super().do_GET()

        try:
            source = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return

        with source:
            stat = os.fstat(source.fileno())
            first, last = byte_range.groups()
            start = int(first) if first else max(0, stat.st_size - int(last))
            end = min(int(last), stat.st_size - 1) if first and last else stat.st_size - 1
            if start > end or start >= stat.st_size:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{stat.st_size}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return

            self.send_response(206)
            self.send_header("Content-Type", self.guess_type(path))
            self.send_header("Content-Length", str(end - start + 1))
            self.send_header("Content-Range", f"bytes {start}-{end}/{stat.st_size}")
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Last-Modified", self.date_time_string(stat.st_mtime))
            self.end_headers()
            source.seek(start)
            remaining = end - start + 1
            while remaining:
                chunk = source.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remaining -= len(chunk)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            sys.exit(f"Not a port number: {sys.argv[1]}")

    if not os.path.exists(os.path.join(DIRECTORY, "index.html")):
        sys.exit(f"No index.html in {DIRECTORY} — run this from the project folder.")

    # Bound to 127.0.0.1 rather than localhost: on Windows "localhost" can
    # resolve to ::1 first, and this keeps the server off the local network.
    try:
        with Server(("127.0.0.1", port), NoCacheHandler) as httpd:
            print(f"Serving {DIRECTORY}")
            print(f"  -> http://127.0.0.1:{port}   (Ctrl+C to stop)")
            print("Caching is disabled; a plain reload always fetches fresh files.")
            httpd.serve_forever()
    except OSError as err:
        sys.exit(f"Could not bind port {port}: {err}\nTry another port: python serve.py 9000")
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
