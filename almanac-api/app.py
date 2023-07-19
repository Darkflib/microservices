from flask import Flask, request, jsonify
import geoip2.database
import redis

app = Flask(__name__)
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

# Connect to your Redis instance.
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def home():
    ip = request.remote_addr  # Get the client's IP address
    response = reader.city(ip)  # Lookup the IP in the GeoIP database

    # Access specific data from the response
    city = response.city.name
    country = response.country.iso_code
    latitude = response.location.latitude
    longitude = response.location.longitude

    # Now, to find the nearest location to a specific point, use GEORADIUS.
    # We'll use the user's approximate location and find the nearest 5 cities.
    nearby_locations = r.georadius('Locations', longitude, latitude, 500, 'km', sort='ASC', count=5)

    # Print the location
    print(f'Your approximated location is {city}, {country}')

    # Return as JSON
    return jsonify({
        'your_location': {
            'city': city,
            'country': country,
            'latitude': latitude,
            'longitude': longitude,
        },
        'nearby_locations': nearby_locations.decode('utf-8') if nearby_locations else []
    })

if __name__ == '__main__':
    app.run()
