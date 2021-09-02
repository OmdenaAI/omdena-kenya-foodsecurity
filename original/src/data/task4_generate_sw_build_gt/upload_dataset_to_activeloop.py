import numpy as np
from hub import Dataset, schema

dataset_path = "./data/IPAR/histograms_weeks_19_30/dataset_Maize"
tag = "username/Senegal_IPAR_histograms_weeks_19_30_Maize"

histograms_path = dataset_path + '/histograms.npy'
yields_path = dataset_path + '/yields.npy'
ndvi_path = dataset_path + '/ndvi.npy'

histograms = np.load(histograms_path)
yields = np.load(yields_path)
ndvi = np.load(ndvi_path)
print(histograms.shape)
print(yields.shape)
print(ndvi.shape)

# Create dataset
ds = Dataset(
    tag,
    shape=(histograms.shape[0],),
    schema={
        "histograms": schema.Tensor(histograms[0].shape, dtype="float"),
        "yields": schema.Tensor(shape=(1,), dtype="float"),
        "ndvi": schema.Tensor(ndvi[0].shape, dtype="float"),
    },
    mode="w+",
)

# Upload Data
ds["histograms"][:] = histograms
ds["yields"][:] = yields
ds["ndvi"][:] = ndvi
ds.commit()

# Load the data
print("Load data...")
ds = Dataset(tag)
print(len(ds["histograms"][0].compute()))
print("Done!")


