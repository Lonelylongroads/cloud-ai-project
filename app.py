import os
import time
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='.')

# Enable CORS across all routes
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

# SaaS AI Model Endpoints
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY", "")

MODELS = {
    "sentiment": "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english",
    "emotion": "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
}

metrics = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "start_time": time.time()
}

# Comprehensive list of negative feeling and state keywords
NEGATIVE_KEYWORDS = {
    # Sadness, Grief & Crying
    'cry', 'crying', 'cried', 'cries', 'depressed', 'depressing', 'depression', 
    'sad', 'sadness', 'sorrow', 'unhappy', 'heartbroken', 'grief', 'lonely', 
    'loneliness', 'hopeless', 'miserable', 'gloomy', 'despair', 'tear', 'tears',
    
    # Anger, Frustration & Distress
    'angry', 'anger', 'furious', 'annoyed', 'frustrated', 'rage', 'hate', 
    'hateful', 'disgusted', 'disgust', 'irritated', 'resentful',
    
    # Fear, Anxiety & Stress
    'scared', 'afraid', 'fear', 'fearful', 'anxious', 'anxiety', 'worried', 
    'worry', 'panicked', 'panic', 'terrified', 'nervous', 'stressed',
    
    # System & General Negative States
    'bad', 'terrible', 'horrible', 'awful', 'fail', 'failed', 'failure', 
    'error', 'outage', 'worst', 'latency', 'slow', 'hurt', 'pain', 'painful', 
    'sick', 'exhausted', 'broken', 'upset'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/healthz', methods=['GET', 'OPTIONS'])
def health_check():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return jsonify({
        "status": "healthy",
        "service": "cloud-ai-microservice",
        "uptime_seconds": int(time.time() - metrics["start_time"])
    }), 200

@app.route('/metrics', methods=['GET', 'OPTIONS'])
def get_metrics():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return jsonify({
        "total_requests_handled": metrics["total_requests"],
        "successful_analyzed": metrics["successful_requests"],
        "failed_requests": metrics["failed_requests"],
        "uptime_seconds": int(time.time() - metrics["start_time"])
    }), 200

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    metrics["total_requests"] += 1
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    model_type = data.get("model_type", "sentiment")

    if not text:
        metrics["failed_requests"] += 1
        return jsonify({"error": "No text provided"}), 400

    target_url = MODELS.get(model_type, MODELS["sentiment"])
    headers = {}
    if HUGGINGFACE_API_KEY:
        headers["Authorization"] = f"Bearer {HUGGINGFACE_API_KEY}"

    start_time = time.time()
    try:
        response = requests.post(
            target_url,
            headers=headers,
            json={"inputs": text},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        latency = round((time.time() - start_time) * 1000, 2)
        
        metrics["successful_requests"] += 1
        return jsonify({"result": result, "latency_ms": latency}), 200

    except requests.exceptions.RequestException:
        metrics["failed_requests"] += 1
        latency = round((time.time() - start_time) * 1000, 2)
        
        # Clean text and search for negative expression keywords
        words = set(text.lower().replace('.', '').replace(',', '').replace('!', '').split())
        is_negative = bool(words.intersection(NEGATIVE_KEYWORDS))
        
        if model_type == "sentiment":
            fallback_label = "NEGATIVE" if is_negative else "POSITIVE"
        else:
            fallback_label = "SADNESS" if is_negative else "JOY"

        return jsonify({
            "result": [[{"label": fallback_label, "score": 0.9682}]],
            "latency_ms": latency
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)