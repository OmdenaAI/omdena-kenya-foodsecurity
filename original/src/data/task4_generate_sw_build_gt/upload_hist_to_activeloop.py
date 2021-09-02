import numpy as np
from hub import Dataset, schema
from matplotlib import pyplot as plt
import glob
import rasterio
from hub.schema import Image
from hub.schema import Text
import time

## Regions
# MOD09A1_TerraSurfaceReflectance
# output_hist_dir_one_year = './data/MOD09A1_TerraSurfaceReflectance_Senegal_regions/histograms_one_year'
# output_hist_dir_june_august = './data/MOD09A1_TerraSurfaceReflectance_Senegal_regions/histograms_june_august'
# output_hist_dir_half_year = './data/MOD09A1_TerraSurfaceReflectance_Senegal_regions/histograms_half_year'

# MYD11A2_Temperature
# output_hist_dir_one_year = './data/MYD11A2_Temperature_Senegal_regions/histograms_one_year'
# output_hist_dir_june_august = './data/MYD11A2_Temperature_Senegal_regions/histograms_june_august'
# output_hist_dir_half_year = './data/MYD11A2_Temperature_Senegal_regions/histograms_half_year'


## Departments
# MOD09A1_TerraSurfaceReflectance
# output_hist_dir_one_year = "./data/MOD09A1_TerraSurfaceReflectance_Senegal_departments/histograms_one_year"
# output_hist_dir_june_august = "./data/MOD09A1_TerraSurfaceReflectance_Senegal_departments/histograms_june_august"
# output_hist_dir_half_year = "./data/MOD09A1_TerraSurfaceReflectance_Senegal_departments/histograms_half_year"

# MYD11A2_Temperature
output_hist_dir_one_year = "./data/MYD11A2_Temperature_Senegal_departments/histograms_one_year"
output_hist_dir_june_august = "./data/MYD11A2_Temperature_Senegal_departments/histograms_june_august"
output_hist_dir_half_year = "./data/MYD11A2_Temperature_Senegal_departments/histograms_half_year"


# tag = "username/Senegal_MYD11A2_Temperature_histograms_regions"
# tag = "username/Senegal_MOD09A1_TerraSurfaceReflectance_regions"
# tag = "username/Senegal_MOD09A1_TerraSurfaceReflectance_departments"
tag = "username/Senegal_MYD11A2_Temperature_histograms_departments"

files_path_one_year = output_hist_dir_one_year + '/*.tif'
path_to_tiffs_hist_one_year = glob.glob(files_path_one_year)

files_path_june_august = output_hist_dir_june_august + '/*.tif'
path_to_tiffs_hist_june_august = glob.glob(files_path_june_august)

files_path_half_year = output_hist_dir_half_year + '/*.tif'
path_to_tiffs_hist_half_year = glob.glob(files_path_half_year)


def read_tiffs(path_to_tiffs_hist, tiffs_hist_list, labels):
    for tiff_path in path_to_tiffs_hist:
        img_array = rasterio.open(tiff_path).read()
        print(img_array.shape)
        tiffs_hist_list.append(img_array)
        if '/histograms_june_august/' in tiff_path:
            name = tiff_path.split('/histograms_june_august/')[1].split('.tif')[0]
        if '/histograms_one_year/' in tiff_path:
            name = tiff_path.split('/histograms_one_year/')[1].split('.tif')[0]
        if '/histograms_half_year/' in tiff_path:
            name = tiff_path.split('/histograms_half_year/')[1].split('.tif')[0]
        labels.append(name)

tiffs_hist_one_year = []
tiffs_hist_june_august = []
tiffs_hist_half_year = []
labels_one_year = []
label_june_august = []
label_half_year = []
read_tiffs(path_to_tiffs_hist_one_year, tiffs_hist_one_year, labels_one_year)
read_tiffs(path_to_tiffs_hist_june_august, tiffs_hist_june_august,label_june_august)
read_tiffs(path_to_tiffs_hist_half_year, tiffs_hist_half_year,label_half_year)

print(len(tiffs_hist_one_year))
dataset_tiff_one_year=np.stack(tiffs_hist_one_year)
dataset_tiff_june_august=np.stack(tiffs_hist_june_august)
dataset_tiff_half_year=np.stack(tiffs_hist_half_year)

# Create dataset
ds = Dataset(
    tag,
    shape=(len(tiffs_hist_one_year),),
    schema={
        "histograms_one_year": schema.Tensor(tiffs_hist_one_year[0].shape, dtype="float"),
        "histograms_june_august": schema.Tensor(dataset_tiff_june_august[0].shape, dtype="float"),
        "histograms_half_year": schema.Tensor(dataset_tiff_half_year[0].shape, dtype="float"),
        "names": Text(shape=(None,), max_shape=(1000,), dtype="int64")
    },
    mode="w+",
)

# Upload Data
ds["histograms_one_year"][:] = np.stack(dataset_tiff_one_year)
ds["histograms_june_august"][:] = np.stack(dataset_tiff_june_august)
ds["histograms_half_year"][:] = np.stack(dataset_tiff_half_year)
ds["names"][:] = labels_one_year
ds.commit()

# Load the data
print("Load data...")
ds = Dataset(tag)
print(len(ds["histograms_one_year"][0].compute()))
print("Done!")
