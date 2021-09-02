import rasterio
import numpy as np
import glob
import os
import csv

# !! Folder's structure must be: folder, folder/sat, folder/temp
# Folder in the S3 bucket: s3://omdena-gpsdd-senegal/data/IPAR_data/IPAR_1500ha_maize_2014/histograms_weeks_0_46/
histograms_path = "./data/IPAR_data/IPAR_1500ha_maize_2014/histograms_weeks_0_46/"
yield_statistics_path = "./data/IPAR_yields_with_NDVI - Maize_2014.csv"
crop_type = "Maize"

output_path = histograms_path + "/dataset_" + crop_type
output_path_hist_npy = output_path + "/histograms.npy"
output_path_yields_npy = output_path + "/yields.npy"
output_path_ndvi_npy = output_path + "/ndvi.npy"

ndvi_npy_path = histograms_path + "/ndvi.npy"
histograms_paths_sat = glob.glob(histograms_path + "/sat/" + "./*tif")
histograms_paths_sat.sort()
histograms_paths_temp = glob.glob(histograms_path + "/temp/" + "./*tif")
histograms_paths_temp.sort()
ndvi_paths = glob.glob(histograms_path + "/ndvi/" + "./*npy")
ndvi_paths.sort()
histograms_list = []
yields = []
yields_linked_to_hist = []
ndvi_list = []

def check_if_folder_exists_creates_it_if_no(path_to_dir):
    if not os.path.exists(path_to_dir):
        print("Creating output folder: {}...".format(path_to_dir))
        os.mkdir(path_to_dir)

def get_yield_region_department(name_region_department, year, crop_type="Rice"):
    yield_value = 0
    for i in range(0, len(yields)):
        if name_region_department.lower() == yields[i][rows.index('Region')].lower() \
                and crop_type.lower() == yields[i][rows.index('Crop')].lower() \
                and year == yields[i][rows.index('Year')]:
            yield_value = yields[i][rows.index('Yield')]
    return yield_value

def get_yield_key(key):
    yield_value = 0
    for i in range(0, len(yields)):
        # print(key.lower())
        # print(yields[i][rows.index('KEY')].lower())
        if key.lower() == yields[i][rows.index('KEY')].lower().split(':')[1]:
            yield_value = yields[i][rows.index('Yield')]
    return yield_value

def get_ndvi(ndvi_npy_path):
    ndvi = np.load(ndvi_npy_path)
    return ndvi

check_if_folder_exists_creates_it_if_no(output_path)

########################## YIELDS ##########################
print("Starting to save the yield...")
with open(yield_statistics_path) as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        row_info = []
        rows = []
        for (k,v) in row.items(): # go over each column name and value
            row_info.append(v)
            rows.append(k)
        yields.append(row_info)
print("yields file read, there are {} rows in the file\n".format(len(yields)))

########################## HISTOGRAMS ##########################
print("\nStarting to read the histograms and saving them as npy...")
not_saved = 0
for idx in range(0, len(histograms_paths_sat)):
    print(histograms_paths_sat[idx])
    print(histograms_paths_temp[idx])
    hist_sat_img = rasterio.open(histograms_paths_sat[idx]).read() # 7 bands
    hist_temp_img = rasterio.open(histograms_paths_temp[idx]).read() # 2 bands

    # Get info in name file
    # name format for regions should be senegal_reflectance_senegal-dakar_2015-01-01_2016-01-01_hist.tif
    # name format for departments should be senegal_reflectance_senegal-dakar-dakar_2015-01-01_2016-01-01_hist.tif.tif
    split_name = histograms_paths_sat[idx].split('/')[-1].split('_')[2]
    regions_name = split_name.split('-')
    if len(regions_name) == 5: #saint-louis for example
        region_names = regions_name[-2] + '-' + regions_name[-1]
    else:
        region_names = regions_name[-1]
    key = histograms_paths_sat[idx].split('/')[-1].split('uuid_')[1].split('_2')[0]

    # print(histograms_paths_sat[idx])
    year = histograms_paths_sat[idx].split(region_names + '_')[1].split('-01')[0]

    # get yield for region/department, year and crop type
    # yield_value_for_region_year_crop = get_yield_region_department(region_names, year=year, crop_type=crop_type)
    yield_value_for_region_year_crop = get_yield_key(key)

    # get ndvi (saved in same order as sat histograms)
    ndvi = get_ndvi(ndvi_paths[idx])

    # if no yield value for these region, year and crop type, not saving the histogram
    if str(yield_value_for_region_year_crop) != "0" and str(yield_value_for_region_year_crop) != "0.0" and str(yield_value_for_region_year_crop) != '':
        yields_linked_to_hist.append([float(yield_value_for_region_year_crop)])
        print("Saving histogram of {} year {}, yield of {} is {}".format(region_names, year, crop_type, yield_value_for_region_year_crop))

        # Combine bands of sat and temperature in one array: results in 9 bands
        hists_concat = np.concatenate((hist_sat_img, hist_temp_img), axis=0)
        hists_concat = np.transpose(hists_concat, (1, 2, 0))
        histograms_list.append(hists_concat)

        # Save ndvi corresponding
        ndvi_list.append(ndvi)
    else:
        not_saved = not_saved + 1
        print("Not saving histogram of {} year {} because yield of {} is {}".format(region_names, year, crop_type, yield_value_for_region_year_crop))


print("There are {} histograms in the list".format(len(histograms_list)))
print("{} histograms were not saved".format(not_saved))
print("Shape of first concatenated histogram in list of all histograms: {}".format(histograms_list[0].shape))
print("Shape should be = ({}, {}, {})".format(hist_sat_img.shape[0] + hist_temp_img.shape[0],
                                    hist_sat_img.shape[1],
                                    hist_sat_img.shape[2]))

print("\nSaving all histograms as npy file...")
np.save(output_path_hist_npy, np.array(histograms_list))
print("All histograms saved")

print("\nSaving all ndvi as npy file (replacing existing one because some histograms are not saved (lack of yield) ...")
np.save(output_path_ndvi_npy, np.array(ndvi_list))
print("ndvi file updated")

print("\nYields linked to histograms: {}".format(len(yields_linked_to_hist)))
print("Saving all yields as npy file...")
np.save(output_path_yields_npy, yields_linked_to_hist)
print("All yields saved")


################## TEST if data correctly saved #####################
print("\nTest to check if data was correctly exported... "
      "by reading exported .npy files. Shapes should match with previous shapes ")
test_read_hist_npy = np.load(output_path_hist_npy)
print("\nShape of all histograms npy file saved: {} "
      "should match: {}".format(test_read_hist_npy.shape, np.array(histograms_list).shape))
assert test_read_hist_npy.shape == np.array(histograms_list).shape

test_read_yields_npy = np.load(output_path_yields_npy)
print("\nShape of all yields npy file saved: {} "
      "should match {}".format(test_read_yields_npy.shape, np.array(yields_linked_to_hist).shape))
assert test_read_yields_npy.shape == np.array(yields_linked_to_hist).shape

test_read_ndvi_npy = np.load(output_path_ndvi_npy)
print("\nShape of all ndvi npy file saved: {} "
      "should match {}".format(test_read_ndvi_npy.shape, np.array(ndvi_list).shape))
assert test_read_ndvi_npy.shape == np.array(ndvi_list).shape

print("Done!")
