import os
import sys
import time
import json
import signal
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- Configurações de Ambiente ---
PORT = int(os.environ.get("PORT", "8080"))
DEV_NAME = os.environ.get("DEV_NAME", "Platform Engineering Team")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")

START_TIME = time.time()

class EnterpriseAppHandler(BaseHTTPRequestHandler):
    
    def _send_response(self, status_code, content_type, body):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("X-App-Version", APP_VERSION)
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, format, *args):
        # Formatando logs em JSON estruturado para observabilidade
        log_data = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "client_ip": self.client_address[0],
            "method": self.command,
            "path": self.path,
            "status": args[1] if len(args) > 1 else "200"
        }
        print(json.dumps(log_data), flush=True)

    def do_GET(self):
        # Rota de Healthcheck dedicada para Kubernetes / Load Balancer
        if self.path in ["/health", "/healthz"]:
            uptime_seconds = int(time.time() - START_TIME)
            health_payload = json.dumps({
                "status": "UP",
                "environment": ENVIRONMENT,
                "version": APP_VERSION,
                "uptime_seconds": uptime_seconds
            })
            self._send_response(200, "application/json", health_payload)
            return

        # Dashboard Principal (Portal de Serviço)
        if self.path == "/":
            uptime = int(time.time() - START_TIME)
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise Application Gateway</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0b0f19;
            --card-bg: #111827;
            --border: rgba(255, 255, 255, 0.08);
            --text: #f9fafb;
            --muted: #9ca3af;
            --accent: #3b82f6;
            --success: #10b981;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
        }}
        .container {{
            width: 100%;
            max-width: 650px;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 1.25rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: 1.5rem;
        }}
        .title h1 {{ font-size: 1.25rem; font-weight: 700; color: #fff; }}
        .title p {{ font-size: 0.85rem; color: var(--muted); margin-top: 2px; }}
        .status-badge {{
            display: flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: var(--success);
            padding: 4px 10px;
            border-radius: 99px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .pulse {{
            width: 6px; height: 6px; background: var(--success); border-radius: 50%;
            box-shadow: 0 0 8px var(--success);
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        .metric-box {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem;
        }}
        .metric-label {{ font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }}
        .metric-value {{ font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 700; margin-top: 4px; color: #fff; }}
        .footer {{
            font-size: 0.8rem;
            color: var(--muted);
            display: flex;
            justify-content: space-between;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">
                <h1>Service Core Node</h1>
                <p>Enterprise Microservice Gateway</p>
            </div>
            <div class="status-badge">
                <span class="pulse"></span> ONLINE
            </div>
        </div>
        <div class="grid">
            <div class="metric-box">
                <div class="metric-label">Maintainer</div>
                <div class="metric-value">{DEV_NAME}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Environment</div>
                <div class="metric-value">{ENVIRONMENT.upper()}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Port Binding</div>
                <div class="metric-value">:{PORT}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">System Uptime</div>
                <div class="metric-value">{uptime}s</div>
            </div>
        </div>
        <div class="footer">
            <span>Version: {APP_VERSION}</span>
            <span>Health Check: /health</span>
        </div>
    </div>
</body>
</html>"""
            self._send_response(200, "text/html; charset=utf-8", html_content)
            return

        # Rota Não Encontrada
        self._send_response(404, "application/json", json.dumps({"error": "Resource Not Found", "status": 404}))


def graceful_shutdown(signum, frame):
    print(json.dumps({"event": "SHUTDOWN_SIGNAL_RECEIVED", "signal": signum}), flush=True)
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)

    print(json.dumps({
        "event": "SERVER_STARTING",
        "port": PORT,
        "environment": ENVIRONMENT,
        "version": APP_VERSION
    }), flush=True)

    server = HTTPServer(("0.0.0.0", PORT), EnterpriseAppHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
