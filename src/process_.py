"""
Project Flow
~Read Data Frames
~CRS: 32638 UTM ZONE 38
~Cell Size:
~Create Grid
"""

import geopandas as gpd
import pandas as pd
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
# DF GPS DATA
df_gps = pd.read_csv(r'../assets/gps_data.csv')
gdf_gps = gpd.GeoDataFrame(df_gps, geometry=gpd.points_from_xy(df_gps.lat, df_gps.lon), crs=DATA_CRS)
del df_gps
gdf_gps.drop(columns=['lat', 'lon'], inplace=True)

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

merged_ap = gpd.sjoin(gdf_ap, cell, how='left', predicate='within').drop(columns=['geometry', 'Unnamed: 0']).dropna()
merged_ap['index_right'] = merged_ap['index_right'].astype(int)
del gdf_ap
merged_gps = gpd.sjoin(gdf_gps, cell, how='left', predicate='within').drop(columns=['geometry', 'Unnamed: 0']).dropna()
merged_gps['index_right'] = merged_gps['index_right'].astype(int)
del gdf_gps

#Drop Duplicate Columns
merged_gps.drop_duplicates(inplace=True)
merged_ap.drop_duplicates(inplace=True)


df_merged = pd.merge(merged_ap, merged_gps, on="index_right")

del merged_ap
del merged_gps


df_merged.rename(columns={'index_right': 'cell_index'}, inplace=True)
df_merged['cell_index'] = df_merged['cell_index'].astype(int)

df_merged = df_merged[['cell_index', 'mac_address', 'trip_id']]

cell.to_csv(r'Output/Cells_.csv', index=False)
df_merged.to_csv(r'Output/Merged_.csv', index=False)
