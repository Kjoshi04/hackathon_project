import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from streamlit_folium import st_folium
import folium

from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import streamlit.components.v1 as components

from geopy.geocoders import Nominatim


# favicon
st.set_page_config(
    page_title="ReliefLink",
    page_icon="assets/favicon.png",  # path to your favicon image
    layout="wide"
)


# for location 

def geocode_address(address):
    geolocator = Nominatim(user_agent="relieflink-app")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None


# for mail notification

def send_claim_email(volunteer_name, request_info):
    sender_email = "ADD EMAIL"
    sender_password = "APP PASSWORD"  # Generate an app password from Gmail settings
    receiver_email = sender_email

    subject = f"Relief Request Claimed by {volunteer_name}"
    body = f"""
    The following request has been claimed:

    Name: {request_info['name']}
    Role: {request_info['role']}
    Category: {request_info['category']}
    Location: ({request_info['lat']}, {request_info['lon']})
    
    Claimed by: {volunteer_name}
    """

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print(" Email sent successfully!")
    except Exception as e:
        print(" Failed to send email:", e)


# Simple admin login
st.sidebar.title(" Admin Login")
admin_password = st.sidebar.text_input("Enter admin password", type="password")
is_admin = admin_password == "relieflink123"  # Change this to a secure password


#  Firebase init
if not firebase_admin._apps:
	cred = credentials.Certificate({
    		"type": st.secrets["firebase"]["type"],
    		"project_id": st.secrets["firebase"]["project_id"],
    		"private_key_id": st.secrets["firebase"]["private_key_id"],
    		"private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
    		"client_email": st.secrets["firebase"]["client_email"],
    		"client_id": st.secrets["firebase"]["client_id"],
    		"auth_uri": st.secrets["firebase"]["auth_uri"],
    		"token_uri": st.secrets["firebase"]["token_uri"],
    		"auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
    		"client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
	})
	firebase_admin.initialize_app(cred, {
    		"databaseURL": st.secrets["firebase"]["databaseURL"]
	})


#  Title
st.title(" ReliefLink - Emergency Aid Logistics System")


# Function to load entries from Firebase
def load_entries_from_firebase():
    entries_ref = db.reference("entries")
    return entries_ref.get()  # Get all entries from Firebase

#  Form for submitting new requests
with st.form("entry_form"):
    st.subheader(" Share What You Need or Can Offer")
    name = st.text_input("Your Name")
    role = st.selectbox("You are a...", ["NGO", "Volunteer", "Citizen"])
    need_or_have = st.radio("Do you NEED help or HAVE resources?", ["Need", "Have"])
    category = st.selectbox("Type of Aid", ["Food", "Water", "Medicine", "Shelter", "Other"])

    # 🗺 Optional: Address-based location
    address = st.text_input(" Or enter your location (Address, City, or Landmark)")
    if address:
        lat, lon = geocode_address(address)
        if lat and lon:
            st.session_state["lat"] = lat
            st.session_state["lon"] = lon
            st.success(f" Location set to: ({lat:.6f}, {lon:.6f})")
        else:
            st.warning(" Could not find that location. Please try again.")

    # Manual/Auto Location Entry
    location_col1, location_col2 = st.columns([1, 1])
    with location_col1:
        latitude = st.number_input("Latitude", format="%.6f", key="lat_input", value=st.session_state.get("lat", 0.0))
    with location_col2:
        longitude = st.number_input("Longitude", format="%.6f", key="lon_input", value=st.session_state.get("lon", 0.0))

    submitted = st.form_submit_button(" Submit")

# Submit the form to Firebase and update the map
if submitted:
    data = {
        "name": name,
        "role": role,
        "type": need_or_have,
        "category": category,
        "lat": latitude,
        "lon": longitude,
        "claimed": False,
        "timestamp": datetime.now().isoformat()
    }

    # Save data to Firebase
    db.reference("entries").push(data)
    st.success(" Info submitted successfully!")

    # Trigger a page reload to reflect the newly added marker on the map
    st.cache_data.clear()


#  Sidebar filters for map view
st.sidebar.header(" Filter Map")
selected_type = st.sidebar.radio("Show Entries of Type", ["All", "Need", "Have"])
selected_category = st.sidebar.selectbox("Select Aid Category", ["All", "Food", "Water", "Medicine", "Shelter", "Other"])

# Load the latest entries from Firebase
entries = load_entries_from_firebase()

#  Map
map_center = [20.5937, 78.9629]
map = folium.Map(location=map_center, zoom_start=5)

if entries:
    # 🗺 Add markers with claim button
    for key, val in entries.items():
        if selected_type != "All" and val["type"] != selected_type:
            continue
        if selected_category != "All" and val["category"] != selected_category:
            continue

        if "claimed" not in val:
            val["claimed"] = False

        #  Marker color logic
        if val["type"] == "Need":
            icon_color = "gray" if val["claimed"] else "red"  # Grey for claimed, red for unclaimed
        else:
            icon_color = "green"  # Green for "Have" type

        # Set up the popup message for the marker
        popup_content = f'{val["name"]} ({val["role"]}): {val["type"]} {val["category"]}'

        # Claim section (only for unclaimed NEED requests)
        if val["type"] == "Need" and not val["claimed"]:
            # Unique key for each volunteer name input field
            volunteer_key = f"volunteer_name_{key}"
            
            volunteer_name = st.text_input(f"Enter your name to claim the request from {val['name']}:", key=volunteer_key)
            
            if st.button(f" Claim request from {val['name']}", key=f"claim_button_{key}"):
                if volunteer_name.strip():
                    db.reference(f"entries/{key}").update({
                        "claimed": True,
                        "claimed_by": volunteer_name
                    })
                    send_claim_email(volunteer_name, val)
                    st.success(f"You claimed the request from {val['name']}!")
                    st.cache_data.clear()  # Refresh the cache to load the updated data
                else:
                    st.warning("Please enter your name to confirm the claim.")
        
        # Create the map marker with the claim button inside the popup
        iframe = folium.IFrame(popup_content, width=200, height=150)
        popup = folium.Popup(iframe, max_width=300)

        # Add marker to the map with the claim button inside the popup
        folium.Marker(
            location=[val["lat"], val["lon"]],
            popup=popup,
            icon=folium.Icon(color=icon_color)  # Apply the color based on claimed status
        ).add_to(map)

#  Show map
st_folium(map, width=1200, height=500)

# Claimed Requests Section
st.header(" Claimed Requests")
claimed_entries = [val for val in entries.values() if val.get("claimed")]
if claimed_entries:
    for entry in claimed_entries:
        st.write(f'{entry["name"]} ({entry["role"]}) requested {entry["category"]} — claimed by **{entry.get("claimed_by", "Someone")}**')
else:
    st.write("No requests have been claimed yet.")


# Show admin access confirmation
if is_admin:
    st.success(" Admin mode enabled. You have access to all submitted entries.")

    #  Full Admin Dashboard View (Not hidden in expander)
    st.markdown("##  Admin Dashboard")
    st.markdown("Here you can view, manage, and delete submitted requests:")

    # Sort entries by timestamp descending (newest first)
    sorted_entries = sorted(entries.items(), key=lambda x: x[1].get("timestamp", ""), reverse=True)

    for key, val in sorted_entries:
        with st.container():
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"""
                Name: {val['name']} ({val['role']})  
                Type: {val['type']} — {val['category']}  
                Location:  ({val['lat']}, {val['lon']})  
                Time: {val.get("timestamp", "No timestamp")}  
                Claimed: {" by " + val.get("claimed_by", "N/A") if val.get("claimed") else "Not Claimed"}  
                """)
            with col2:
                if st.button(f"Delete", key=f"del_{key}"):
                    db.reference(f"entries/{key}").delete()
                    st.success(f" Deleted request from {val['name']}")
                    st.rerun()

            st.markdown("---")

