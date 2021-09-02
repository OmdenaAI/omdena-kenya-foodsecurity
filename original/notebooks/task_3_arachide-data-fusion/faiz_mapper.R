library(maps)
library(tidyverse)

#------#my choice mapping script--------------#

#simple map
world_map <- map_data("world")

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

#------adding mexico-------------#
mexico <- subset(world_map, world_map$region=="Mexico")
#add map to base plot (Mexico)
base_loc_messy <- p + geom_polygon(data=mexico, aes(x=long, y=lat, group=group), 
                                       colour="light green", fill="light green")
#base_mex_messy
base_loc <- base_loc_messy + cleanup
base_mexico <- base_loc
base_mexico

#------#fin--------------#


#now lets try those 2071 points!!!
#add my data with households
map_data <- 
  base_mexico +
  geom_point(data=households, 
             aes(x=gpslon, y=gpslat), colour="Deep Pink", 
             fill="Pink",pch=21, size=5, alpha=I(0.7))
map_data