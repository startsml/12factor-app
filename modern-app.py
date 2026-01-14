import os
import sys
import signal
import logging
from flask import Flask, jsonify
from redis import Redis, RedisError

# FACTOR 11: Logs
# We configure logs to stream to Standard Output (stdout), not a file.
# The container engine (Docker) will capture these streams.
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# FACTOR 3: Config
# We read ALL config from Environment Variables.
# Defaults are provided for Dev, but overridden in Prod.
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
APP_COLOR = os.environ.get('APP_COLOR', 'white')

# FACTOR 4: Backing Services
# We connect to Redis via a URL/Host provided by the environment.
# The app doesn't care if Redis is a local container or a cloud cluster.
redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, socket_connect_timeout=2, socket_timeout=2)

@app.route('/')
def index():
    # FACTOR 6: Stateless Processes
    # We do NOT store state in a local variable or local text file.
    # We store it in the Backing Service (Redis).
    try:
        hits = redis.incr('hits')
    except RedisError:
        hits = "Cannot connect to Redis"
        logger.error("Failed to connect to Redis backing service")

    # Log the event (Streamed to stdout)
    logger.info(f"Request served. Current Hit Count: {hits}")

    html = f"""
    <body style="background-color: {APP_COLOR}; font-family: sans-serif; padding: 2rem;">
        <h1>12-Factor Modern App</h1>
        <div style="border: 2px solid green; padding: 20px; background: white;">
            <h2>Global Visitor Count: {hits}</h2>
            <p><em>(Served by Hostname: {os.uname()[1]})</em></p>
        </div>
    </body>
    """
    return html

@app.route('/health')
def health():
    # Used for orchestration health checks
    return jsonify(status="healthy")

# FACTOR 9: Disposability
# Handle SIGTERM signals to shut down gracefully.
def signal_handler(sig, frame):
    logger.info('Received SIGTERM. Shutting down gracefully...')
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    # FACTOR 7: Port Binding
    # We listen on the port defined by the environment (default 5000).
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Modern App on port {port}...")
    app.run(host="0.0.0.0", port=port)