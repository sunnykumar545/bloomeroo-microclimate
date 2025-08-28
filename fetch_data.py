import requests
import psycopg2
from psycopg2.extras import execute_values
import json
from dotenv import load_dotenv
import os



# Load environment variables from a specific location
load_dotenv()
# Retrieve environment variables
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')


# -------- Step 1: Database connection setup --------

try:
conn = psycopg2.connect(
    dbname="db_name",
    user="db_user",
    password="db_password",
    host="db_host",
    port="db_port"
)
cursor = conn.cursor()
print("Database connection successful.")
except psycopg2.OperationalError as e:
    print(f"Database connection failed: {e}")
    exit()
# -------- Step 2: Create table if not exists --------

create_table_query = """
CREATE TABLE IF NOT EXISTS microclimate_sensors (
    device_id TEXT PRIMARY KEY,
    sensorlocation TEXT,
    received_at TIMESTAMP,
    minimumwinddirection FLOAT,
    averagewinddirection FLOAT,
    maximumwinddirection FLOAT,
    minimumwindspeed FLOAT,
    averagewindspeed FLOAT,
    gustwindspeed FLOAT,
    airtemperature FLOAT,
    relativehumidity FLOAT,
    atmosphericpressure FLOAT
    
);
"""
try:
cursor.execute(create_table_query)
conn.commit()
print("Table 'microclimate_sensors' checked/created.")
except Exception as e:
    print(f"Error creating/checking table: {e}")
    conn.rollback() # Rollback in case of error

# Microclimate sensors data API URL
#Step 3 : Connect to below mentioned API and fetch the data
url = "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/microclimate-sensors-data/records?limit=100"

try:
    # Send GET request
    response = requests.get(url)
    
    # Check if request was successful (HTTP status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        # Print the full JSON data (list of events)
        #print(data)
        records = data.get("results", [])
        #print(records)
    else:
        print(f"Request failed with status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")

    
    # Print each record
    weather_record = []
    for i, record in enumerate(records, start=1):
##    print(f"Record {i}:")
##    print(f"Device ID: {record.get('device_id')}")

    device_id = record.get('device_id')
    sensorlocation = record.get('sensorlocation')
    received_at = record.get('received_at')
    minimumwinddirection = record.get('minimumwinddirection')
    averagewinddirection = record.get('averagewinddirection')
    maximumwinddirection = record.get('maximumwinddirection')
    minimumwindspeed = record.get('minimumwindspeed')
    averagewindspeed = record.get('averagewindspeed')
    gustwindspeed = record.get('gustwindspeed')
    airtemperature = record.get('airtemperature')
    relativehumidity = record.get('relativehumidity')
    atmosphericpressure = record.get('atmosphericpressure')

    weather_record.append((
        device_id,
        sensorlocation,
        received_at,
        minimumwinddirection,
        averagewinddirection,
        maximumwinddirection,
        minimumwindspeed,
        averagewindspeed,
        gustwindspeed,
        airtemperature,
        relativehumidity,
        atmosphericpressure        
    ))

    # Step 5: Insert data into PostgreSQL
    if weather_record:
insert_query = """
INSERT INTO microclimate_sensors (
    device_id,sensorlocation, received_at, minimumwinddirection, averagewinddirection, maximumwinddirection, minimumwindspeed,
    averagewindspeed, gustwindspeed, airtemperature, relativehumidity, atmosphericpressure
) VALUES %s
ON CONFLICT (device_id) DO NOTHING;  -- avoid duplicates if recordid is the same
"""
execute_values(cursor, insert_query, weather_record)
conn.commit()

print(f"Inserted {len(weather_record)} records successfully!")
else:
            print("No data processed to insert.")


# Step 6: Close connection
cursor.close()
conn.close()
