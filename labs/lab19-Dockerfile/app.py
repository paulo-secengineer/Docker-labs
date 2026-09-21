from flask import Flask, jsonify
import psutil
import os

app = Flask(__name__)

PORT = int(os.getenv("PORT", 8080))
ENVIRONMENT = os.getenv("ENVIRONMENT", "Production")

@app.route("/")
def health_check():
    return jsonify({
        "status": "UP",
        "service": "infra-monitor-api",
        "environment": ENVIRONMENT,
        "metrics": {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_usage_percent": psutil.virtual_memory().percent,
            "total_memory_mb": round(psutil.virtual_memory().total / (1024 * 1024), 2)
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
