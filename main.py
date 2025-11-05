from flask import Flask, render_template, jsonify, send_from_directory, request
import os
import json
import requests
from urllib.parse import urlencode
import openai

app = Flask(__name__, static_folder='static', template_folder='templates')

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'parks.json')


def load_parks():
	with open(DATA_PATH, 'r', encoding='utf-8') as f:
		return json.load(f)


@app.route('/')
def index():
	parks = load_parks()
	return render_template('index.html', parks=parks)


@app.route('/api/parks')
def api_parks():
	return jsonify(load_parks())


@app.route('/api/park/<park_id>')
def api_park_detail(park_id):
	"""Return richer details for a park. If NPS_API_KEY is set in environment, try to fetch NPS data and images.

	The server will not store your API key; set it in your environment as NPS_API_KEY.
	"""
	parks = load_parks()
	park = next((p for p in parks if p.get('id') == park_id), None)
	if not park:
		return jsonify({'error': 'park not found'}), 404

	nps_key = os.environ.get('NPS_API_KEY')
	if not nps_key:
		# Return basic info and a helpful message
		return jsonify({
			'park': park,
			'note': 'No NPS API key configured. Set NPS_API_KEY environment variable to get photos and extended info.'
		})

	try:
		# Query the NPS parks endpoint by park name. Note: park JSON ids here may not be NPS park codes,
		# so we search by name and pick the best match.
		params = {'q': park.get('name', ''), 'limit': 50, 'api_key': nps_key}
		resp = requests.get('https://developer.nps.gov/api/v1/parks', params=params, timeout=8)
		resp.raise_for_status()
		data = resp.json().get('data', [])

		# Try to find a close match by fullName or name containing the park name
		match = None
		name_lower = park.get('name', '').lower()
		for item in data:
			if name_lower in (item.get('fullName','') or '').lower() or name_lower in (item.get('name','') or '').lower():
				match = item
				break
		if not match and data:
			match = data[0]

		result = {'park': park}
		if match:
			# pick only useful fields to return
			result['nps'] = {
				'fullName': match.get('fullName'),
				'description': match.get('description'),
				'directionsInfo': match.get('directionsInfo'),
				'url': match.get('url'),
				'images': match.get('images', [])
			}
		else:
			result['note'] = 'No matching NPS entry found for this park.'

		# Compute a simple heuristic for "best time to go" based on latitude
		lat = park.get('lat')
		best = 'Spring or Fall'
		try:
			if lat is not None:
				lat = float(lat)
				if lat >= 55:
					best = 'Summer (short season)'
				elif lat <= 32:
					best = 'Fall or Winter (milder)'
				else:
					best = 'Spring or Fall'
		except Exception:
			pass
		result['bestTimeToGo'] = best

		return jsonify(result)
	except requests.RequestException as e:
		return jsonify({'error': 'failed to fetch NPS data', 'detail': str(e)}), 502


@app.route('/api/chat', methods=['POST'])
def api_chat():
	"""Handle chat messages with AI assistant for park questions."""
	openai_key = os.environ.get('OPENAI_API_KEY')
	if not openai_key:
		return jsonify({'error': 'AI not configured. Set OPENAI_API_KEY environment variable.'}), 500

	data = request.get_json()
	user_message = data.get('message', '')
	if not user_message:
		return jsonify({'response': 'Please ask a question about national parks!'})

	try:
		openai.api_key = openai_key
		response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=[
				{"role": "system", "content": "You are a helpful AI assistant for a US National Parks tracker website. Answer questions about national parks, provide facts, and help users plan visits. Keep responses concise and friendly."},
				{"role": "user", "content": user_message}
			],
			max_tokens=200
		)
		ai_response = response.choices[0].message['content'].strip()
		return jsonify({'response': ai_response})
	except Exception as e:
		return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
	# For local quick dev. In production use a WSGI server.
	app.run(host='0.0.0.0', port=5000, debug=True)
