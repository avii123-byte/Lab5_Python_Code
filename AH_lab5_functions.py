#####################
# Block 1:  Import the packages you'll need
import os, sys
import rasterio
import geopandas as gpd
import numpy as np
from rasterstats import zonal_stats  # this is needed for zonal statistics

##################
# Block 2: 
# set the working directory to the directory where the data are

# Change this to the directory where your data are

data_dir = r"R:\2025\Spring\GEOG562\Students\hamala\Labs\Lab5_2025"
os.chdir(data_dir)
print(os.getcwd())


##################
# Block 3: 
#   Set up a new smart raster class using rasterio  
#    that will have a method called "calculate_ndvi"

class SmartRaster:
    def __init__(self, raster_path):
        self.raster_path = raster_path
        try:
            self.dataset = rasterio.open(raster_path)
        except Exception as e:
            raise RuntimeError(f"Error opening raster file '{raster_path}': {e}")

    def calculate_ndvi(self, red_band_index=4, nir_band_index=5):
        try:
            if red_band_index > self.dataset.count or nir_band_index > self.dataset.count:
                raise ValueError("Specified band indices exceed number of bands in the raster.")
            red = self.dataset.read(red_band_index).astype("float32")
            nir = self.dataset.read(nir_band_index).astype("float32")
            np.seterr(divide="ignore", invalid="ignore")
            ndvi = (nir - red) / (nir + red)
            return ndvi
        except Exception as e:
            raise RuntimeError(f"Error calculating NDVI for raster '{self.raster_path}': {e}")


##################
# Block 4: 
#   Set up a new smart vector class using geopandas
#    that will have a method similar to what did in lab 4
#    to calculate the zonal statistics for a raster
#    and add them as a column to the attribute table of the vector

class SmartVector:
    def __init__(self, vector_path):
        self.vector_path = vector_path
        try:
            self.gdf = gpd.read_file(vector_path)
        except Exception as e:
            raise RuntimeError(f"Error loading vector file: {e}")

    def calculate_zonal_statistics(self, raster_path, stats=['mean'], column_name='zonal_stat'):
        try:
            zs = zonal_stats(self.gdf, raster_path, stats=stats, geojson_out=True)
            self.gdf[column_name] = [z[stats[0]] for z in zs]
        except Exception as e:
            raise RuntimeError(f"Error calculating zonal statistics: {e}")
