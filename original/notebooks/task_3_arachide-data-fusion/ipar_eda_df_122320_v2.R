#eda ipar data  of dataframes 12/23/20
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
             aes(x=gpslon, y=gpslat), colour="azure", 
             fill="bisque2",pch=21, size=2, alpha=I(0.7))
map_data

#ok that worked, now will focus on centreal region... i think this is arachide basin
#will sort through this area, perhaps by region or city (column A03)

#lets check category
A03 <- table(households$A03)
A03
#cool ... lets make barplots, i think these are regions
barplot(A03, main = "Absolute frequency")
barp <- barplot(A03, main = "Absolute frequency", col = rainbow(20), ylim = c(0, 250))
text(barp, A03 + 1, labels = A03)
#i want the text along the x to show all cities (ok i rotated to horizontal)
barplot(A03, col="#69b3a2", horiz=T , las=1)
#let me sort it in order of count
A03 <- sort(A03)
barplot(A03, col="#69b3a2", horiz=T , las=1)
as.data.frame(A03)
#20 total regions - as per ipar, these must be rural areas?
#top 5 are:  NIORO, BIGNONA, PODOR, MATAM, VELINGARA
#i want to know where these top 5 are on the map (from excel)
#i also recognize - KOLAK, and KAFFRINE 

#there is high consolidation at these points... need to find out what the mean
#clearly there are diversified clustering... but these points show up by far the most... 
#i want to focus on the arachide basine... what is that one point
#=---- actually backtracking, i think i did the previous consolidation wrong as i assumed all those are at the same lat/long
#but they may not be, let me redo via grouping/selectingin R---- #

#each of these 20 regions - by rank
nioro = households %>% filter(A03 == 'NIORO')
bignona = households %>% filter(A03 == 'BIGNONA')
podor = households %>% filter(A03 == 'PODOR')
matam = households %>% filter(A03 == 'MATAM')
velingara = households %>% filter(A03 == 'VELINGARA')
kolda = households %>% filter(A03 == 'KOLDA')
dagana = households %>% filter(A03 == 'DAGANA')
sedhiou = households %>% filter(A03 == 'SEDHIOU')
kaolack = households %>% filter(A03 == 'KAOLACK')
goudomp = households %>% filter(A03 == 'GOUDOMP')
yorofoulah = households %>% filter(A03 == 'MEDINA YORO FOULAH')
foundiougne = households %>% filter(A03 == 'FOUNDIOUGNE')
birkelane = households %>% filter(A03 == 'BIRKELANE')
bounkiling = households %>% filter(A03 == 'BOUNKILING')
kanel = households %>% filter(A03 == 'KANEL')
ziguinchor = households %>% filter(A03 == 'ZIGUINCHOR')
koungheul = households %>% filter(A03 == 'KOUNGHEUL')
kaffrine = households %>% filter(A03 == 'KAFFRINE')
malemhoddar = households %>% filter(A03 == 'MALEM HODDAR')
oussouye = households %>% filter(A03 == 'OUSSOUYE')

#ok great, now lets analyze each of the 20 regions, in order (first top 5 here)
map_data3 <- map_data + geom_point(data=nioro, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
             fill="Orange",pch=21, size=3, alpha=I(0.7)); map_data3
map_data4 <- map_data3 + geom_point(data=bignona, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                   fill="Blue",pch=21, size=3, alpha=I(0.7)); map_data4
map_data5 <- map_data4 + geom_point(data=podor, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                   fill="Deep Pink",pch=21, size=3, alpha=I(0.7)); map_data5
map_data6 <- map_data5 + geom_point(data=matam, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                   fill="Yellow",pch=21, size=3, alpha=I(0.7)); map_data6
map_data7 <- map_data6 + geom_point(data=velingara, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                   fill="Sienna",pch=21, size=3, alpha=I(0.7)); map_data7
#map_data7 is my top 5
#adding my 2 recognized regions
map_data8 <- map_data7 + geom_point(data=kaolack, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                    fill="darkgreen",pch=21, size=3, alpha=I(0.7)); map_data8
map_data9 <- map_data8 + geom_point(data=kaffrine, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                    fill="aquamarine3",pch=21, size=3, alpha=I(0.7)); map_data9

#lets get rankers #6-11
map_data10 <- map_data9 + geom_point(data=kolda, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                    fill="black",pch=21, size=3, alpha=I(0.7)); map_data10
map_data10 <- map_data10 + geom_point(data=dagana, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                    fill="black",pch=21, size=3, alpha=I(0.7)); map_data10
map_data10 <- map_data10 + geom_point(data=sedhiou, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                    fill="black",pch=21, size=3, alpha=I(0.7)); map_data10
map_data10 <- map_data10 + geom_point(data=goudomp, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                    fill="black",pch=21, size=3, alpha=I(0.7)); map_data10
map_data10 <- map_data10 + geom_point(data=yorofoulah, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                    fill="black",pch=21, size=3, alpha=I(0.7)); map_data10

# #ok, so this is headed by north, central, and southern
# #looks like highest 'density' is central - i want to focus on this region, and inlcude the others
# #let me filter 'households' by lat value range

# df2 <- nioro
# df2 <- df2[complete.cases(df2$gpslat),]
# range(df2$gpslat)
# #and now for the other ones in a quick list
# df2 <- bignona ; df2 <- df2[complete.cases(df2$gpslat),] ; range(df2$gpslat)
# df2 <- podor ; df2 <- df2[complete.cases(df2$gpslat),] ; range(df2$gpslat)

#ok so these are my 3 main regions... central is ~13.2 to 15 lat, lets select on that range
central_zone = households %>% filter(gpslat >= 13.5, gpslat <= 15)
#down to 661 from 2071, let me plot on these on map_data
central_map <- map_data + geom_point(data=central_zone, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                    fill="red4",pch=21, size=3, alpha=I(0.7)); central_map
#this is my focus zone!!!! arachine basin - central
A03 <- table(central_zone$A03)
A03
#so these are my 7 focus statistical regions as per ipar - highest density -
#maybe highest vuca 
#central rural senegal !!!
# nioro 
# kaolack 
# foundiougne 
# birkelane 
# koungheul 
# kaffrine 
# malemhoddar
#these form my 'central_zone' 7 regions dataframe moving forward.
#need ipar, climate, crop, socio-economic, soil, hazard, etc. data for these as per datastage


#----------------------------------------------------------------#

#------ moving on to the clustering in the 'capital' data , for these 7 regions------#

