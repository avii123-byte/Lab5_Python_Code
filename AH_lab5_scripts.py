# Lab 5 scripts

import AH_lab5_functions as l5
import matplotlib.pyplot as plt
import geopandas as gpd

#  Part 1:

#  Assign a variable to the Landsat file 
landsat_file = "Landsat_image_corv.tif"

# Pass this to your new smart raster class
smart_raster = l5.SmartRaster(landsat_file)

# Calculate NDVI and save to and output file
try:
    ndvi = smart_raster.calculate_ndvi()
    print("NDVI calculated successfully.")
except Exception as e:
    print(f"An error occurred while calculating NDVI: {e}")

# Part 2:
# Assign a variable to the parcels data shapefile path
parcels_file = "Benton_County_TaxLots.shp"

#  Pass this to your new smart vector class
smart_vector = l5.SmartVector(parcels_file)

#  Calculate zonal statistics and add to the attribute table of the parcels shapefile
try:
    smart_vector.calculate_zonal_statistics(landsat_file, stats=["mean"], column_name="mean_ndvi")
    print("Zonal statistics calculated successfully.")
    print(smart_vector.gdf.head())
except Exception as e:
    print(f"An error occurred while calculating zonal statistics: {e}")

#  Part 3: Optional
#  Use matplotlib to make a map of your census tracts with the average NDVI values
try:
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    smart_vector.gdf.plot(column="mean_ndvi", ax=ax, legend=True, cmap="YlGn")
    ax.set_title("Census Tracts with Average NDVI Values")
    plt.show()
except Exception as e:
    print(f"An error occurred while plotting: {e}")
