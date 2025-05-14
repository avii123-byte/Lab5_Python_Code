#####################
# Block 1:  Import the packages you'll need
import os, sys
import os
import rasterio
import geopandas as gpd
import numpy as np

##################
# Block 2: 
# set the working directory to the directory where the data are

# Change this to the directory where your data are

data_dir = r"R:\2025\Spring\GEOG562\Students\hamala\Labs\Lab5_2025\Lab5_Python_Code"
os.chdir(data_dir)
print(os.getcwd())


##################
# Block 3: 
#   Set up a new smart raster class using rasterio  
#    that will have a method called "calculate_ndvi"


class SmartRaster:
    def __init__(self, raster_path):
        if not os.path.exists(raster_path):
            raise FileNotFoundError(f"Raster file not found: {raster_path}")
        self.raster_path = raster_path

    def calculate_ndvi(self, red_band_index=3, nir_band_index=4, output_path="ndvi_output.tif"):
        """
        Calculate NDVI from Red and NIR bands.
        Band indices are 1-based (like rasterio).
        """

        try:
            with rasterio.open(self.raster_path) as src:
                red = src.read(red_band_index).astype('float32')
                nir = src.read(nir_band_index).astype('float32')
                meta = src.meta.copy()

            # Calculate NDVI
            np.seterr(divide='ignore', invalid='ignore')  # suppress division warnings
            ndvi = (nir - red) / (nir + red)

            # Update metadata for NDVI (single-band float32 output)
            meta.update(dtype=rasterio.float32, count=1)

            with rasterio.open(output_path, 'w', **meta) as dst:
                dst.write(ndvi, 1)

            print(f"NDVI written to {output_path}")
            return True, output_path
        
        except Exception as e:
            print(f"Failed to calculate NDVI: {e}")
            return False, str(e)




##################
# Block 4: 
#   Set up a new smart vector class using geopandas
#    that will have a method similar to what did in lab 4
#    to calculate the zonal statistics for a raster
#    and add them as a column to the attribute table of the vector
import geopandas as gpd
from rasterstats import zonal_stats

class SmartVector:
    def __init__(self, vector_path):
        if not os.path.exists(vector_path):
            raise FileNotFoundError(f"Vector file not found: {vector_path}")
        self.vector_path = vector_path
        self.vector = gpd.read_file(vector_path)

    def add_zonal_stats(self, raster_path, stat='mean', output_column='ZonalStat'):
        """
        Compute zonal statistics for each polygon and add the result as a new column.
        
        Parameters:
        - raster_path: path to the raster file
        - stat: statistic to compute (e.g., 'mean', 'sum', 'min', 'max', etc.)
        - output_column: name of the new column to store the result
        """
        try:
            print(f"Computing zonal stats: {stat} from raster: {raster_path}")
            stats = zonal_stats(self.vector, raster_path, stats=stat, geojson_out=True)

            # Extract the stat values
            values = [feature['properties'][stat] for feature in stats]

            # Add the column to the GeoDataFrame
            self.vector[output_column] = values

            print(f"Zonal statistics added as column '{output_column}'")
            return True
        except Exception as e:
            print(f"Error computing zonal statistics: {e}")
            return False

    def save(self, output_path):
        """
        Save the updated GeoDataFrame to a new file.
        """
        try:
            self.vector.to_file(output_path)
            print(f"Saved updated vector to: {output_path}")
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
