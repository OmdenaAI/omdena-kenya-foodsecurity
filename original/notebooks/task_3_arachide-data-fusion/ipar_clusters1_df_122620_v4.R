#clusters of 'household' , 'central_zone' of ipar dataframes 12/25/20 v3
#rm(list=ls())
#
#
library(tidyverse)
library(tidymodels)
library(haven)
library(maps)
library(DBI)
library(RSQLite)

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

#G0x data - UPA unit of production - in 'producers' (description, demographics only, small dataframe)
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


#------ clustering in the 'producers' data , for these 7 regions------#
#G03 and G04 are gender and age
G03 <- table(producers$G03)
G04 <- table(producers$G04)
G03 #2288 male, 663 female
barplot(G03, main = "gnder: 1-male, 2-femle:", col = '#69b3a2')
G04 # as expected all over the place, lets group in 10s?
# ages = producers %>% group_by(G04) %>% summarize(n()) #this came back with 79 ages (12-99!)
# glimpse(ages)
# age18 = split(ages, ages$G04 >= 1 & ages$G04 <= 17)
# age30 = split(ages, ages$G04 >= 18 & ages$G04 <= 30)
# age50 = split(ages, ages$G04 >= 31 & ages$G04 <= 50)
# age65 = split(ages, ages$G04 >= 51 & ages$G04 <= 65)
# age99 = split(ages, ages$G04 >= 66 & ages$G04 <= 99)
hist(producers$G04, breaks=4)
ggplot(producers, aes(x=G04)) + 
  geom_histogram(aes(y=..density..), colour="black", fill="gray", binwidth = 10)+
  geom_density(alpha=.2, fill="#69b3a2") + 
  geom_vline(aes(xintercept=mean(G04)),color="blue", linetype="dashed", size=1)
gender <- as.character(producers$G03) 

producers3 <- cbind(producers,gender)

ggplot(producers3, aes(x = G04)) +
  geom_histogram(aes(color = gender, fill = gender), 
                 position = "identity", bins = 10, alpha = 0.4) +
  scale_color_manual(values = c("darkolivegreen4", "firebrick3")) +
  scale_fill_manual(values = c("darkolivegreen4", "firebrick3"))

#G05 is networking
G05 <- table(producers$G05)
G05  #381 yes network group, 2570 no network group
barplot(G03, main = "network group: 1-no, 2-yes:", col = '#69b3a2')
#G06 is the name of the group if so, lets see how many there are?
G06 <- table(producers$G06)
# G06
G06 <- sort(G06) # 2570 of 2951 are part of 'A 23 seddo abbas'
cat("2570 of 2951 are part of 'A 23 seddo abbas'")
#checking G01 for completeness
G01 <- table(producers$prod_id)
G01  #values 1-11 , need coding for this... #1 is not arachide, the coding is tied to id_menage!!!
#need to sort by ID_menage
cat ("where is this? - 1-arachide, 2-arachide biomass, 3-millet, 4-sorghum, 5-maize, 6-rice, 7-onion, 8-potato, 9-cassava, 10-cowpea, 11-tomato")
#make a nice table of this!!!!! after mashing with ID_menage!!!
# barplot(notG01, main = "(? NO!!!): 1-arachide, 2-arachide biomass, 3-millet, 4-sorghum, 
#         5-maize, 6-rice, 7-onion, 8-potato, 9-cassava, 10-cowpea, 11-tomato)", col = '#69b3a2')
#View(producers)
#----------------------------------------------------------------#
#------ clustering in the 'production' data , for these 7 regions------#
#I0x, J0x, and K0x in production
#production - this has 381 columsn, need to analyzer, let me 
glimpse(production)
#so far these ar for all the regions north, central , south
#perhaps i should first sort by only my 'central_zone' households,
#or better yet, create 3 groupings - central, southern, northern (distinct rural)
#then do an anova for each
#ok so these are my 3 main regions... central is ~13.2 to 15 lat, lets select on that range
# remember "central_zone = households %>% filter(gpslat >= 13.5, gpslat <= 15)"
# central_map
#this is my focus zone!!!! arachine basin - central
A03central <- table(central_zone$A03)
A03central
northern_zone = households %>% filter(gpslat >= 15)
southern_zone = households %>% filter(gpslat < 13.5)
northern_map <- map_data + geom_point(data=northern_zone, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                     fill="dodgerblue4",pch=21, size=3, alpha=I(0.7)); # northern_map
southern_map <- map_data + geom_point(data=southern_zone, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                                         fill="darkorange",pch=21, size=3, alpha=I(0.7)); # southern_map
northern <- geom_point(data=northern_zone, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
           fill="dodgerblue4",pch=21, size=3, alpha=I(0.7))
southern <- geom_point(data=southern_zone, aes(x=gpslon, y=gpslat), colour="Deep Pink", 
                      fill="darkorange",pch=21, size=3, alpha=I(0.7))
three_region <- central_map + northern + southern; three_region
#other regions
A03central
A03northern <- table(northern_zone$A03)
A03northern
A03southern <- table(southern_zone$A03)
A03southern

#now need to link these to my 'production' file ... #3304 rows. vs. 2071 n households
#try to link/join my 'id_menage'..... (more to come l8er!!!)
#rowSums(central_zone)
nrow(central_zone)
nrow(northern_zone)
nrow(southern_zone)
#lat search
df1 <- central_zone; df2 <- northern_zone; df3 <- southern_zone 
df1 <- df1[complete.cases(df1$gpslat),]; df2 <- df2[complete.cases(df2$gpslat),]; df3 <- df3[complete.cases(df3$gpslat),] 
range(df1$gpslat) ; range(df2$gpslat); range(df3$gpslat)
#longit search
df1 <- df1[complete.cases(df1$gpslon),]; df2 <- df2[complete.cases(df2$gpslon),]; df3 <- df3[complete.cases(df3$gpslon),] 
range(df1$gpslon) ; range(df2$gpslon); range(df3$gpslon)



#----------------------------------------------------------------#
