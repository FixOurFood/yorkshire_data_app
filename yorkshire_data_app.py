import streamlit as st
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

from map_config import maps_yorkshire, cloropleth_folium_yorkshire
from gui_config import *
from data_config import data, metadata

def long_str_trunc(label, leng=45):
    ''' Shortens a long string to 45 characters or less.
    If longer than 45 characters, it adds an elipsis at the end.

    Parameters
    ----------
    label : str
        String to shorten
    leng : int
        Maximum number of characters before shortening and appending an elipsis.

    Returns
    -------
    str
        Shortened label.
    '''

    if len(label) > leng:
        return label[:leng] + "..."
    else:
        return label 

# Reduce the padding at the top of the page. 1rem results in some clipping
st.set_page_config(layout="wide")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1.5rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

# Define main columns
main_cols = st.columns((2,4,2))

# Left side panel: Data selector and notes
with main_cols[0]:

    option_main_category = st.selectbox("Main category",
                                        list(data.keys())[2:],
                                        format_func=long_str_trunc)
    
    # Fetch information from metadata
    info_row = metadata[metadata["column"] == option_main_category]

    st.markdown("## " + option_main_category)

    if isinstance(info_row["notes"].values[0], str):
        st.markdown('### Description')
        st.markdown(info_row["notes"].values[0])
    st.markdown('### Sources')
    st.markdown(info_row["source_name"].values[0])
    st.markdown(info_row["url"].values[0])     
    
    # option_sub_category = st.selectbox(option_main_category,
    #                                    main_categories[option_main_category])

# Center panel: Data view selector and view
with main_cols[1]:
    option = st.selectbox("Data view", ("Map view", "Table view", "Comparison"))

    if option == "Map view":
        map = cloropleth_folium_yorkshire(maps_yorkshire,
                                          data,
                                          option_main_category,
                                          info_row["units"].values[0])
        st_data = st_folium(map, use_container_width = True)

    elif option == "Table view":
        st.dataframe(data[["LAD21NM", option_main_category]],
                     use_container_width=True,
                     hide_index=True,
                     height=710)
        
    elif option == "Comparison":
        compare_main_category = st.selectbox("Compare against",
                                        list(data.keys())[2:],
                                        format_func=long_str_trunc)
        
        f, ax = plt.subplots()
        ax.plot(data[option_main_category], data[compare_main_category], 'o')
        ax.set_xlabel(option_main_category)
        ax.set_ylabel(compare_main_category)

        st.pyplot(f)
               
with main_cols[2]:
    pass
