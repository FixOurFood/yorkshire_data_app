import pandas as pd
import streamlit as st

_data_url = st.secrets["data_url"]
_metadata_url = st.secrets["metadata_url"]

# read amd get rid of extra rows and columns
data = pd.read_csv(_data_url, header=0, nrows=34, thousands=r',', na_values=["No data"])
data = data[data.columns[:-1]]

# Keep columns with LAD21NM defined to match agains map data 
data = data[data["LAD21NM"].notna()]

#### Format columns

# Change percentages to values
_percentage_keys = [
    "Child poverty: Income deprivation affecting children index (IDACI) - 2019 - Proportion - % (DLUHC)",
    "Access to Healthy Assets & Hazards (AHAH Index - 2022 (OHID / CDRC): Percentage of the population who live in LSOAs which score in the poorest performing 20% on the AHAH index",
    "Alcohol-related mortality 2021 - per 100,000 people (OHID) - based on ONS data",
    "Percentage of physically active adults - 2021/22 (OHID)",
    "Percentage of physically active children and young people - 2021/22 (OHID)",
    # "Percentage of adults (aged 18 plus) classed as overweight or obese - 2021/22 (OHID)",
    "Diabetes prevalence (QOF) - 2021/22 (OHID)",
    "Percentage of people in employment (ONS) - Annual Population Survey (estimates)",
    "Economic inactivity rate - 2021/22 - ONS (Annual Population Survey)",
    "Proportion of resident population aged 16-64 claiming Jobseeker's Allowance or Universal Credit - July 2023 (ONS)",
    "Unemployment estimates - Labour Force Survey (ONS) - April-March 2023 - Rate (%)",
    "Fuel poverty (low income, low energy efficiency methodology) - 2020 - Proportion - % (OHID)"
]

for key in _percentage_keys:
    data[key] = data[key].str.rstrip('%').astype('float')

# These keys can be converted to a population percentage within the local authority
convertible_to_LA_pop_percentage_keys = [
    "Demographics - Ethnicity of usual residents - Asian, Asian British (Census 2021, estimates) ",
    "Demographics - Ethnicity of usual residents - Black, Black British, Caribbean or African (Census 2021, estimates) ",
    "Demographics - Ethnicity of usual residents - Mixed or Multiple ethnic groups (Census 2021, estimates) ",
    "Demographics - Ethnicity of usual residents - White (Census 2021, estimates) ",
    "Demographics - Ethnicity of usual residents - Other ethnic group (Census 2021, estimates) ",
    "Household deprivation level (Census 2021)",
]

metadata = pd.read_csv(_metadata_url)