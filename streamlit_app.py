from datetime import date
import folium
import requests

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_folium import st_folium

import gspread
import pandas as pd

# --- LOAD SECRETS ---
type = st.secrets.type
project_id=st.secrets.project_id
private_key_id=st.secrets.private_key_id
private_key=st.secrets.private_key
client_email=st.secrets.client_email
client_id=st.secrets.client_id
auth_uri=st.secrets.auth_uri
token_uri=st.secrets.token_uri
auth_provider=st.secrets.auth_provider_x509_cert_url
client=st.secrets.client_x509_cert_url
universe_domain=st.secrets.universe_domain

creds = {
    "type":type,
    "project_id":project_id,
    "private_key_id":private_key_id,
    "private_key":private_key,
    "client_email":client_email,
    "client_id":client_id,
    "auth_uri":auth_uri,
    "token_uri":token_uri,
    "auth_provider_x509_cert_url":auth_provider,
    "client_x509_cert_url":client,
    "universe_domain":universe_domain
}

# ------------ SETTINGS -------------
page_icon = ":spaghetti:"
page_title = "Italian Eats NYC"
layout = "centered"
#------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

@st.cache_resource
def load_sheet(creds):
    gc = gspread.service_account_from_dict(creds)
    ws = gc.open("ItalianEats").worksheet("Sheet1")
    return ws
    

def query_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    parameters = {'q': '{}, New York'.format(address), 'format':'json'}
    response = requests.get(url, params=parameters)
    
    if response.status_code != 200:
        print("Error querying {}".format(address))
        result = {}
    else:
        result = response.json()
    return result

# --- Load Spreadsheet ---
ws = load_sheet(creds)
data = ws.get_all_values()
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers)


completion_date = date.today()

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization", "Data"],
    icons=["pencil-fill", "bar-chart-fill","list-ol"],
    orientation="horizontal",
)

# --- INPUT & SAVE RESTAURANTS
if selected == "Data Entry":
    st.header("Add/Update Restaurant Entry")
    with st.form("entry_form", clear_on_submit=True):
        name=st.text_input("Restaurant Name:")
        address=st.text_input("Address:")
        service=st.slider("Service:",0.0,5.0,2.5,0.1)
        food=st.slider("Food:",0.0,5.0,2.5,0.1)
        ambience=st.slider("Ambience:",0.0,5.0,2.5,0.1)
        travel_time=st.number_input("Travel Time (min):",0,120,0,1)
        comment=st.text_area("Comments:")
        
        # --- Calculate Overall Rating ---
        service_int=float(service)
        food_int=float(food)
        ambience_int=float(ambience)
        overall = (service_int*25 + food_int*50 + ambience_int*25) / 100

        # --- Get Coordinates ---
        json_list = query_address(address)
        json_dict = json_list[0]
        lat = json_dict.get('lat')
        lon = json_dict.get('lon')

    
        submitted = st.form_submit_button("Save Data")
        if submitted:
            data = [name,address,overall,service,food,ambience,travel_time,comment,lat,lon]
            ws.append_row(data)
            st.success("Data saved!")
            st.balloons()
elif selected == "Data Visualization":
    m = folium.Map(location=[40.7826, -73.9656], zoom_start=13)
    for restaurant in range(0,len(df)):
        folium.Marker (
            location=[df.iloc[restaurant]['lat'], df.iloc[restaurant]['lon']],
            popup=df.iloc[restaurant]['Name'],
            icon=folium.Icon(color="red"),
        ).add_to(m)
    folium.TileLayer('stamentoner').add_to(m)
    st_data = st_folium(m, width=725)
elif selected == "Data":
    df1 = df.drop(['lat','lon'], axis=1)
    st.dataframe(df1)
    


