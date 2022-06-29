"""
Project Flow
~Read Data Frames
~CRS: 32638 UTM ZONE 38
~Cell Size:
~Create Grid
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import pyproj
import numpy as np
import shapely

DATA_CRS = pyproj.CRS.from_epsg(32638)
print('{CRS:', DATA_CRS, '}')

# DF AP
df_ap = pd.read_csv(r'../assets/ap1.csv')
gdf_ap = gpd.GeoDataFrame(df_ap, geometry=gpd.points_from_xy(df_ap.lat, df_ap.lon), crs=DATA_CRS)

del df_ap

gdf_ap.drop(columns=['lat', 'lon'], inplace=True)
# ax = gdf_ap.plot(markersize=.1, figsize=(12, 8), column='mac_address', cmap='GnBu')
print('Gathering Data')

# DF GPS DATA
df_gps = pd.read_csv(r'../assets/gps_data.csv')
gdf_gps = gpd.GeoDataFrame(df_gps, geometry=gpd.points_from_xy(df_gps.lat, df_gps.lon), crs=DATA_CRS)
del df_gps
gdf_gps.drop(columns=['lat', 'lon'], inplace=True)
# gdf_gps.plot(markersize=.1, column='trip_id', cmap='OrRd', ax=ax)

# PLOT ON WORLD SHP
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# world.to_crs(gdf_ap.crs).plot(ax=ax, color='none', edgecolor='black')
# GRIDDING
#

xmin, ymin, xmax, ymax = gdf_ap.total_bounds
n_cells = 50
cell_size = (xmax - xmin) / n_cells
grid_cells = []
for x0 in np.arange(xmin, xmax + cell_size, cell_size):
    for y0 in np.arange(ymin, ymax + cell_size, cell_size):
        # bounds
        x1 = x0 - cell_size
        y1 = y0 + cell_size
        grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))
cell = gpd.GeoDataFrame(grid_cells, columns=['geometry'],
                        crs=DATA_CRS)

# cell.plot(ax=ax, facecolor="none", edgecolor='grey')
# plt.plot()
# plt.show()

gdf_ap.rename(columns={'Unnamed: 0': 'S.no'}, inplace=True)
gdf_gps.rename(columns={'Unnamed: 0': 'S.no'}, inplace=True)

print('Joining...')
merged_ap = gpd.sjoin(gdf_ap, cell, how='left', predicate='within').drop(columns=['geometry']).dropna()
merged_ap['index_right'] = merged_ap['index_right'].astype(int)
del gdf_ap
merged_gps = gpd.sjoin(gdf_gps, cell, how='left', predicate='within').drop(columns=['geometry']).dropna()
merged_gps['index_right'] = merged_gps['index_right'].astype(int)
del gdf_gps

merged_gps.to_csv('MergedGps.csv', index=False)
merged_ap.to_csv('MergedAp.csv', index=False)

print('Merging')

df_merged = merged_ap.join(merged_gps, how='left', on="index_right", lsuffix='_caller', rsuffix='_kt')
pd.merge(merged_ap, merged_gps, on="index_right")

del merged_ap
del merged_gps


df_merged.rename(columns={'index_right': 'cell_index', 'S.no_x': 'id_ap', 'S.no_y': 'id_gps'}, inplace=True)
df_merged['cell_index'] = df_merged['cell_index'].astype(int)



# df_merged.dropna(inplace=True)

# print('Writing...')
cell.to_csv('Cells.csv', index=False)
df_merged.to_csv('GPS_AP_CELLS.csv', index=False)
