from datetime import date

import streamlit as st
from streamlit_option_menu import option_menu

import gspread
import pandas as pd

# --- LOAD SHEET ---
SHEET_ID = st.secrets.sheet_id
SHEET_NAME = "Sheet1"
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
df = pd.read_csv(url)
print(df.head())

# ------------ SETTINGS -------------
page_icon = ":spaghetti:"
page_title = "Italian Eats NYC"
layout = "centered"
trains = ['1','2','3','4','5','6','7','A','B','C','D','E','F','G','J','L',
          'M','N','Q','R','W','Z']
#------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

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
    options=["Data Entry", "Data Visualization"],
    icons=["pencil-fill", "bar-chart-fill"],
    orientation="horizontal",
)

# --- INPUT & SAVE RESTAURANTS
if selected == "Data Entry":
    st.header("Add/Update Restaurant Entry")
    with st.form("entry_form", clear_on_submit=True):
        name=st.text_input("Restaurant Name:")
        address=st.text_input("Address:")
        st.date_input("Date Visited:")
        st.slider("Overall:",0.0,5.0,2.5,0.1)
        st.slider("Service:",0.0,5.0,2.5,0.1)
        st.slider("Food:",0.0,5.0,2.5,0.1)
        st.slider("Ambience:",0.0,5.0,2.5,0.1)
        st.multiselect("Trains:",options=trains)
        st.number_input("Travel Time (min):",0,120,0,1)
        st.text_area("Comments:")
    
        submitted = st.form_submit_button("Save Data")
        if submitted:
            st.success("Data saved!")
            st.balloons()

