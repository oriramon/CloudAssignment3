import requests
import json

# Open query.txt file for reading
with open('query.txt', 'r') as query_file:
    # Open response.txt file for writing
    with open('/tmp/response.txt', 'w') as response_file:
        # Iterate over each line in query.txt
        for line in query_file:
            # Remove leading and trailing whitespace from the line
            query = line.strip()
            # Make a POST request to the API
            url = "http://127.0.0.1:8000/dishes"
            headers = {"Content-Type": "application/json"}
            post = requests.post(url, headers=headers, data=json.dumps({'name': query}))
            id = int(post.json())
            response = requests.get(f'{url}/{id}', headers=headers)
            # Extract the data from the response JSON
            data = response.json()
            calories = data.get('cal')
            sodium = data.get('sodium')
            sugar = data.get('sugar')
            # Write the response to response.txt
            response_file.write(f'{query} contains {calories} calories, {sodium} mgs of sodium, and {sugar} grams of sugar\n')
