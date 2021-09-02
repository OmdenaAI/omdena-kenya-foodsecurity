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

path_csv = './data/task4_generate_sw_build_gt/data/IPAR_yields_with_NDVI - Rice_CSC_2014.csv'
output_csv_path = './data/task4_generate_sw_build_gt/data/rice_rice_CSC_combined_duplicates.csv'

keys = []
yields = []
productions = []
areas_planted = []

indexes_to_delete = []
for i in range(len(list_fields)):
    if str(list_fields[i].get('Yield')) != "0.0" and str(list_fields[i].get('Yield')) != "":
        if list_fields[i].get('KEY') in keys:
            print('\nDuplicate key: {}'.format(list_fields[i].get('KEY')))
            # yields = T /ha = (0.001 * kg) / ha
            index = keys.index(list_fields[i].get('KEY'))
            production_combined = float(list_fields[i].get('Quantity produced (Kg)')) + float(productions[index])
            areas_planted_combined = float(list_fields[i].get('Area planted')) + float(areas_planted[index])
            combined_yields = (production_combined*0.001) / areas_planted_combined
            print("Combined production: {} replacing {}".format(production_combined, list_fields[index]['Quantity produced (Kg)']))
            print("Combined areas: {} replacing {}".format(areas_planted_combined, list_fields[index]['Area planted']))
            print("Combined yields: {}".format(combined_yields))

            yields[index] = combined_yields
            productions[index] = production_combined
            areas_planted[index] = areas_planted_combined
            print(list_fields[index]['KEY'])
            list_fields[index]['Yield'] = combined_yields
            list_fields[index]['Quantity produced (Kg)'] = production_combined
            list_fields[index]['Area planted'] = areas_planted_combined
            indexes_to_delete.append(i)
            # need to keep the indexing right
            keys.append('')
            productions.append(0)
            areas_planted.append(0)
            yields.append(0)
        else:
            keys.append(list_fields[i].get('KEY'))
            yields.append(list_fields[i].get('Yield'))
            productions.append(list_fields[i].get('Quantity produced (Kg)'))
            areas_planted.append(list_fields[i].get('Area planted'))
    else:
        indexes_to_delete.append(i)

print("Removed {} duplicates".format(len(indexes_to_delete)))
list_fields = [i for j, i in enumerate(list_fields) if j not in indexes_to_delete]
print(len(list_fields))

with open(output_csv_path, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(list_fields[0].keys()))
    writer.writeheader()
    for i in range(len(list_fields)):
        writer.writerow(list_fields[i])

print("File saved {}".format(output_csv_path))
