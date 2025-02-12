# webhook_listener.py
from flask import Flask, request, jsonify
from main import start_bug_fix

app = Flask(__name__)

@app.route("/sentry-webhook", methods=["POST"])
def sentry_webhook():
    payload = request.json  # Receive Sentry error details
    print(f"Received Error: {payload}")

    start_bug_fix(payload)  # Start AI bug-fixing process

    return jsonify({"message": "Bug Fixing Process Started"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
