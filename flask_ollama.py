from flask import Flask, request, jsonify
import requests
import json

app = Flask("OllamaAPI")

@app.route('/api/generate', methods=['POST'])
def generate():
    # Extract model and prompt from the incoming request
    data = request.get_json()
    if not data or 'model' not in data or 'prompt' not in data:
        return jsonify({"error": "Missing 'model' or 'prompt' in request data"}), 400

    model = data['model']
    prompt = data['prompt']

    # Send request to the Ollama API
    ollama_url = "http://127.0.0.1:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {"model": model, "prompt": prompt}

    try:
        response = requests.post(ollama_url, headers=headers, json=payload, stream=True)

        if response.status_code == 200:
            # Collect streamed responses
            full_response = []
            for line in response.iter_lines():
                if line:
                    try:
                        full_response.append(json.loads(line))  # Parse each JSON line
                    except json.JSONDecodeError as e:
                        return jsonify({"error": "Invalid JSON received from Ollama API", "details": str(e)}), 500

            # Combine the streamed responses into a single string or list
            final_response = ''.join([r['response'] for r in full_response if 'response' in r])
            return jsonify({"result": final_response})

        # Handle errors from the Ollama API
        return jsonify({"error": "Failed to communicate with Ollama API", "status_code": response.status_code}), response.status_code

    except requests.RequestException as e:
        return jsonify({"error": "Error connecting to Ollama API", "details": str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """A simple status endpoint to check if the Flask app is running."""
    return jsonify({"status": "Flask app is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
