import numpy as np
import csv
from glob import glob

def csv_reader(path):
  list_fields = []
  with open(path) as csvfile:
    reader = csv.DictReader(csvfile) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        list_fields.append(row)
  return list_fields

path_base = "./data/IPAR_1500ha_millet/histograms_weeks_0_46/"
path_ndvi = path_base + "/ndvi/"
path_temp = path_base + "/temp/"
path_csv = './IPAR_yields_with_NDVI - Millet_2014.csv'
output_csv_path = path_base + '/IPAR_Millet_2014.csv'

path_ndvi_npy = glob(path_ndvi + "/*.npy")

ndvis_list = []
names_list = []
for path in path_ndvi_npy:
    ndvis = np.load(path)
    ndvis_list.append(ndvis)
    names_list.append("uuid:" + path.split("uuid_")[1].split("_")[0])

print("ndvi {}".format(len(ndvis_list)))
list_fields = csv_reader(path_csv)
print(len(list_fields))

indexes_to_delete = []
for i in range(len(list_fields)):
    if str(list_fields[i].get('Yield')) != "0.0" and str(list_fields[i].get('Yield')) != "":
        if list_fields[i].get('KEY') in names_list:
            print(list_fields[i].get('KEY'))
            ndvi = list(ndvis_list[names_list.index(list_fields[i].get('KEY'))])
            print(ndvi)
            list_fields[i]['ndvi'] = ndvi
    else:
        indexes_to_delete.append(i)

list_fields = [i for j, i in enumerate(list_fields) if j not in indexes_to_delete]
print("ndvi: {}".format(list_fields[10].get('ndvi')))
print("{} yield values are null".format(len(indexes_to_delete)))
print("Length list after removing null values: {}".format(len(list_fields)))

with open(output_csv_path, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(list_fields[0].keys()))
    writer.writeheader()
    for i in range(len(list_fields)):
        writer.writerow(list_fields[i])

print("Done! Modified csv file saved: {}".format(output_csv_path))
