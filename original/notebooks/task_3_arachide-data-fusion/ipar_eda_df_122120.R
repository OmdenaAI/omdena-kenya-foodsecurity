#ead ipar data  of dataframes 12/21/20
#rm(list=ls())
#
#
library(tidyverse)
library(tidymodels)
library(haven)
library(maps)

colnames(households)
colnames(production)
colnames(producers)
colnames(capital)
#View(households)
#View(production)
#View(producers)
#View(capital)

glimpse(households)
summary(households)
as.data.frame(households)
#from viewing in excel - 
#households contains some lat and long data (can map this)
#capital - contains some crop specific info and coding/indexing? (can try to cluster)
#lets try mapping household - there are 2071 data points

#simple map
world_map <- map_data("world")
senegal <- subset(world_map, world_map$region=="Senegal")

#------#my choice mapping script--------------#
#basemap
#Creat a base plot with gpplot2
p <- ggplot() + coord_fixed() +
  xlab("") + ylab("")

#Add map to base plot (world)
base_world_messy <- p + geom_polygon(data=world_map, aes(x=long, y=lat, group=group), 
                                     colour="light green", fill="light green")

#map_cleaner
cleanup <- 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), 
        panel.background = element_rect(fill = 'white', colour = 'white'), 
        axis.line = element_line(colour = "white"), legend.position="none",
        axis.ticks=element_blank(), axis.text.x=element_blank(),
        axis.text.y=element_blank())
base_world <- base_world_messy + cleanup
#base_world
#------adding senegal--------------#
#add map to base plot (senegal)
base_senegal_messy <- p + geom_polygon(data=senegal, aes(x=long, y=lat, group=group), 
                                   colour="light green", fill="light green")
#base_mex_messy
base_senegal <- base_senegal_messy + cleanup
base_senegal

#now lets try those 2071 points!!!
#add my data with households
map_data <- 
  base_senegal +
  geom_point(data=households, 
             aes(x=gpslon, y=gpslat), colour="Deep Pink", 
             fill="Pink",pch=21, size=5, alpha=I(0.7))
map_data

#need to change the last few chr to numeric
households$gpslat <- as.numeric(as.character(households$gpslat))
households$gpslon <- as.numeric(as.character(households$gpslon))
glimpse(households) #ok, lets try again

map_data <- 
  base_senegal +
  geom_point(data=households, 
             aes(x=gpslon, y=gpslat), colour="Deep Pink", 
             fill="Pink",pch=21, size=2, alpha=I(0.7))
map_data
