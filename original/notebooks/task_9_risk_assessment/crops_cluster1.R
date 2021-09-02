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

setwd('F:/_Moons/om/datasets1/')

#load csv
crops <- read_csv("senegal_crops3.csv")
weather <- read_csv("senegal_weather.csv")
biomass <- read_csv("biomass1.csv")

households <- read_csv("1_NM_SN__baseline_Menages.csv")
capital <- read_csv("3_NM_SN_baseline_Capital_Foncier.csv")
production <- read_csv("4_NM_SN_baseline_Production.csv")
producers <- read_csv("2_NM_SN_baseline_Producteurs.csv")

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

#these are by city and by year, so lets try cluster with just columns 6-29
blind <- two_region_crops %>% select(6:29)
blind <- na.omit(blind)
#need to change the last few chr to numeric
blind$yieldGroundnut <- as.numeric(as.character(blind$yieldGroundnut))
#normalize/scale
blind <- scale(blind)
set.seed(1)
#try with gapstat
fviz_nbclust(blind, kmeans, method = "gap_stat")
#try another method - wss
fviz_nbclust(blind, kmeans, method = "wss")
#try another - silhouette
fviz_nbclust(blind, kmeans, method = "silhouette")
#the optimal number could be 2, 4, or 6, or 7 from these results, lets visualize
# Visualize the classification
km.res2 <- kmeans(blind, 2, nstart = 25)
fviz_cluster(km.res2, data = blind)
km.res4 <- kmeans(blind, 4, nstart = 25)
fviz_cluster(km.res4, data = blind)
km.res6 <- kmeans(blind, 6, nstart = 25)
fviz_cluster(km.res6, data = blind)
#lets try 3 and 7 also
km.res3 <- kmeans(blind, 3, nstart = 25)
fviz_cluster(km.res3, data = blind)
km.res7 <- kmeans(blind, 7, nstart = 25)
fviz_cluster(km.res7, data = blind)
#go back and associate clusters by year, location (note!!! this is only southern, central)

