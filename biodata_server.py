import json
import os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
HTML_DIR = BASE_DIR.parent / 'HTML'

app = Flask(__name__, static_folder=None)


@app.route('/')
def home():
    return send_from_directory(HTML_DIR, 'biodata.html')


@app.route('/submit', methods=['POST'])
def submit_biodata():
    if not request.is_json:
        return jsonify(error='Expected JSON payload.'), 400

    data = request.get_json()
    required_fields = ['user_id', 'password', 'address', 'gender', 'hobbies']

    missing = [field for field in required_fields if field not in data or not data[field]]
    if missing:
        return jsonify(error=f'Missing fields: {", '.join(missing)}'), 400

    user_id = str(data['user_id']).strip()
    address = str(data['address']).strip()
    gender = str(data['gender']).strip()
    hobbies = data['hobbies'] if isinstance(data['hobbies'], list) else [str(data['hobbies'])]

    if not user_id or not address or not gender:
        return jsonify(error='User ID, address, and gender are required.'), 400

    hobbies_text = ', '.join(hobby for hobby in hobbies if hobby)
    summary = (
        f'User {user_id} submitted biodata with gender {gender} and hobbies: '
        f'{hobbies_text or "None"}. Address length: {len(address)} chars.'
    )

    response = {
        'message': 'Biodata received successfully.',
        'summary': summary,
        'stored': {
            'user_id': user_id,
            'gender': gender,
            'hobbies': hobbies,
            'address': address,
        },
    }

    return jsonify(response)


@app.route('/<path:filename>')
def serve_static(filename):
    requested = BASE_DIR.parent / 'HTML' / filename
    if requested.exists() and requested.is_file():
        return send_from_directory(HTML_DIR, filename)
    return jsonify(error='File not found.'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
