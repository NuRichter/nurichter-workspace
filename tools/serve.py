#!/usr/bin/env python3
"""Server lokal yang meniru Vercel: cleanUrls, 404.html, dan header dari vercel.json.

    python3 tools/serve.py [port]      # default 8000
"""
import http.server
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF = json.load(open(os.path.join(ROOT, "vercel.json")))
RULES = [(re.compile("^" + r["source"].replace("(.*)", "(.*)") + "$"), r["headers"]) for r in CONF.get("headers", [])]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        path = self.path.split("?")[0]
        for rx, hs in RULES:
            if rx.match(path):
                for h in hs:
                    self.send_header(h["key"], h["value"])
        super().end_headers()

    def send_head(self):
        path = self.path.split("?")[0]
        local = os.path.join(ROOT, path.lstrip("/"))
        if path != "/" and not os.path.exists(local) and os.path.exists(local + ".html"):
            self.path = path + ".html" + (("?" + self.path.split("?", 1)[1]) if "?" in self.path else "")
        elif path != "/" and not os.path.exists(local):
            self.send_response(404)
            body = open(os.path.join(ROOT, "404.html"), "rb").read()
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return None
        return super().send_head()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"http://localhost:{port}")
    http.server.ThreadingHTTPServer(("", port), Handler).serve_forever()
