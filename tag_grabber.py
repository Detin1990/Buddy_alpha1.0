from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)
TAGS_FILE = "detected_tags.txt"

@app.route("/submit", methods=["POST"])
def submit_tag():
    data = request.get_json()
    if not data or "tag" not in data or "payload" not in data:
        return jsonify({"error": "Invalid format"}), 400

    tag = data["tag"]
    payload = data["payload"]
    tag_line = f"!{tag}:{payload}!"

    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, "r") as f:
            if tag_line in f.read():
                print(f"[Flask] Duplicate tag skipped: {tag_line}")
                return jsonify({"status": "duplicate skipped"}), 200

    with open(TAGS_FILE, "a") as f:
        f.write(tag_line + "\n")
    print(f"[Flask] Tag written: {tag_line}")

    return jsonify({"status": "tag written"}), 200

@app.route("/submit_tag", methods=["POST"])
def submit_tag_proxy():
    tag = request.form.get("tag", "").strip()
    if not tag.startswith("!exec:"):
        return "Invalid tag format", 400

    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, "r") as f:
            if tag in f.read():
                print(f"[Flask] Duplicate tag skipped: {tag}")
                return "Duplicate tag", 200

    with open(TAGS_FILE, "a") as f:
        f.write(tag + "\n")

    print(f"[Flask] Received tag via proxy: {tag}")
    return "Tag accepted", 200

@app.route("/proxy.html")
def serve_proxy():
    return send_file("proxy.html")

@app.route("/latest_output", methods=["GET", "OPTIONS"])
def get_output():
    output_file = "latest_output.txt"
    if not os.path.exists(output_file):
        return "", 204
    with open(output_file, "r") as f:
        return f.read(), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
