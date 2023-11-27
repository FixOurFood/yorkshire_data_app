import streamlit as st
import geopandas as gpd

from streamlit_folium import st_folium

from map_config import maps_yorkshire, cloropleth_folium_yorkshire
from gui_config import *
from data_config import data

st.set_page_config(layout="wide")
main_cols = st.columns((2,4,2))

with main_cols[0]:

    option_main_category = st.selectbox("Main category",
                                        list(main_categories.keys()))
    
    option_sub_category = st.selectbox(option_main_category,
                                       main_categories[option_main_category])

with main_cols[1]:
    option = st.selectbox("Data display", ("Map view", "Table view", "Comparison"))

    if option == "Map view":
        map = cloropleth_folium_yorkshire(maps_yorkshire)
        st_data = st_folium(map, use_container_width = True)

