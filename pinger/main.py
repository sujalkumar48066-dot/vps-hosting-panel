import os
import sys
import time
import urllib.request

TARGET = os.environ.get("PING_TARGET", "https://vps-hosting-panel.onrender.com/health")
INTERVAL = int(os.environ.get("PING_INTERVAL", "30"))


def ping():
    req = urllib.request.Request(TARGET, method="GET")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read()[:30]
            dt = (time.time() - t0) * 1000
            return f"ok {r.status} {dt:.0f}ms {body}"
    except Exception as e:
        return f"ERR {e}"


def main():
    print(f"pinger: target={TARGET} interval={INTERVAL}s", flush=True)
    while True:
        res = ping()
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {res}", flush=True)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)