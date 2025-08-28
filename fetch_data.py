import requests
# Public API endpoint - GitHub public events
url = "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/microclimate-sensors-data/records?limit=100"

try:
    # Send GET request
    response = requests.get(url)
    
    # Check if request was successful (HTTP status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        # Print the full JSON data (list of events)
        print(data)
        records = data.get("results", {})
        print(records)
    else:
        print(f"Request failed with status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")

    
    # Print each record
for i, record in enumerate(records, start=1):
    print(f"Record {i}: {record}")
