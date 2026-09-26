import os
import sys
import threading
import time
import urllib.request

TARGET = os.environ.get("PING_TARGET", "https://vps-hosting-panel.onrender.com/health")
INTERVAL = int(os.environ.get("PING_INTERVAL", "30"))
PORT = int(os.environ.get("PORT", "7860"))


def _serve():
    import http.server

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"pinger-ok")

        def do_HEAD(self):
            self.send_response(200)
            self.end_headers()

        def log_message(self, *a):
            pass

    try:
        http.server.ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
    except Exception as e:
        print("http server:", e, flush=True)


def ping():
    t0 = time.time()
    try:
        with urllib.request.urlopen(TARGET, timeout=25) as r:
            dt = (time.time() - t0) * 1000
            return f"ok {r.status} {dt:.0f}ms"
    except Exception as e:
        return f"ERR {type(e).__name__}: {e}"


def main():
    threading.Thread(target=_serve, daemon=True).start()
    print(f"pinger: target={TARGET} interval={INTERVAL}s port={PORT}", flush=True)
    while True:
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {ping()}", flush=True)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)