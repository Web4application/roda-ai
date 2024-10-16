from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__roda__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/proxy/<path:path>', methods=['GET', 'POST'])
def proxy(path):
# Here you would add the logic to forward the request to the OpenAI API
return jsonify({"message": f"Proxying to OpenAI API: {path}"})

@app.route('/google-fonts/<path:path>', methods=['GET'])
def google_fonts(path):
# Here you would add the logic to forward the request to Google Fonts
return jsonify({"message": f"Proxying to Google Fonts: {path}"})

@app.route('/sharegpt', methods=['GET'])
def sharegpt():
# Here you would add the logic to forward the request to ShareGPT
return jsonify({"message": "Proxying to ShareGPT"})

if __name__ == '__main__':
app.run(debug=True)
