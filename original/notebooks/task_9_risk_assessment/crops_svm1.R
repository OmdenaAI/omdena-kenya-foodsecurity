#read crops file, pre-stats, and unsupervised cluster attempt
#with crops, weather, biomass, households, capital, production, producers, other tbd
#rm(list=ls())
library(tidyverse)
library(tidymodels)
library(maps)
library(imager)
library(gridExtra)
library(cluster)
library(factoextra)
library(FactoMineR)

library(e1071)
library(sp)
library(sf)

setwd('F:/_Moons/om/datasets1/')
#setwd('C:/')

#load csv
crops <- read_csv("senegal_crops3.csv")
weather <- read_csv("senegal_weather.csv")
biomass <- read_csv("biomass1.csv")

households <- read_csv("1_NM_SN__baseline_Menages.csv")
capital <- read_csv("3_NM_SN_baseline_Capital_Foncier.csv")
production <- read_csv("4_NM_SN_baseline_Production.csv")
producers <- read_csv("2_NM_SN_baseline_Producteurs.csv")

prices <- read_csv("wfp_food_prices_senegal.csv")
unique(prices$mktname)
#senegal region map
image <- load.image("senegal_regions.jpg")
plot(image)

colnames(weather)
colnames(crops)
colnames(biomass)
base_senegal

#need to change the last few chr to numeric
households$gpslat <- as.numeric(as.character(households$gpslat))
households$gpslon <- as.numeric(as.character(households$gpslon))
#glimpse(households) #ok, lets try again

map_data <- 
  base_senegal +
  geom_point(data=households, 
             aes(x=gpslon, y=gpslat), colour="azure", 
             fill="bisque2",pch=21, size=2, alpha=I(0.7))
map_data

#CROPS analys - add to map 
crop_data <- 
  map_data +
  geom_point(data=crops, 
             aes(x=lon, y=lat), colour="azure", 
             fill="red",pch=21, size=2, alpha=I(0.7))
crop_data

#add yearly weather grid
#sort by central and southern
central_weather = weather %>% filter(latitude >= 13.5, latitude <= 15)
central_weather = central_weather %>% filter(longitude >= -16.8, longitude <= -14.8)
southern_weather = weather %>% filter(latitude < 13.5)
southern_weather = southern_weather %>% filter(longitude >= -16.9, longitude <= -13.6)
northern_weather = weather %>% filter(latitude >= 15)
#setting regional grid
grid = select(weather, 'latitude','longitude')
central_grid = select(central_weather, 'latitude','longitude')
southern_grid = select(southern_weather, 'latitude','longitude')
grid = distinct(grid)
central_grid = distinct(central_grid)
southern_grid = distinct(southern_grid)
#write.csv(grid, ".\\grid.csv")
#write.csv(central_grid, ".\\central_grid.csv")
#write.csv(southern_grid, ".\\southern_grid.csv")

#overlap mapping these
all_points <- geom_point(data=grid, aes(x=longitude, y=latitude), colour="black", 
                      fill="black",pch=21, size=.5, alpha=I(0.7))
all_gridmap <- crop_data + all_points ; all_gridmap
central_points <- geom_point(data=central_grid, aes(x=longitude, y=latitude), colour="black", 
                             fill="black",pch=21, size=.5, alpha=I(0.7))
central_gridmap <- crop_data + central_points ; central_gridmap

southern_points <- geom_point(data=southern_grid, aes(x=longitude, y=latitude), colour="black", 
                              fill="black",pch=21, size=.5, alpha=I(0.7))
southern_gridmap <- crop_data + southern_points ; southern_gridmap
two_region_gridmap <- crop_data + southern_points + central_points; two_region_gridmap


#group crops in same way
central_crops = crops %>% filter(lat >= 13.5, lat <= 15)
central_crops = central_crops %>% filter(lon >= -16.8, lon <= -14.8)
southern_crops = crops %>% filter(lat < 13.5)
southern_crops = southern_crops %>% filter(lon >= -16.9, lon <= -13.6)
northern_crops = crops %>% filter(lat >= 15)
#merging
two_region_crops = rbind(central_crops, southern_crops)

#check N/As and duplicates
glimpse(two_region_crops)
sum(is.na(two_region_crops))
colSums(is.na(two_region_crops))
cities = unique(two_region_crops$level2)
cities #central and southern cities


#(note!!! this is only southern, central), let try to label with leve1 region

#all variables, and scale/normalize (based on PCA, only choosing a few)
#6,9,10,11,12,13 - ndvimean, max, rainmin, mean, meax
blind1 <- na.omit(two_region_crops)
level1 <- blind1$level1
blind2 <- blind1 %>% select(6,9:13)
blind2 <- scale(blind2)
blind3 <- cbind.data.frame(blind2, level1)
blind3$level1 = as.factor(blind3$level1)
set.seed(1)

#svm to level1 
train = sample(1:nrow(blind3), nrow(blind3)/2)
#from top 6 from PCA
svm.fit = svm(level1 ~ tempday + ndvimax+ndvimean + rainmax+rainmin+rainmean, data= blind3[train, ], kernel = "radial", gamma =1, cost =1)
#print out model results
summary(svm.fit)
#view(blind3[train, ])
plot(svm.fit, blind3[train, ], tempday ~ ndvimean, slice=list(ndvimax=0, rainmin=0))
#**** heat map here ***** 
#forecast the am using test dataset
pred = predict(svm.fit, newdata = blind3[-train, ])
#get the true observation of am of  the test dataset
true= blind3[-train, "level1"]
#compute the test error by construct confusion matrix
table(true, pred)

#lets redo with cross validation to improve
tune.out = tune(svm, level1 ~ tempday + ndvimax+ndvimean + rainmax+rainmin+rainmean, data= blind3[train, ], kernel = "radial", ranges = list(cost = c(1,10, 50, 100), gamma= c(1, 3, 5, 10)))
summary(tune.out)

pred1 = predict(tune.out$best.model, newdata = blind3[-train, ])
true1= blind3[-train, "level1"]
table(true1, pred1)
caret::confusionMatrix(pred1, true1)

#let me try without scaling