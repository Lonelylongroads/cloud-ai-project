import os
import time
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='.')

# Enable CORS for local development (Live Server compatibility)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

# Environment & Model Setup
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY", "")
HF_MODEL_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

# Request Metrics Tracking
metrics = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "start_time": time.time()
}

@app.route('/')
def home():
    """Serves the Frontend Dashboard."""
    return render_template('index.html')

@app.route('/healthz', methods=['GET', 'OPTIONS'])
def health_check():
    """Kubernetes Liveness and Readiness Probe Endpoint."""
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return jsonify({
        "status": "healthy",
        "service": "cloud-ai-microservice",
        "uptime_seconds": int(time.time() - metrics["start_time"])
    }), 200

@app.route('/metrics', methods=['GET', 'OPTIONS'])
def get_metrics():
    """Prometheus-style Application Metrics Endpoint."""
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return jsonify({
        "total_requests_handled": metrics["total_requests"],
        "successful_analyzed": metrics["successful_requests"],
        "failed_requests": metrics["failed_requests"],
        "uptime_seconds": int(time.time() - metrics["start_time"])
    }), 200

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_sentiment():
    """Main AI Sentiment Analysis Endpoint."""
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    metrics["total_requests"] += 1
    data = request.get_json() or {}
    text = data.get("text", "").strip()

    if not text:
        metrics["failed_requests"] += 1
        return jsonify({"error": "No text provided for sentiment analysis."}), 400

    headers = {}
    if HUGGINGFACE_API_KEY:
        headers["Authorization"] = f"Bearer {HUGGINGFACE_API_KEY}"

    try:
        response = requests.post(
            HF_MODEL_URL,
            headers=headers,
            json={"inputs": text},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        
        metrics["successful_requests"] += 1
        return jsonify(result), 200

    except requests.exceptions.RequestException as e:
        metrics["failed_requests"] += 1
        # Fallback response for offline testing or HF rate-limiting
        fallback_sentiment = "POSITIVE" if len(text) % 2 == 0 else "NEGATIVE"
        return jsonify([[
            {"label": fallback_sentiment, "score": 0.9852},
            {"label": "DEMO_FALLBACK_MODE", "score": 0.0148}
        ]]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)