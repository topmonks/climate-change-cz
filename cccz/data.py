import json
import os

import pandas as pd
import streamlit as st

import cccz.cfg as cfg


class StreamLitVis(object):
    """
        {
             year : {
                  temperature : N,
                  locations : {
                      name : location_name,
                      month_temperature: [1...12],
                  },
             },
             ...,
             ...,
             ...,
        }
    """

    def __init__(self):
        self._raw_data = {}

    def start(self):
        self._load_data()

    def _load_data(self):
        data_file_paths = []
        for root, dir_, files in os.walk(cfg.DATA_DIR):
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

                self._raw_data[int(fp_year[1])] = locations
