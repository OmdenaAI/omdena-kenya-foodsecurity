
# Crop Identification and Yield Estimation

## Summary
Using open source satellite data and AI to identify crops and estimate the yield. We proposed a crop identification method based on Random Forest algorithm and calculated the yield estimates.

<img src="images/demo.gif" width="80%" />

# Sample Output

Sample 1:

<img src="images/sample1.png" width="80%" />

<img src="images/sample1_1.png" width="40%" />

Sample 2:

<img src="images/sample2.png" width="80%" />

<img src="images/sample2_1.png" width="40%" />

# Demo videos

* [Demo 1](images/demo1.mp4)
* [Demo 2](images/demo2.mp4)

# Requirements:
1. Latest version of Geemap installed.
2. [Model file](https://omdena-gpsdd-senegal.s3-us-west-1.amazonaws.com/data/Task11/trained_model_smote_sentinelV2.sav) from Omdena S3 bucket; save the model inside the model folder.
3. Internet connection to collect satellite data.
4. Active Google earth engine account.
5. Recommendeded: install [Anaconda](https://docs.anaconda.com/anaconda/install/) to manage packages and to create an environment (optional)

Note: the user interface won't work in Google Colab.


# How it works
Every object, including every crop, reflects light of different wavelengths in unique way. We are using this principle along with multitemporal and multispectral remote sensing images to identify the crops. 

Crops are identified using the reflectance value in every band over a region from the Sentinel satellite.



**Sentinel bands wavelength info** 

<img src="images/bandInfo.png" width="60%" />


# Ground truth data
Ground truth data in the form of geographical areas labelled with the crops grown there are lacking in Senegal. Instead, we used ground truth data from South Africa obtained from [Zindi - Farm Pin Crop Detection Challenge.](https://zindi.africa/competitions/farm-pin-crop-detection-challenge/data)

The crop grown in each field was verified in person and with drones in 2017. There are 7 crop types (**Cotton, Dates, Grass, Lucern, Maize, Pecan, Vineyard**) present in these fields, plus **vacant fields**, and fields that have both **vineyards and pecans intercropped** in one field.

# Our approach
* We used the shapefiles from the Zindi challenge and collected data from Google Earth Engine.
* We split the data in to 2 seasons each containing 4 months, and used multitemporal data fusion to get 2 images representing 2 seasons for every field in the training data.  
* We trained multiple models (SVM, Logistic Regression, LSTM and Random forest) and selected the best model (Random Forest).
* Using the Random Forest model, we calculated a crop estimation at the pixel level of the satellite image.

<img src="images/flowDiagram.png" width="60%" />

## Steps followed to identify crops and estimate yield:
 1. Collect the satellite image for the specified region.
 2. Preprocess the data to get the reflectance value of every band.
 3. Pass the reflectance value of every pixel to the Random Forest model one by one and store the corresponding results in the form of a prediction matrix.
 4. Get the unique count values from the prediction matrix.
 5. Multiply unique count with the area of 1 pixel to get yield estimation. 
 
*Note:* Each of the unique values in prediction matrix represents crop ID and the value of unique count represents the propotionality constant of area.

Example:
```python
PredictionMatrix = [[0,1,0],
                    [2,0,2],
                    [0,0,2]]
```
Each element in the matrix is the output from the model. Each value is classification ID (see "Model output labels" below).

Here the values and unique counts are as follows.
Values | Unique count
--- | --- 
0 |5
1 |1
2 |3

Let area of 1 pixel = 2 acre

So, area of crop 0 = 5 * 2 = 10 acre

area of crop 1 = 1 * 2 = 2 acre

area of crop 2 = 3 * 2 = 6 acre


# Model output labels
Classification ID | Classification Labels
--- | --- 
0 |No classification
1 |Cotton
2 |Dates
3 |Grass
4 |Lucern
5 |Maize
6 |Pecan
7 |Vacant Land
8 |Vineyard
9 |Vineyard & Pecan ("Intercrop")




# Overview on UI
The UI has 4 steps. Steps have to be followed in the same order. 

<img src="images/UI_overview.png" width="60%" />

* Step 1: choose an approximate date on which crop is grown. The Sentinel satellite captures images over a region every 5 days. So from the choosen date it will search for images in the last 30 days and pick the best image with lowest cloud cover.


* Step 2: select the rectangle icon on the map to select the region. Then click the "ok" button. It will show the image for the specified date on the map and will provide the value of the total area.

Note: the initial image preview in the map is the latest Google Maps image and it is not the Sentinel satellite image.

* Step 3: load the model. Once the model is finished loading it is not necessary to load the model again for subsequent estimation.

* Step 4: the time taken to get the result is directly propotional to the area of selected region. The greater the area, the longer the processing time.


# Project setup

**Conda Installation**

```
conda install --file Requirements.txt
```
**To create environment and install dependency**
```
conda create --name <env_name> --file Requirements.txt
```
**Dependent libraries:**
```
earthengine-api
geemap
numpy
seaborn
matplotlib
py-opencv
opencv
ipywidgets
voila
```


# Steps to run the app
1. Open app.ipynb

<img src="images/appNotebook.png" width="60%" />

2. Click on Voila button

<img src="images/voilaButton.png" width="30%" />

# Folder structure

* `data` - Contains training data for the model
* `images` - Contains images and videos for documentation
* `model` - Contains model file
* `app.ipynb` - The main notebook which acts as user interface
* `ModelTraining.ipynb` - Notebook used to train the model
* `Requirements.txt` - File containing list of dependent library
* `README.md` - Contains documentation  
 
# Model benchmark 
Results are based on the ground truth data of South Africa obtained from [Zindi - Farm Pin Crop Detection Challenge.](https://zindi.africa/competitions/farm-pin-crop-detection-challenge/data)

<img src="images/testScores.png" width="60%" />

**Confusion matrix**

<img src="images/confusionMatrix.png" width="60%" />

**Evaluation for Senegal**

To evaluate how well the model trained on South African crop fields generalises to Senegal, we adjusted the threshold so that the estimated total area of Senegal planted with maize is as close as possible to the statistics from DAPSA ([obtained here](https://senegal.opendataforafrica.org/idtepgd/agriculture-r%C3%A9sultats-des-campagnes-agricoles)). We then applied the model to every region individually from a different year, and calculated the difference between the model's estimated area planted with maize and the actual observed area planted with maize for every region. In the best case scenario, the accuracy is 12.7%.

# Applications
* Our estimates of area planted with each crop can be used to estimate crop productivity.
* Enables policy makers to identify food insecurity stressors and enable planning. 

# Limitations
* Quality of the image is quite poor so the model can't identify crops for small fields.

<img src="images/imageQuality.png" width="60%" />

* As the model is trained for very few crops, it can't identify many of the main crops of Senegal and results in many "no classification" results.

* Data is collected directly from Google Earth Engine. It restricts collecting data over large area like country level.

# Improvements
* Use of high quality satellite images would provide better results.
* Training the model with more crop types would enable more comprehensive classification.
* Obtaining some ground truth data for Senegal would enable fine-tuning of the model to account for differences in geography, weather, agricultural practices, and so on between South Africa and Senegal. This would improve the model's ability to generalise to Senegal and provide more accurate estimates.


