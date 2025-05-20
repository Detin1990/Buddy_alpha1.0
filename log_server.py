from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import os

# === CONFIGURATION ===
LOG_PATH = "/home/detin/Buddy4.0/output_log.txt"
BLOCK_SEPARATOR = "\n\n"

# === GLOBAL STATE ===
last_read_position = 0
request_log = []

# === FLASK APP ===
app = Flask(__name__)
CORS(app)

@app.route("/logs", methods=["GET"])
def get_new_logs():
    global last_read_position

    print(f"[INFO] Reading log file: {LOG_PATH}")

    if not os.path.isfile(LOG_PATH):
        print(f"[ERROR] File not found: {LOG_PATH}")
        return jsonify({"error": f"Log file not found at {LOG_PATH}"}), 404

    current_size = os.path.getsize(LOG_PATH)
    print(f"[INFO] Current file size: {current_size} bytes | Read offset: {last_read_position}")

    if last_read_position > current_size:
        print("[WARN] File was truncated. Resetting pointer.")
        last_read_position = 0

    new_blocks = []

    try:
        with open(LOG_PATH, "r") as f:
            f.seek(last_read_position)
            new_data = f.read()
            print(f"[DEBUG] Read {len(new_data)} bytes from file.")
            print(f"[DEBUG] File preview:\n{repr(new_data[:200])}")

            last_read_position = f.tell()

        if new_data.strip():
            new_blocks = new_data.strip().split(BLOCK_SEPARATOR)

    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return jsonify({"error": str(e)}), 500

    return jsonify({"new_blocks": new_blocks})


@app.route("/inject", methods=["POST"])
def inject_log_entry():
    content = request.data.decode("utf-8").strip()
    if not content:
        return jsonify({"error": "Empty body"}), 400

    request_log.append(content)

    try:
        with open(LOG_PATH, "a") as f:
            f.write(content + BLOCK_SEPARATOR)
        print(f"[INFO] Injected new block: {repr(content[:100])}")
        return jsonify({"status": "ok", "written": content})
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/")
def dashboard():
    return render_template_string("""
        <html>
        <head>
            <title>Log Server Monitor</title>
            <meta http-equiv="refresh" content="2">
            <style>
                body { font-family: monospace; background: #111; color: #0f0; padding: 20px; }
                pre { white-space: pre-wrap; word-wrap: break-word; }
            </style>
        </head>
        <body>
            <h2>Recent /inject Commands</h2>
            <ul>
            {% for entry in entries %}
                <li><pre>{{ entry }}</pre></li>
            {% endfor %}
            </ul>
        </body>
        </html>
    """, entries=reversed(request_log[-10:]))


if __name__ == "__main__":
    print(f"[BOOT] Log server starting...")
    print(f"[BOOT] Resolved log path: {LOG_PATH}")
    app.run(host="0.0.0.0", port=8003, debug=False)
