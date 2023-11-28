import pandas as pd
import numpy as np

data_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTrUrpE22TyzTFUzXJkI4BFqLTPMmqv6MSOmZZ5_e6MaOd15J4H2P40hpntDNICSg/pub?gid=2067425503&single=true&output=csv"

# read amd get rid of extra rows and columns
data = pd.read_csv(data_url, header=0, nrows=34, thousands=r',')
data = data[data.columns[:-1]]

# Keep columns with LAD21NM defined to match agains map data 
data = data[data["LAD21NM"].notna()]

