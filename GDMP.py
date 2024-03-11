import csv
import requests

def get_distance(origin, destination, api_key):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={origin}&destinations={destination}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    print("API Response:", data)  # Add this line to print the response data

    if data['status'] == 'OK':
        if 'distance' in data['rows'][0]['elements'][0]:
            distance_in_meters = data['rows'][0]['elements'][0]['distance']['value']
            distance_in_miles = distance_in_meters / 1609.34  # Convert meters to miles
            return distance_in_miles
        else:
            print("No distance information found in the response")
            return None
    else:
        print("Error:", data['status'])
        return None

def main():
    api_key = '<INSERT_API_HERE>'  # Replace with your own API key
    with open('postcodes.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    for row in rows:
        origin, destination = row[:2]  # Extract first two values (origin and destination) from each row
        if origin and destination:  # Check if both origin and destination are not empty
            distance = get_distance(origin, destination, api_key)
            if distance is not None:
                row.append(f"{distance:.2f} miles")  # Append distance in miles to the row
                print(f"Distance from {origin} to {destination}: {distance:.2f} miles")
            else:
                print(f"Failed to retrieve distance for {origin} to {destination}")

    with open('postcodes_with_distances.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

if __name__ == "__main__":
    main()
