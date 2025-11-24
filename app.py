import streamlit as st
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Initialize Nominatim geocoder
geolocator = Nominatim(user_agent="distance_web_app_v1")

def get_location(query):
    try:
        return geolocator.geocode(query, language='ko')
    except Exception as e:
        st.error(f"Error finding location: {e}")
        return None

st.title("Distance Calculator")

col1, col2 = st.columns(2)

with col1:
    start_input = st.text_input("Start Location", "Seoul")

with col2:
    end_input = st.text_input("End Location", "Busan")

if st.button("Calculate Distance"):
    if start_input and end_input:
        with st.spinner("Finding locations..."):
            start_loc = get_location(start_input)
            end_loc = get_location(end_input)

        if start_loc and end_loc:
            st.success("Locations found!")
            
            # Display location details
            st.write(f"**Start:** {start_loc.address}")
            st.write(f"**End:** {end_loc.address}")

            # Calculate distance
            start_coords = (start_loc.latitude, start_loc.longitude)
            end_coords = (end_loc.latitude, end_loc.longitude)
            dist = geodesic(start_coords, end_coords).kilometers

            st.metric(label="Distance", value=f"{dist:.2f} km")
            
            # Map link (optional enhancement)
            st.markdown(f"[View Route on OpenStreetMap](https://www.openstreetmap.org/directions?engine=graphhopper_car&route={start_loc.latitude}%2C{start_loc.longitude}%3B{end_loc.latitude}%2C{end_loc.longitude})")

        else:
            if not start_loc:
                st.error(f"Could not find location: {start_input}")
            if not end_loc:
                st.error(f"Could not find location: {end_input}")
    else:
        st.warning("Please enter both locations.")
