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

    def calculate_ndvi(self, band4_index=4, band3_index=3):
        """
        Calculate NDVI using NIR and Red bands.

        Parameters:
        - band4_index (int): Index of the NIR band (1-based)
        - band3_index (int): Index of the Red band (1-based)

        Returns:
        - tuple: (okay, ndvi_array) where okay is True/False
        """
        okay = True
        try:
            nir = self.dataset.read(band4_index).astype("float32")
            red = self.dataset.read(band3_index).astype("float32")
        except Exception as e:
            okay = False
            print(f"Error reading bands: {e}")
            return okay, None

        try:
            np.seterr(divide="ignore", invalid="ignore")
            ndvi = (nir - red) / (nir + red)
            ndvi = np.clip(ndvi, -1, 1)
            return okay, ndvi
        except Exception as e:
            okay = False
            print(f"Error calculating NDVI: {e}")
            return okay, None


# ##################
# # Block 4: 
# #   Set up a new smart vector class using geopandas
# #    that will have a method similar to what did in lab 4
# #    to calculate the zonal statistics for a raster
# #    and add them as a column to the attribute table of the vector

# class SmartVector:
#     def __init__(self, vector_path):
#         self.vector_path = vector_path
#         try:
#             self.gdf = gpd.read_file(vector_path)
#         except Exception as e:
#             raise RuntimeError(f"Error loading vector file: {e}")

#     def calculate_zonal_statistics(self, raster_path, stats=['mean'], column_name='zonal_stat'):
#         try:
#             zs = zonal_stats(self.gdf, raster_path, stats=stats, geojson_out=True)
#             self.gdf[column_name] = [z[stats[0]] for z in zs]
#         except Exception as e:
#             raise RuntimeError(f"Error calculating zonal statistics: {e}")
