# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 21:25:55 2021

@author: jdt470
"""

#IMPORT MODULES
import os
import pandas as pd
import sys
import traceback
from functions_4tu import generate_tide_signals
from functions_4tu import generate_surge_hydrograph
from functions_4tu import generate_storm_tide_hydrograph

#FILE PATHS
projectdir = r'/projects/0/ESLRP/hydrographs/'
pxyn_coastal_points = pd.read_pickle(os.path.join(projectdir,'pxyn_coastal_points.xyn'))
station_nrs = pxyn_coastal_points.index.values

#LOOP OVER SELECTION OF STATIONS
stations = int(sys.argv[1])
if stations == 23800:
    stations_range = range(stations,23815)
else:
    stations_range = range(stations,stations+20)

#USER SETTINGS
percentile=0.99
rp=1000
make_plot='yes'
offset=0

#PROCESS STATIONS
for nr in stations_range:
    try:
        station = station_nrs[nr]
        print('\n','start processing station:',int(station))
        average_tide_signal, spring_tide_signal=generate_tide_signals(station,make_plot)
        surge_hydrograph_height, surge_hydrograph_duration_mean = generate_surge_hydrograph(station,percentile,make_plot)
        storm_tide_hydrograph_average_tide_signal,storm_tide_hydrograph_spring_tide_signal = generate_storm_tide_hydrograph(station,average_tide_signal,spring_tide_signal,surge_hydrograph_duration_mean,surge_hydrograph_height,percentile,rp,offset,make_plot)
        
        file_out = pd.DataFrame(data={'average_tide_signal':average_tide_signal,'spring_tide_signal':spring_tide_signal,'surge_hydrograph_height':surge_hydrograph_height,'surge_hydrograph_duration_mean':surge_hydrograph_duration_mean,'storm_tide_hydrograph_average_tide_signal':storm_tide_hydrograph_average_tide_signal,'storm_tide_hydrograph_spring_tide_signal':storm_tide_hydrograph_spring_tide_signal})
        file_out.to_pickle(os.path.join(projectdir,'4tu_output_data/rp%04d_percentile%0d/df_hydrographs_station_%05d.pkl'%(rp,percentile*100,station)))
        print('Finished! station:',int(station))
    except Exception:
        print('station = '+str(station)+' error = '+traceback.format_exc())
        with open('errors.txt', 'a') as f:
            f.write('station = '+str(station)+' error = '+traceback.format_exc())
        continue
