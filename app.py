
from flask import Flask, render_template, request, jsonify
import requests
import datetime

app = Flask(__name__)
API_KEY = 'f82d429e6a4cb8fecadd760ca2c4a2ed'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    city = data.get('city')
    lat = data.get('lat')
    lon = data.get('lon')

    if city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    elif lat and lon:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    else:
        return jsonify({'error': 'No location provided'}), 400

    response = requests.get(url)
    weather_data = response.json()

    if weather_data.get('cod') != 200:
        return jsonify({'error': 'City not found'}), 404

    result = {
        'city': weather_data['name'],
        'country': weather_data['sys']['country'],
        'temp': weather_data['main']['temp'],
        'condition': weather_data['weather'][0]['main'],
        'icon': weather_data['weather'][0]['icon'],
        'humidity': weather_data['main']['humidity'],
        'wind': weather_data['wind']['speed'],
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
