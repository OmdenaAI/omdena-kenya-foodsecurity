import numpy as np
import rasterio
import matplotlib.pyplot as plt
import cv2
import glob
import tifffile
import os
from tqdm import tqdm

######################## Variables ###################################
# Download folder from the S3 bucket (s3://omdena-gpsdd-senegal/data/IPAR_data/IPAR_1500ha_maize_2014/)
# other crop types can be found here: s3://omdena-gpsdd-senegal/data/IPAR_data
files_path = "./data/IPAR_data/IPAR_1500ha_maize_2014/"

files_path_temp = files_path + "/MYD11A2_Temperature_Senegal"
files_path_sat = files_path + "/MOD09A1_TerraSurfaceReflectance_Senegal"
files_path_landcover = files_path + "/CopernicusGlobal_LandCover_Senegal"

# weeks = [0,46] # one year
weeks = [19,30] # first week of June to last week of August
# weeks = [0,23] # half year

output_histograms_path = files_path + "/histograms_weeks_{}_{}/".format(weeks[0], weeks[1])
output_dir_sat = output_histograms_path + "/sat/"
output_dir_plot_figures_sat = output_dir_sat + "/figures/"
ndvi_save_path = output_histograms_path + "/ndvi.npy"
output_dir_temp = output_histograms_path + "/temp/"
output_dir_plot_figures_temp = output_dir_temp + "/figures/"

show_figures = True
CROP_LABEL = 40
NUM_REF_BANDS = 7
RED_BAND = 0 # 0-indexed, so this is band 1
NIR_BAND = 1 # Near infrared.

bin_seq_list_temp = [np.linspace(13000,16500,33), np.linspace(13000,15500,33)]
num_bands_temp = 2 # night and day
bin_seq_list_sat = [np.linspace(1, 2200, 33),
          np.linspace(900, 4999, 33),
          np.linspace(1, 1250, 33),
          np.linspace(150, 1875, 33),
          np.linspace(750, 4999, 33),
          np.linspace(300, 4999, 33),
          np.linspace(1, 4999, 33)]
num_bands_sat = 7 # 7 bands of reflectance

######################## Functions ###################################
def check_if_folder_exists_creates_it_if_no(path_to_dir):
    if not os.path.exists(path_to_dir):
        print("Creating output folder: {} ...".format(path_to_dir))
        os.mkdir(path_to_dir)

def calc_ndvi(sat_tensor):
    num_times = sat_tensor.shape[2]//NUM_REF_BANDS
    sat_tensor = np.transpose(sat_tensor.reshape(-1, sat_tensor.shape[2]), [1, 0]) #bands*time, flattened image
    ndvi_arr = np.empty([num_times])
    for t in range(num_times):
        offset = t*NUM_REF_BANDS
        sat_slice = sat_tensor[[offset + RED_BAND, offset + NIR_BAND], :]
        zeros_mask = np.where((sat_slice[0] > 0) + (sat_slice[1] > 0))
        sat_slice = np.squeeze(sat_slice[:, zeros_mask]).astype(np.float32) # remove indices where NIR = RED = 0
        red = sat_slice[0]
        nir = sat_slice[1]
        ndvi_arr[t] = np.average((nir - red)/(nir + red))
    return ndvi_arr


### Function calc_32_bins_histograms ####
# Generates 32-bins pixel counts histograms from GeoTiff
# The resulting histogram's size is [normalized bin values, number of timestamps, band]
# NB: number of timestamps N = N-day composite of GEE layers
# To be able to concanete histograms, all GeoTiff used need to have the same number of timestamps
# otherwise the sizes of the histrograms won't match
#
# Input:
# image: GeoTiff layer
# num_bands : number of bands combined in the image
# bin_seq_list: lindscape list to create the corresponding histograms
# weeks: time in weeks of the months before harvest. for 1 year: weeks = [0,46]
# for first week June to last week August: weeks = [19,30]
def calc_32_bins_histograms(image, num_bands, bin_seq_list, weeks=[0,46]):
    num_bins = 32
    num_times = image.shape[2] // num_bands
    hist = np.zeros([num_bins, num_times, num_bands])
    for i in range(image.shape[2]):
        band = i % num_bands
        density, _ = np.histogram(image[:, :, i], bin_seq_list[band], density=False)
        total = density.sum()  # normalize over only values in bins
        hist[:, i // num_bands, band] = density / float(total) if total > 0 else 0
    return hist[:, weeks[0]:weeks[1]]

#### Function mask_image
# Removes non-crop pixels in all 2D slices of 3D image tensor of shape X x Y x (bands/time)
def mask_image(img, mask, num_bands):
    num_imgs = img.shape[2]//num_bands
    assert num_imgs == int(num_imgs)
    for t in range(num_imgs):
        for b in range(num_bands):
            img[:, :, t*num_bands + b] = np.multiply(img[:, :, t*num_bands + b], mask)
    return img


def generate_histograms(files_path, num_bands, bin_seq_list, output_dir):
    path_to_tiffs = glob.glob(files_path + '/*.tif')
    path_to_tiffs.sort()
    path_to_masks = glob.glob(files_path_landcover + '/*.tif')
    path_to_masks.sort()

    for i in tqdm(range(0, len(path_to_tiffs))):
        name = path_to_tiffs[i].split(files_path)[1].split(".tif")[0] + "_hist"
        path_file = output_dir + name + ".tif"
        check_if_folder_exists_creates_it_if_no(output_dir + "/../ndvi/")
        path_file_ndvi = output_dir + "/../ndvi/" + name + "_ndvi.npy"
        output_dir_plot_figures = output_dir + "/figures/"
        check_if_folder_exists_creates_it_if_no(output_dir_plot_figures)
        path_file_plots = output_dir_plot_figures + name

        image = rasterio.open(path_to_tiffs[i])
        image_read = image.read()
        print(image_read.shape)
        image_read = np.transpose(image_read, (1, 2, 0))

        # Read landcover and use it for masking all non crop areas
        print(path_to_masks[i])
        landcover_mask = rasterio.open(path_to_masks[i]).read()
        landcover_mask[landcover_mask != CROP_LABEL] = 0
        landcover_mask[landcover_mask == CROP_LABEL] = 1
        print(landcover_mask.shape)
        print("\n\nFile: {}".format(path_to_tiffs[i]))
        print("Landcover: {}".format(path_to_masks[i]))

        masked_image = mask_image(image_read, landcover_mask, num_bands)
        if "sat" in output_dir:
            print("Calculating ndvi values ...")
            ndvi = calc_ndvi(image_read)
            np.save(path_file_ndvi, ndvi)
            print("ndvi values saved under {}".format(ndvi_save_path))

        hist = calc_32_bins_histograms(masked_image, num_bands, bin_seq_list, weeks)

        print(hist.shape)
        if show_figures:
            plt.figure(1)
            plt.suptitle(name.split('.tif')[0])
            plt.subplot(121)
            plt.imshow(masked_image[:, :, 0])
            plt.subplot(122)
            plt.imshow(hist[:, :, 0])
            # plt.show()
            plt.savefig(path_file_plots.split('.tif')[0] + '.png')

        print("Saving {} ...".format(path_file))
        tifffile.imsave(path_file, hist, planarconfig='contig')

### Checking folder exist and create them if not
check_if_folder_exists_creates_it_if_no(output_histograms_path)
check_if_folder_exists_creates_it_if_no(output_dir_sat)
check_if_folder_exists_creates_it_if_no(output_dir_temp)

######################## Start generating histograms ###################################

######################## Satellite ########################
generate_histograms(files_path_sat, num_bands_sat, bin_seq_list_sat, output_dir_sat)

######################## Satellite ########################
generate_histograms(files_path_temp, num_bands_temp, bin_seq_list_temp, output_dir_temp)




