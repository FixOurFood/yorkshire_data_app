import geopandas as gpd
import folium

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

def cloropleth_folium_yorkshire(gpd, data, key, legend_name):
    """Returns a folium cloropleth map from a geopandas boundary dataframe and
    data for each boundary

    Parameters
    ----------

    gpd : geopandas dataframe
        each row defined by a geometry
    data : str or arraylike
        string with the name of the column to extract data from, or an input
        array to use for each row in the geopandas dataframe
    key : string
        Data column name from `data` to map
    legend_name : string
        String used for the legend label on top of the plot 

    Returns
    -------
    map : folium map
        cloropleth map with different colors associated to each geometry in the
        geopandas dataframe, depending on the values.
    """

    map = folium.Map([54, -1.3],
                 zoom_start=8,
                 tiles="Cartodb Positron",
                 min_zoom=7,
                 max_zoom=10)
    
    folium.Choropleth(
    geo_data=gpd,
    data=data,
    columns=["LAD21NM", key],
    key_on="feature.properties.LAD21NM",
    # fill_opacity=0.1,
    line_weight=0.5,
    legend_name=legend_name,
    highlight=True,
    ).add_to(map)

    return map