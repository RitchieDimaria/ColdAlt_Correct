import pandas as pd
import numpy as np
import os
from scipy.interpolate import interp2d
from dotenv import load_dotenv
import requests
from json import load as load_json

correction_data = pd.read_csv('correction.csv')
load_dotenv()
f = open("elevations.json")
elevations = load_json(f)
f.close()
weather_key = os.environ.get('WEATHER_KEY')
temperatures = correction_data['temperature_C'].values
altitudes = correction_data.columns[1:].astype(float)
corrections = correction_data.iloc[:, 1:].values
interp_function = interp2d(altitudes, temperatures, corrections, kind='linear')

def get_airport_alt(airport_code):
    return(elevations[airport_code])
def temp_parser(data):
    return (data["data"][0]["temperature"]["celsius"])

def get_airport_temp(airport_code):
    api_key = weather_key
    api_endpoint = f"https://api.checkwx.com/metar/{airport_code}/decoded"
    headers = {
        'X-API-Key': api_key
    }
    
    try:
        # Send GET request to the API
        response = requests.get(api_endpoint,headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            temp_C = temp_parser(data)
            print(temp_C)
            return(temp_C)
            
        else:
            print(f"Error: Request failed with status code {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def interpolate_correction(altitude_ft, temperature_C):
    """Interpolate the correction value for given altitude and temperature."""
    correction = interp_function(altitude_ft, temperature_C)[0]
    return correction

def true_altitude(indicated_altitude_ft, airport_elevation_ft, ground_temp):
    """Calculate the true altitude after applying the cold weather correction."""
    altitude_ft = indicated_altitude_ft - airport_elevation_ft
    correction = interpolate_correction(altitude_ft, ground_temp)
    true_alt = indicated_altitude_ft + correction
    return true_alt


def get_correctionAltitude(indicated_altitude_ft,airport_elevation_ft,ground_temp):
    correction = interpolate_correction(indicated_altitude_ft - airport_elevation_ft, ground_temp)
    true_alt = true_altitude(indicated_altitude_ft, airport_elevation_ft, ground_temp)

    print(f"Cold weather correction: {correction:.2f} feet")
    print(f"True altitude: {true_alt:.2f} feet")
    return(correction,true_alt)
