import streamlit as st
import pandas as pd
import numpy as np 
from scipy import interpolate
import base64
from datetime import datetime

# interpolate more datapoints into the limited scale dataset
def upsample_coords(coord_list):
    # s is smoothness, set to zero
    # k is degree of the spline. setting to 1 for linear spline
    tck, u = interpolate.splprep(coord_list, k=1, s=0.0)
    upsampled_coords = interpolate.splev(np.linspace(0, 1, 100), tck)
    return upsampled_coords


# generate download link for the results csv file
def generate_download_link(result, filename):
    csv_file = result.to_csv(index=False)
    b64 = base64.b64encode(csv_file.encode()).decode()
    filename = "{}_{}.csv".format(filename, datetime.now())
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download Results as CSV</a>'
    return href