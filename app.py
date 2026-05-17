from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Suspicious phishing keywords
suspicious_keywords = [
    'login',
    'verify',
    'bank',
    'secure',
    'update',
    'free',
    'bonus',
    'gift',
    'win'
]

# Function to check phishing
def is_phishing(url):

    # Detect IP address URLs
    ip_pattern = r'http[s]?://\d+\.\d+\.\d+\.\d+'

    if re.match(ip_pattern, url):
        return True

    # Detect suspicious words
    for word in suspicious_keywords:
        if word in url.lower():
            return True

    # Detect long URLs
    if len(url) > 75:
        return True

    return False


# Home route
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


# API route
@app.route('/check', methods=['POST'])
def check_url():

    data = request.json
    url = data.get('url')

    if is_phishing(url):
        return jsonify({
            'status': 'phishing'
        })

    return jsonify({
        'status': 'safe'
    })


if __name__ == '__main__':
    app.run(debug=True)