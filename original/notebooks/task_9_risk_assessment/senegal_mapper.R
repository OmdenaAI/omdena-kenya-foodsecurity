#senegal mapper 01/08/21
#rm(list=ls())
#
#setwd('C:/Users/Faiz/Desktop/_Omdena/software')
library(ggplot2)
library(maps)

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
#base_senegal
remove(base_senegal_messy, base_world, base_world_messy, p, cleanup, world_map, senegal)
