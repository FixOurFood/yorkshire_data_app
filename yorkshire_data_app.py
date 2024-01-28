import streamlit as st
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

from map_config import maps_yorkshire, choropleth_folium_yorkshire
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

main_category_names = metadata["Main group"].unique()

# Define main columns
main_cols = st.columns((2,4,2))

# Left side panel: Data selector and notes
with main_cols[0]:

    st.image("images/fof_logo.png")

    selected_main_category = st.selectbox("Main category", main_category_names)

    indicator_names = metadata[metadata["Main group"] == selected_main_category]["column"]
    selected_indicator = st.selectbox("Indicator", indicator_names, label_visibility="collapsed")
    
    # Fetch information from metadata
    info_row = metadata[metadata["column"] == selected_indicator]

    st.markdown("## " + selected_indicator)

    if isinstance(info_row["notes"].values[0], str):
        st.markdown('### Description')
        st.markdown(info_row["notes"].values[0])
    st.markdown('### Sources')
    st.markdown(info_row["source_name"].values[0])
    st.markdown(info_row["url"].values[0])     
    
# Center panel: Data view selector and view
with main_cols[1]:
    option = st.selectbox("Data view", ("Map view", "Table view", "Comparison"))

    if option == "Map view":
        map = choropleth_folium_yorkshire(maps_yorkshire,
                                          data,
                                          selected_indicator,
                                          info_row["units"].values[0])
        st_data = st_folium(map, use_container_width = True)

    elif option == "Table view":
        st.dataframe(data[["LAD21NM", selected_indicator]],
                     use_container_width=True,
                     hide_index=True,
                     height=710)
        
    elif option == "Comparison":

        view_cols = st.columns((3,7))

        with view_cols[0]:
            compare_main_category = st.selectbox("Compare against",
                                            main_category_names, label_visibility="collapsed")
            compare_indicator_names = metadata[metadata["Main group"] == compare_main_category]["column"]
        with view_cols[1]:
            compare_indicator = st.selectbox("Compare indicator", compare_indicator_names, label_visibility="collapsed")
        
        f, ax = plt.subplots()
        ax.plot(data[selected_indicator], data[compare_indicator], 'o')
        ax.set_xlabel(selected_indicator)
        ax.set_ylabel(compare_indicator)

        st.pyplot(f)
               
with main_cols[2]:
    pass
