from flask import Flask, request, jsonify
import geohash2

app = Flask(__name__)

@app.route('/geohash', methods=['GET'])
def get_geohash():
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    precision = request.args.get('precision', type=int)
    round_mode = request.args.get('round_mode', default='down', type=str)

    if round_mode not in ['up', 'down']:
        return jsonify({'error': 'Invalid round_mode, use "up" or "down"'}), 400

    geohash = geohash2.encode(latitude, longitude, precision)

    # TODO: Debug round_mode - expand not working
    #if round_mode == 'up':
    #    geohash = geohash2.expand(geohash)[-1]
    #elif round_mode == 'down':
    #    geohash = geohash2.expand(geohash)[0]

    return jsonify({'geohash': geohash})

@app.route('/ungeohash', methods=['GET'])
def get_ungeohash():
    geohash = request.args.get('geohash', type=str)

    try:
        latitude, longitude, lat_error, lon_error = geohash2.decode_exactly(geohash)
        precision = len(geohash)
    except Exception as e:
        return jsonify({'error': 'Invalid geohash'}), 400

    return jsonify({'latitude': latitude, 'longitude': longitude, 'precision': precision})

if __name__ == '__main__':
    app.run()