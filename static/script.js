function getCurrentLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(pos => {
      fetch('/weather_by_coords', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lat: pos.coords.latitude,
          lon: pos.coords.longitude
        })
      })
      .then(res => res.json())
      .then(data => {
        if (data.error) alert(data.error);
        else location.reload();
      });
    });
  } else {
    alert("Geolocation not supported by your browser.");
  }
}

function toggleDarkMode() {
  document.body.classList.toggle('dark');
}
