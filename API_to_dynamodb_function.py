# Importing necessary libraries
import json
from datetime import datetime
import requests  
import boto3
import os
from decimal import Decimal

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("weather_usa")

# Retrieve API key from environment variable
api_key = os.getenv('WEATHER_API_KEY')

# Defining get_weather_data function
def get_weather_data(city):  
    api_url = "http://api.weatherapi.com/v1/current.json"
    params = {  
        "q": city,    
        "key": api_key
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raises an error for non-200 status codes
        data = response.json()
        
        # Check if 'current' key exists in response
        if 'current' in data:
            return data['current']
        else:
            print(f"No 'current' data found for city: {city}")
            return None
    except requests.RequestException as e:
        print(f"API request failed for city: {city}, error: {e}")
        return None

# Defining Lambda handler
def lambda_handler(event, context):
    # Check if API key is set
    if not api_key:
        print("Error: API key is not set.")
        return {
            'statusCode': 500,
            'body': "API key is missing."
        }

    # List of cities to retrieve weather data for
    cities = ["Fairbanks", "Grand Forks", "Williston", "Fargo", "Aberdeen", "Duluth", "Bismarck", "Marquette", "Rochester", "Anchorage"]

    for city in cities:
        # Get weather data
        data = get_weather_data(city)
        
        # Proceed only if data is valid
        if data:
            try:
                # Extract relevant fields
                temp = data['temp_c']
                wind_speed = data['wind_mph']
                wind_dir = data['wind_dir']
                pressure_mb = data['pressure_mb']
                humidity = data['humidity']
                
                # Timestamp for record
                current_timestamp = datetime.utcnow().isoformat()
                
                # Prepare item for DynamoDB
                item = {
                    'city': city,
                    'time': str(current_timestamp),
                    'temp': Decimal(str(temp)),
                    'wind_speed': Decimal(str(wind_speed)),
                    'wind_dir': wind_dir,
                    'pressure_mb': Decimal(str(pressure_mb)),
                    'humidity': Decimal(str(humidity))
                }
                
                # Insert item into DynamoDB
                table.put_item(Item=item)
                
                print(f"Inserted data for {city}: {item}")
            except KeyError as e:
                print(f"Missing data for city: {city}, error: {e}")
            except Exception as e:
                print(f"Failed to insert data for city: {city}, error: {e}")
        else:
            print(f"No data available for city: {city}")

    return {
        'statusCode': 200,
        'body': "Weather data inserted successfully."
    }
