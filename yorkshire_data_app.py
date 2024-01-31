import streamlit as st
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from textwrap import wrap
from sklearn.linear_model import LinearRegression
import numpy as np

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

    select_cols = st.columns((1,1))

    with select_cols[0]:
        selected_main_category = st.selectbox("Main category", main_category_names)
    main_category_metadata = metadata[metadata["Main group"] == selected_main_category]
    sub_category_names = main_category_metadata["Sub group"].unique()
    
    with select_cols[1]:
        selected_sub_category = st.selectbox("Sub category", sub_category_names)

    indicator_names = main_category_metadata[main_category_metadata["Sub group"] == selected_sub_category]["column"]
    selected_indicator = st.selectbox("Indicator", indicator_names, label_visibility="collapsed")
    
    # Fetch information from metadata
    info_row = metadata[metadata["column"] == selected_indicator]
    units_selected = info_row["units"].values[0]
    scale_type = info_row["scale_type"].values[0]

    st.markdown("### " + selected_indicator)

    if isinstance(info_row["notes"].values[0], str):
        # st.markdown('### Description')
        st.markdown(info_row["notes"].values[0])
    st.markdown('### Sources')
    st.markdown(info_row["source_name"].values[0])
    st.markdown(info_row["url"].values[0])     
    
# Center panel: Data view selector and view
with main_cols[1]:
    option = st.selectbox("Data view", ("Map view", "Table view", "Comparison", "Bar graph"))

    if option == "Map view":

        invert_scale = scale_type == "inverted"
        map = choropleth_folium_yorkshire(maps_yorkshire,
                                          data,
                                          selected_indicator,
                                          units_selected,
                                          scale_type=scale_type)
        st_data = st_folium(map, use_container_width = True)

    elif option == "Table view":
        st.dataframe(data[["LAD21NM", selected_indicator]],
                     use_container_width=True,
                     hide_index=True,
                     height=710)
        
    elif option == "Comparison":

        view_cols = st.columns((2,2,6))

        with view_cols[0]:
            compare_main_category = st.selectbox("Compare against",
                                            main_category_names, label_visibility="collapsed")
            
            compare_indicator_metadata = metadata[metadata["Main group"] == compare_main_category]
            compare_sub_group_names = compare_indicator_metadata["Sub group"].unique()

        with view_cols[1]:
            compare_sub_group = st.selectbox("Compare sub group",
                                            compare_sub_group_names, label_visibility="collapsed")
            compare_indicator_names = compare_indicator_metadata[compare_indicator_metadata["Sub group"] == compare_sub_group]["column"]

        with view_cols[2]:
            compare_indicator = st.selectbox("Compare indicator", compare_indicator_names, label_visibility="collapsed")
        
        compare_info_row = metadata[metadata["column"] == compare_indicator]
        compare_units_selected = compare_info_row["units"].values[0]

        X = data[selected_indicator].to_numpy()
        Y = data[compare_indicator].to_numpy()
        mask = ~np.isnan(X) & ~np.isnan(Y)

        X = X[mask].reshape(-1, 1)
        Y = Y[mask].reshape(-1, 1)   

        reg = LinearRegression().fit(X, Y)
        Y_exp = reg.predict(X)
        R = reg.score(X, Y)

        f, ax = plt.subplots()
        ax.plot(data[selected_indicator], data[compare_indicator], 'o')
        ax.plot(X, Y_exp, color='k', alpha=0.5, label = f"R = {R:.3f}")
        ax.set_xlabel("\n".join(wrap(selected_indicator + " [" + units_selected + "]", 50)), size=8)
        ax.set_ylabel("\n".join(wrap(compare_indicator + " [" + compare_units_selected + "]", 50)), size=8)
        ax.legend()

        st.pyplot(f)
    
    elif option == "Bar graph":

        view_cols = st.columns((1.5, 1.5, 6, 1, 1))

        with view_cols[0]:
            compare_main_category = st.selectbox("Compare against",
                                            main_category_names, label_visibility="collapsed")
            
            compare_indicator_metadata = metadata[metadata["Main group"] == compare_main_category]
            compare_sub_group_names = compare_indicator_metadata["Sub group"].unique()

        with view_cols[1]:
            compare_sub_group = st.selectbox("Compare sub group",
                                            compare_sub_group_names, label_visibility="collapsed")
            compare_indicator_names = compare_indicator_metadata[compare_indicator_metadata["Sub group"] == compare_sub_group]["column"]

        with view_cols[2]:
            compare_indicator = st.selectbox("Compare indicator", compare_indicator_names, label_visibility="collapsed")

        with view_cols[3]:
            if st.button("Add"):
                if "bar_graph_cols" not in st.session_state:
                    st.session_state.bar_graph_cols = list()
                st.session_state.bar_graph_cols.append(compare_indicator)
        with view_cols[4]:
            if st.button("Clear", type="primary"):
                st.session_state.bar_graph_cols = list()

        data_sel = data[np.concatenate((["LAD21NM"] ,st.session_state.bar_graph_cols))]

        try:
            f, ax = plt.subplots(figsize=(12, 6))
            ax = data_sel.plot.bar(x="LAD21NM", ax=ax)
            plt.xticks(rotation=45, ha="right")
            st.pyplot(f)

        except TypeError:
            st.write("Choose columns from the selector to start generating a bar graph.")
with main_cols[2]:
    pass
