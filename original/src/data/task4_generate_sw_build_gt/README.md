Build Training Dataset using GEE Layers and yield statistics 

1. Use the script histograms.py to generate the histograms from images downloaded from GEE using the notebook (task 4: pull_GEE_data_Senegal_shapefile.ipynb)

! You need to have the images from the datasets: MYD11A2_Temperature_Senegal_regions, MOD09A1_TerraSurfaceReflectance_Senegal_regions and CopernicusGlobal_LandCover_Senegal_regions before to running this script. They can be found in the S3 bucket under /data.
One example of output folder of histograms for a period of one year (week 0 to week 46) can be found here (histograms_weeks_0_46)

2. Use the script make_datasets.py to combine satellite data bands (7) and temperature bands (2)
It will create a dataset folder under the histograms folder with npy files of a list of all histograms (9 bands) and a list of all associated yields.
This script uses the csv file senegal_yields_standardized

3. Upload histograms or dataset to Activeloop using the scripts upload_hist_to_activeloop / upload_dataset_to_activeloop

NB: the scripts generate_sw.py and visualize_layers_tiff.py are not currently used but might be helpful later 


If any questions about these scripts: you can ask Margaux Masson-Forsythe




