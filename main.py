import streamlit as st
import pandas as pd
import numpy as np 
from data_auxiliary import *

def main():

    st.set_page_config(
                        page_title="Qlipper",
                        page_icon="📈",
                        # layout="wide",
                        initial_sidebar_state = "collapsed",
                    )

    st.title("Qlipper")
    st.markdown("#### a small Web-App to get Ct values from qPCR absorption curves")
    st.markdown(" --- ")

    data_input = st.file_uploader("Please, enter your data here", help = "Upload a csv file with absorption values.")

    st.markdown(" --- ")

    container1 = st.container()
    col1, col2 = container1.columns([1,2.5]) # two columns to fit the graph and csv preview in

    if data_input:
        # read data and get min and max values for the threshold slider
        data = pd.read_csv(data_input)
        data.index +=1 # re-index to start from 1 as the first datapoint would be after the first cycle not the 0th cycle
        tmax, tmin = data.max().max(), data.min().min()
        keys = data.keys()
        
       
        # define the threshold slider with 100 steps
        slider = st.slider("Threshold", min_value = float(tmin), max_value = float(tmax), value = float(2 * tmin), step=float((tmax-tmin)/10))   
        
        # add a column for the threshold line with the slider value into the dataframe for plotting
        k0 = keys[0]
        line_data = [slider for i in data[k0]]
        data["Ct"] = line_data
    
        # store x-intersections = CT values
        intersections_x = []
        # we compute for each absorption curve within the dataset
        for k in keys:
            # first we upscale the dataset by interpolation
            tmp = upsample_coords(
                [
                    [i for i in np.arange(len(data[k]))],  # and we manually add the cycle number as column
                    data[k]
                ]
            )

            # next we generate back our x-range for the actual cycle number
            xs = np.array([i for i in np.arange(1, len(data[keys[1]])+1, step = len(data[keys[1]])/len(tmp[1]))]) # essentially the step is to fit all the interpolated datapoints within the range of the original cycle number
            y_data = np.array(tmp[1])
            y_line = np.array([slider for i in tmp[1]]) # to fit the slider line over the entire interpolated line we create a new set

            # now we search for intersecting points of y_data and y_line
            idx=np.argwhere(np.diff(np.sign(y_data - y_line )) != 0).reshape(-1)

            # and we compute the averaged x,y coordinates of the intersections from both y_data and the slider line
            for i in range(len(idx)):
                x_value = (xs[idx[i]]+xs[idx[i]+1])/2.
                y_value = (y_data[idx[i]]+y_data[idx[i]+1])/2.
                intersections_x.append(x_value)
        
        # now we compile the results
        results = {"Sample" : keys, "CT" : intersections_x}
        results = pd.DataFrame(results)

        # show curives
        col2.line_chart(data, use_container_width=True)
        
        # show preview of results and download link
        col1.dataframe(results)
        col1.markdown(generate_download_link(results, "CT_values"), unsafe_allow_html=True)



if __name__ == '__main__':
    main()

