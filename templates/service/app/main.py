"""{{ foundry.service_name }} — {{ foundry.description }}

Standard-library HTTP service with the Foundry operational contract:
/healthz, /readyz, /metrics, JSON logs, graceful shutdown.
"""

from __future__ import annotations

import json
import os
import signal
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVICE = "{{ foundry.service_name }}"
PORT = int(os.environ.get("PORT", "{{ foundry.port }}"))
STARTED = time.time()

_requests_total: dict[str, int] = {}
_lock = threading.Lock()
_ready = threading.Event()


def log(level: str, message: str, **fields: object) -> None:
    record = {"ts": round(time.time(), 3), "level": level, "service": SERVICE,
              "msg": message, **fields}
    print(json.dumps(record), flush=True)


class Handler(BaseHTTPRequestHandler):
    server_version = SERVICE

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, payload: dict) -> None:
        self._send(status, json.dumps(payload).encode(), "application/json")

    def do_GET(self) -> None:  # noqa: N802 - http.server API
        path = self.path.split("?", 1)[0]
        with _lock:
            _requests_total[path] = _requests_total.get(path, 0) + 1

        if path == "/healthz":
            self._send_json(200, {"status": "ok"})
        elif path == "/readyz":
            if _ready.is_set():
                self._send_json(200, {"status": "ready"})
            else:
                self._send_json(503, {"status": "draining"})
        elif path == "/metrics":
            with _lock:
                lines = ["# TYPE http_requests_total counter"]
                lines += [
                    f'http_requests_total{{path="{p}"}} {n}'
                    for p, n in sorted(_requests_total.items())
                ]
            lines.append("# TYPE process_uptime_seconds gauge")
            lines.append(f"process_uptime_seconds {time.time() - STARTED:.1f}")
            self._send(200, ("\n".join(lines) + "\n").encode(),
                       "text/plain; version=0.0.4")
        elif path == "/":
            self._send_json(200, {"service": SERVICE, "status": "ok",
                                  "uptime_s": round(time.time() - STARTED, 1)})
        else:
            self._send_json(404, {"error": "not found", "path": path})

    def log_message(self, fmt: str, *args: object) -> None:
        log("info", "request", method=self.command, path=self.path,
            client=self.client_address[0])


def main() -> int:
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)

    def shutdown(signum: int, _frame: object) -> None:
        log("info", "shutdown requested", signal=signal.Signals(signum).name)
        _ready.clear()          # fail /readyz so load balancers drain first
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    _ready.set()
    log("info", "listening", port=PORT)
    server.serve_forever()
    server.server_close()
    log("info", "stopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
