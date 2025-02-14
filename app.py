import streamlit as st
import folium
from streamlit_folium import folium_static
import requests

# Your Delhi government bus API URL (Replace this with the correct URL from the API documentation)
API_URL = "https://api.delhi.gov.in/bus-location"  # Replace this URL with the correct API endpoint

# Your API key for authentication
API_KEY = "7bantvvp83QkbzXxyC2DBRAD5USt76sE"  # Your API key

def fetch_all_bus_locations():
    """
    Fetches the live locations of all buses from the API.
    """
    try:
        # Include the API key in the request headers or parameters
        headers = {
            "Authorization": f"Bearer {API_KEY}"  # Adjust based on API requirements
        }
        params = {
            "api_key": API_KEY  # Include the API key in the request
        }

        # Send a GET request to the API
        response = requests.get(API_URL, headers=headers, params=params)

        # Print the response for debugging
        st.write("API Response:", response.json())  # Display the raw response in Streamlit

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()  # Assuming the API returns JSON with a list of buses
            bus_locations = []
            for bus in data:
                bus_id = bus.get("bus_id")  # Adjust if the API returns different keys
                latitude = bus.get("latitude")  # Adjust if the API returns different keys
                longitude = bus.get("longitude")  # Adjust if the API returns different keys
                if latitude and longitude:  # Ensure valid coordinates
                    bus_locations.append({"bus_id": bus_id, "lat": latitude, "lon": longitude})
            return bus_locations
        else:
            st.error(f"Error: Unable to fetch data. Status code: {response.status_code}")
            st.error(f"Response: {response.text}")  # Display the error response
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

def show_bus_map(bus_locations):
    """
    Show the live locations of all buses on a map.
    """
    # Create a Folium map centered around the first bus's location (or a default location)
    if bus_locations:
        default_lat = bus_locations[0]["lat"]
        default_lon = bus_locations[0]["lon"]
    else:
        default_lat, default_lon = 28.7041, 77.1025  # Default to Delhi coordinates

    bus_map = folium.Map(location=[default_lat, default_lon], zoom_start=12)

    # Add markers for all bus locations
    for bus in bus_locations:
        folium.Marker(
            location=[bus["lat"], bus["lon"]],
            popup=f"Bus {bus['bus_id']}",
            icon=folium.Icon(color='blue', icon='bus')
        ).add_to(bus_map)

    # Display the map in Streamlit
    folium_static(bus_map)

def main():
    st.title("Delhi Real-Time Bus Tracker 🚌")
    st.write("Track the live locations of all buses on the map.")

    # Fetch all bus locations
    bus_locations = fetch_all_bus_locations()

    if bus_locations:
        st.write(f"Found {len(bus_locations)} buses.")
        # Display the bus locations on the map
        show_bus_map(bus_locations)
    else:
        st.write("Could not retrieve bus locations. Please check the API or try again later.")

if __name__ == "__main__":
    main()