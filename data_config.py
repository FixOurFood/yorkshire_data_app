import pandas as pd
import streamlit as st

data_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRZzN2TqjclsNSGp4GvLkCJtJ0pSyly6aGbesf9vmJ19aUbs7oSxZSwxxLsP-hA5g/pub?gid=741035012&single=true&output=csv"

data = pd.read_csv(data_url, nrows=34, index_col=0)
data = data[data.columns[:-1]]