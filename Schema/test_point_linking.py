# Ensure flask app is running!
# From cw2
# python ..\Schema\test_point_linking.py

import requests

# First, insert Points using the /api/points endpoint

# Define the URL for the Points API endpoint
points_url = "http://127.0.0.1:8000/api/point"

# Data for each point
points_data = [
    {"latitude": 50.423698, "longitude": -4.110593, "description": "Point 1"},
    {"latitude": 50.424958, "longitude": -4.108179, "description": "Point 2"},
    {"latitude": 50.420222, "longitude": -4.099503, "description": "Point 3"},
    {"latitude": 50.422134, "longitude": -4.113191, "description": "Point 4"},
    {"latitude": 50.424262, "longitude": -4.109453, "description": "Point 5"}
]

# Create Points
for point_data in points_data:
    response = requests.post(points_url, json = point_data)
    if response.status_code == 201:
        print(f"Point created: {response.json()}")
    else:
        print(f"Error creating point: {response.text}")

# Next, update Points with Doubly Linked List References

# Define the URL for updating a Point's next/previous relationship
update_point_url = "http://127.0.0.1:8000/api/point/"

# Function to update the links between points
def update_point_link(point_id, next_point_id, previous_point_id):
    update_data = {
        "next_point_id": next_point_id,
        "previous_point_id": previous_point_id
    }
    response = requests.put(f"{update_point_url}/{point_id}", json=update_data)
    
    if response.status_code == 200:
        print(f"Point {point_id} updated successfully.")
    else:
        print(f"Error updating point {point_id}: {response.text}")

# Set the relationships between the points (doubly linked list)
update_point_link(1, 2, 5)  # Point 1
update_point_link(2, 3, 1)  # Point 2
update_point_link(3, 4, 2)  # Point 3
update_point_link(4, 5, 3)  # Point 4
update_point_link(5, 1, 4)  # Point 5

# Finally, create the Trail using the /api/trails endpoint

# Define the URL for the Trails API endpoint
trails_url = "http://127.0.0.1:8000/api/trail"

# Data for the trail
trail_data = {
    "author_id": None,
    "starting_point_id": 1,
    "name": "Plymouth Airport Runway",
    "summary": "A walk that follows Plymouth Airports runway",
    "description": "This trail follows the Plymouth airport runway. Not technically legal to walk this one.",
    "difficulty": "Easy",
    "location": "Plymouth, UK",
    "length": 5.0,
    "elevation_gain": 1,
    "route_type": "Loop"
}

# Create the trail
response = requests.post(trails_url, json=trail_data)
if response.status_code == 201:
    print(f"Trail created: {response.json()}")
    print(f"Trail assigned ID: {response.json().get("id")}")
else:
    print(f"Error creating trail: {response.text}")

# Navigate trail doubly-linked list!

created_trail_id = response.json().get("id")
response = requests.get(f"{trails_url}/{created_trail_id}")

input()

starting_point = response.json().get("starting_point_id")
point_id = starting_point
while True: # eek
    print(point_id)
    response = requests.get(f"{points_url}/{point_id}")
    point_id = response.json().get("next_point_id")
    if point_id == starting_point:
        print(point_id, "end!")
        break
    