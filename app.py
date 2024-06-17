from functions import get_correctionAltitude,get_airport_temp, get_airport_alt
from flask import Flask,request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/adjust_altitudes', methods=['POST'])
def calculate_sum():

    data = request.json

    if 'icao' in data and isinstance(data['icao'],str):
        icao = data['icao']

        temp = get_airport_temp(icao) # Error proof this
        airportAltitude = get_airport_alt(icao)

    else:
        return jsonify({'error': 'No ICAO provided'})
        
    if 'altitudes' in data and isinstance(data['altitudes'], list):
        altitudes = data['altitudes']
    else:
        return jsonify({'error': 'Invalid JSON. Expected format: {"altitudes": [1, 2, 3]}'})
    
    correctedAlts = []
    for i in altitudes:
        correctedAlts.append(get_correctionAltitude(i,airportAltitude,temp))
    data = {"altitudes":correctedAlts}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
