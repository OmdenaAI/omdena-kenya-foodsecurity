#fusion of grid of weather to the points from ipar
#12/27/20 v1
library(tidyverse)
library(tidymodels)
library(haven)
library(maps)
library(geojson)

#setwd('C:/Users/Faiz/Desktop/_Omdena/datasets/iPar Data-20201221T142443Z-001')
setwd('C:/Users/Faiz/Desktop/_Omdena/datasets/')

#load grid geojson
# skipping for now?

#load csv
weather <- read_csv("senegal_weather.csv")
colnames(weather)
#sort by central and southern
central_weather = weather %>% filter(latitude >= 13.5, latitude <= 15)
central_weather = central_weather %>% filter(longitude >= -16.8, longitude <= -14.8)
southern_weather = weather %>% filter(latitude < 13.5)
southern_weather = southern_weather %>% filter(longitude >= -16.9, longitude <= -13.6)
northern_weather = weather %>% filter(latitude >= 15)


#plot points for regional weather
length(unique(central_weather$latitude))
length(unique(central_weather$longitude))
length(unique(southern_weather$latitude))
length(unique(southern_weather$longitude))
length(unique(northern_weather$latitude))
length(unique(northern_weather$longitude))
two_region
#just want to plot the central grid and southern grid
central_grid = select(central_weather, 'latitude','longitude')
southern_grid = select(southern_weather, 'latitude','longitude')
central_grid = distinct(central_grid)
southern_grid = distinct(southern_grid)
#mapping these
central_points <- geom_point(data=central_grid, aes(x=longitude, y=latitude), colour="black", 
                             fill="black",pch=21, size=.5, alpha=I(0.7))
central_gridmap <- map_data + central_points ; central_gridmap

southern_points <- geom_point(data=southern_grid, aes(x=longitude, y=latitude), colour="black", 
                             fill="black",pch=21, size=.5, alpha=I(0.7))
southern_gridmap <- map_data + southern_points ; southern_gridmap
two_region_gridmap <- map_data + southern_points + central_points; two_region_gridmap
two_region_map <- two_region + southern_points + central_points; two_region_map

#great, for each of these points on the grid --- behzad has obtained
#over 20 years, monthly - windspd, t2m (Kelvin), tp (precip), winddir
