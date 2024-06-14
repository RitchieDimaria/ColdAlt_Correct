from functions import get_correctionAltitude,get_airport_temp
from flask import Flask,request,jsonify


app = Flask(__name__)

@app.route('/adjust_altitudes', methods=['POST'])
def calculate_sum():

    data = request.json

    if 'icao' in data and isinstance(data['icao'],str):
        icao = data['icao']

        temp = get_airport_temp(icao) # Error proof this

    else:
        return jsonify({'error': 'No ICAO provided'})
        
    if 'alt' in data and isinstance(data['alt'], list):
        altitudes = data['alt']
    else:
        return jsonify({'error': 'Invalid JSON. Expected format: {"alt": [1, 2, 3]}'})
    
    # Soon this will be replaced to fetch the airport altitude from some database
    if 'airportAlt' in data and isinstance(data['airportAlt'], int):
        airportAltitude = data['airportAlt']

    else:
        return jsonify({'error': 'Expecting airportAlt'})
    
    correctedAlts = []
    for i in altitudes:
        correctedAlts.append(get_correctionAltitude(i,airportAltitude,temp))
    
    return jsonify({"data":correctedAlts})


if __name__ == '__main__':
    app.run(debug=True)