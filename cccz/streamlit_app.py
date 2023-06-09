import os

import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    rd = {}
    locs = []
    yrs = []

    data_file_paths = []
    for root, dir_, files in os.walk('./data'):
        for filename in files:
            data_file_paths.append(
                (os.path.join(root, filename), filename.split('.')[0])
            )

    for fp_year in data_file_paths:
        with open(fp_year[0], encoding='utf-8') as f:
            yrs.append(fp_year[1])
            lines = f.readlines()[1:]
            locations_ = {}
            for line in lines:
                line_arr = line.split(',')
                if line_arr[0] not in locs:
                    locs.append(line_arr[0])

                locations_[line_arr[0]] = {
                    'month_temperatures': [
                        float(x) for x in line_arr[1:-1]
                    ],
                    'year_temperature': float(line_arr[-1].strip())
                }

            rd[int(fp_year[1])] = locations_

    yrs = sorted(yrs)

    return rd, locs, yrs


raw_data, locations, years = load_data()

selected_location = st.selectbox("Location", locations)
selected_year = st.selectbox("Year", years)
selected_month = st.selectbox("Month", range(1, 13))
t1, t2, t3 = st.tabs([
    "Year Temperature by  Month",
    "Temperature by Year",
    "Month temperature by Years"
])
# ==============================================================================

with t1:
    st.caption("Temperatures by Month")
    df = pd.DataFrame(
        {
            'temperatures': raw_data[int(selected_year)][selected_location][
                'month_temperatures'
            ],
            'months': range(1, 13)
        },
        columns=['temperatures', 'months'],
    )
    st.line_chart(df, x='months')

# ==============================================================================

yr_temps = []
yrs = []
for k, v in raw_data.items():
    if selected_location in raw_data[k].keys():
        t = raw_data[k][selected_location]['year_temperature']
        yr_temps.append(t)
        yrs.append(k)

with t2:
    st.caption("Temperatures by Year")
    df2 = pd.DataFrame(
        {
            'temperatures': yr_temps,
            'years': yrs
        },
        columns=['temperatures', 'years'],
    )
    st.line_chart(df2, x='years')

# ==============================================================================


month_temps_by_yr = []
for k, v in raw_data.items():
    if selected_location in raw_data[k].keys():
        t = raw_data[k][selected_location]['month_temperatures'][
            selected_month - 1
            ]
        month_temps_by_yr.append(t)

with t3:
    df3 = pd.DataFrame(
        {
            'temperatures': month_temps_by_yr,
            'years': yrs
        },
        columns=['temperatures', 'years'],
    )
    st.line_chart(df3, x='years')
