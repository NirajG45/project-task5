from flask import Flask, render_template, request, session, jsonify
import requests, datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'
API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'

def get_weather_data(city=None, lat=None, lon=None):
    if city:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    else:
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    if response.status_code != 200:
        return None, None

    data = response.json()
    first = data['list'][0]
    weather = {
        'city': data['city']['name'],
        'country': data['city']['country'],
        'flag': f"https://flagsapi.com/{data['city']['country']}/flat/32.png",
        'description': first['weather'][0]['description'].title(),
        'temperature': first['main']['temp'],
        'feels_like': first['main']['feels_like'],
        'humidity': first['main']['humidity'],
        'wind': first['wind']['speed'],
        'pressure': first['main']['pressure'],
        'updated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    chart_data = [{'time': item['dt_txt'], 'temp': item['main']['temp']} for item in data['list'][:8]]
    return weather, chart_data

@app.route('/', methods=['GET', 'POST'])
def index():
    weather, chart_data, error = None, None, None

    if request.method == 'POST':
        city = request.form.get('city')
        weather, chart_data = get_weather_data(city=city)
        if weather:
            session.setdefault('history', []).append(city)
        else:
            error = "City not found."

    history = session.get('history', [])
    return render_template("index.html", weather=weather, chart_data=chart_data, history=history[-5:], error=error)

@app.route('/weather_by_coords', methods=['POST'])
def weather_by_coords():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    weather, chart_data = get_weather_data(lat=lat, lon=lon)
    if not weather:
        return jsonify({'error': 'Weather data not available'}), 400
    return jsonify({'weather': weather, 'chart_data': chart_data})

if __name__ == '__main__':
    app.run(debug=True)
