import os

import pandas as pd
import streamlit as st

raw_data = {}


@st.cache
def load_data():
    data_file_paths = []
    for root, dir_, files in os.walk('./data'):
        for filename in files:
            data_file_paths.append(
                (os.path.join(root, filename), filename.split('.')[0])
            )

    for fp_year in data_file_paths:
        with open(fp_year[0], encoding='utf-8') as f:
            lines = f.readlines()[1:]
            locations = {}
            for line in lines:
                line_arr = line.split(',')
                locations[line_arr[0]] = {
                    'month_temperatures': [
                        float(x) for x in line_arr[1:-1]
                    ],
                    'year_temperature': float(line_arr[-1].strip())
                }

            raw_data[fp_year[1]] = locations


df = pd.DataFrame(
    {
        'temperatures': raw_data[2022]['month_temperatures'],
        'months': range(1, 13)
    },
    columns=['temperatures', 'months']
)

st.line_chart(df)
