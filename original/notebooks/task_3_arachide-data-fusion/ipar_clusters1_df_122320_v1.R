#clusters of 'household' , 'central_zone' of ipar dataframes 12/24/20
#rm(list=ls())
#
#
library(tidyverse)
library(tidymodels)
library(haven)
library(maps)

colnames(central_zone)
#View(central_zone)
glimpse(central_zone)
summary(central_zone)

#ok so these are my 3 main regions... central is ~13.2 to 15 lat, lets select on that range
central_zone = households %>% filter(gpslat >= 13.5, gpslat <= 15)
#down to 661 from 2071, let me plot on these on map_data
central_map <- map_data + geom_point(data=central_zone, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                    fill="red4",pch=21, size=3, alpha=I(0.7)); central_map
#this is my focus zone!!!! arachine basin - central
A03 <- table(central_zone$A03)
A03
central_map
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
#checking vulnerability from ipar survy for central_zone
#F01 - climatic risk
#F02 - other risks
#lets check category
F01a <- table(central_zone$F01a)
F01b <- table(central_zone$F01b)
F01c <- table(central_zone$F01c)
F01d <- table(central_zone$F01d)
F01e <- table(central_zone$F01e)
F01f <- table(central_zone$F01f)
F01g <- table(central_zone$F01g)
F01a;F01b;F01c;F01d;F01e;F01f;F01g

F02a <- table(central_zone$F02a)
F02b <- table(central_zone$F02b)
F02c <- table(central_zone$F02c)
F02d <- table(central_zone$F02d)
F02e <- table(central_zone$F02e)
F02f <- table(central_zone$F02f)
F02g <- table(central_zone$F02g)
F01a;F01b;F01c;F01d;F01e;F02f;F02g

#*****it looks like q's F01 and F02 are swapped (a-e, vs. a-g?)
cat("it looks like q's F01 and F02 are swapped (a-e, vs. a-g?)")

#checking F03 and F04 - access to information/forecasting
F03 <- table(central_zone$F03)
F04 <- table(central_zone$F04)
F03;F04
#cool ... lets make barplots, i think these are regions
barplot(F03, main = "Absolute frequency")
barp <- barplot(F03, main = "Absolute frequency", col = '#69b3a2', ylim = c(0, 550))
barplot(F04, main = "Absolute frequency")
barp <- barplot(F04, main = "Absolute frequency", col = '#69b3a2', ylim = c(0, 550))

#F05,F06,F07,F08 also are a-e, will come back to later.

#G0x data - UPA units production - in 'producers'
#H0x data - land capital by crop is in 'capital'
#I0x, J0x, and K0x - production habits/methods -  in 'production' (seems like same few crops listed 1-5)
#1,2,3 - rice types; 4 - millet, 5 - maize
#why not aracide??
cat("why not arachide in crop coding of I,J,K (methods)?   Need to look at H more carefully")
#----------------------------------------------------------------#
#------ moving on to the clustering in the 'capital' data , for these 7 regions------#
#H0x questions - land capital and types of land
glimpse(capital)  # remember, this is currently ALL of the regions
cat("remember this is ALL of the regions - need to sort by central zone later")
#H03 - nature of plot, H04 - type, H05 - mode of operation(?)
#H06 - further analysis required.
H03 <- table(capital$H03)
H04 <- table(capital$H04)
H05 <- table(capital$H05)
H03;H04;H05
barplot(H03, main = "land: 1-irrigated, 2-rain, 3-wet:", col = '#69b3a2')
barplot(H04, main = "prop: 1-ind, 2-fam, 3-coop: ", col = '#69b3a2')
barplot(H05, main = "mode: 1-direct, 2-fermage*, 3-metayage**:", col = '#69b3a2')
#now onto H06 - this is interesting, 29 different codes!!!
#......picking a couple for example
H06Riz_irrigue_CSC <- table(capital$H06Riz_irrigue_CSC)
H06Riz_irrigue_CSC
H06Riz_irrigue_hiv <- table(capital$H06Riz_irrigue_hiv)
H06Riz_irrigue_hiv
H06Riz_pluvial <- table(capital$H06Riz_pluvial)
H06Riz_pluvial
H06Mil <- table(capital$H06Mil)
H06Mil
H06Mais <- table(capital$H06Mais)
H06Mais
H06Arachide <- table(capital$H06Arachide)
H06Arachide
#... thats not all of them, not sure what 1 vs. 2 means?
#----------------------------------------------------------------#


#------ moving on to the clustering in the 'producers' data , for these 7 regions------#



#----------------------------------------------------------------#


#------ moving on to the clustering in the 'production' data , for these 7 regions------#
#I0x, J0x, and K0x in production
#production
#----------------------------------------------------------------#
