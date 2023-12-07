import geopandas as gpd
import folium
from branca.colormap import linear, LinearColormap
import numpy as np

# Read map data and create geodataframe
maps = gpd.read_file("data/Local_Authority_Districts_December_2021_UK_BUC_2022_8985961432220200008.gpkg")

yorkshire_council_names = [
    "York",
    "Craven",
    "Hambleton",
    "Harrogate",
    "Richmondshire",
    "Ryedale",
    "Scarborough",
    "Selby",
    "Bradford",
    "Calderdale",
    "Kirklees",
    "Leeds",
    "Wakefield",
    "East Riding of Yorkshire",
    "Kingston upon Hull, City of",
    "Barnsley",
    "Doncaster",
    "Rotherham",
    "Sheffield",
]

maps_yorkshire = maps[maps["LAD21NM"].isin(yorkshire_council_names)]

def choropleth_folium_yorkshire(geoframe, data, key, legend_label):
    """Returns a folium cloropleth map from a geopandas boundary dataframe and
    data for each boundary

    Parameters
    ----------
    gpd : geopandas dataframe
        Geopandas dataframe with geometry for each row and an "LAD21NM" identifier
    data : str or arraylike
        Pandas dataframe with data to match to the geopandas frame used for plotting.
        Must contain "LAD21NM" column to match data to its geometry
    key : string
        Data column name from `data` to assign values in the map
    legend_label : string
        String used for the legend label on top of the plot 

    Returns
    -------
    map : folium map
        cloropleth map with different colors associated to each geometry in the
        geopandas dataframe, depending on the values.
    """

    data_plot = geoframe.merge(data[["LAD21NM", key]], on="LAD21NM")

    map = folium.Map([54, -1.3],
                 zoom_start=8,
                 tiles="Cartodb Positron",
                 min_zoom=7,
                 max_zoom=10)
    
    data_dict = data_plot.set_index("LAD21NM")[key]


    # colormap = linear.YlGn_09.scale(data_plot[key].min(), data_plot[key].max())
    colormap = LinearColormap(["#ea4862", "#f5c22a", "#5b7c62"], vmin=data_plot[key].min(), vmax=data_plot[key].max())
    colormap.caption = legend_label

    def cmap_nan(val):
        if np.isnan(val):
            return "#000000"
        else:
            return colormap(val)

    tooltip = folium.GeoJsonTooltip(
        fields=["LAD21NM", key],
        aliases=["Local Autority:", legend_label],
        localize=True,
        sticky=True,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )

    folium.GeoJson(data_plot,
                   name=key,
                   style_function=lambda feature:{
                       "fillColor": cmap_nan(data_dict[feature["properties"]["LAD21NM"]]),
                       "color": "black",
                       "weight": 1,
                       "fillOpacity": 0.7},
                   highlight_function=lambda feature:{
                       "weight": 2},
                   tooltip=tooltip
                   ).add_to(map)
        
    colormap.add_to(map)

    return map