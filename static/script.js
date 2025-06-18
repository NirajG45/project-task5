
function getWeather() {
  const city = document.getElementById('cityInput').value;
  fetch('/weather', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ city })
  })
  .then(res => res.json())
  .then(data => displayWeather(data))
  .catch(err => console.error(err));
}

function getLocationWeather() {
  navigator.geolocation.getCurrentPosition((pos) => {
    fetch('/weather', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ lat: pos.coords.latitude, lon: pos.coords.longitude })
    })
    .then(res => res.json())
    .then(data => displayWeather(data))
    .catch(err => console.error(err));
  });
}

function displayWeather(data) {
  if (data.error) {
    document.getElementById('weatherResult').innerText = data.error;
    return;
  }

  const icons = {
    Clear: "fas fa-sun",
    Clouds: "fas fa-cloud",
    Rain: "fas fa-cloud-showers-heavy",
    Drizzle: "fas fa-cloud-rain",
    Thunderstorm: "fas fa-bolt",
    Snow: "fas fa-snowflake",
    Mist: "fas fa-smog"
  };

  const iconClass = icons[data.condition] || "fas fa-sun";

  document.getElementById('weatherResult').innerHTML = `
    <h2>${data.city}, ${data.country}</h2>
    <i class="${iconClass}" style="font-size: 50px;"></i>
    <p><strong>Condition:</strong> ${data.condition}</p>
    <p><i class="fas fa-thermometer-half"></i> Temperature: ${data.temp}°C</p>
    <p><i class="fas fa-tint"></i> Humidity: ${data.humidity}%</p>
    <p><i class="fas fa-wind"></i> Wind Speed: ${data.wind} m/s</p>
    <p><i class="fas fa-clock"></i> Time: ${data.time}</p>
  `;
}
