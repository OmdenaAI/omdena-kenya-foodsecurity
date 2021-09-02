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
crops$yieldGroundnut <- as.numeric(as.character(crops$yieldGroundnut))
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
#need to change the last few chr to numeric
two_region_crops$yieldGroundnut <- as.numeric(as.character(two_region_crops$yieldGroundnut))
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
fviz_cluster(km.res2, data = blind) #visualize
km.res4 <- kmeans(blind, 4, nstart = 25)
fviz_cluster(km.res4, data = blind) #visualize
km.res6 <- kmeans(blind, 6, nstart = 25)
fviz_cluster(km.res6, data = blind) #visualize
#lets try 3 and 7 also, and 5
km.res3 <- kmeans(blind, 3, nstart = 25)
fviz_cluster(km.res3, data = blind)
km.res7 <- kmeans(blind, 7, nstart = 25)
fviz_cluster(km.res7, data = blind)
km.res5 <- kmeans(blind, 5, nstart = 25)
fviz_cluster(km.res5, data = blind)
#optimal looks like 3, or 4 or 5 - what are these, need to ...

res.pca <- PCA(blind,  graph = FALSE)
fviz_screeplot(res.pca, addlabels = TRUE, ylim = c(0, 50))
# Extract the results for variables
var <- get_pca_var(res.pca)
var
# Coordinates of variables
head(var$coord)
(var$coord)
# Contribution of variables
head(var$contrib)
(var$contrib)

#graph of contributions
fviz_pca_var(res.pca, col.var="contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE # Avoid text overlapping
)
#... need to go back and associate clusters by year, location 
#(note!!! this is only southern, central), let try to label with leve1 region
blind1 <- na.omit(two_region_crops)
blind2 <- blind1 %>% select(6:29)
#need to change the last few chr to numeric
blind2$yieldGroundnut <- as.numeric(as.character(blind2$yieldGroundnut))
#rownames(blind2) <- with(blind1, paste(year, level1, level2, sep = ":"))
rownames(blind2) <- with(blind1, paste(year, rownames(blind1), sep = ":"))
#blind1 <- na.omit(blind1)
blind2 <- scale(blind2)
set.seed(1)
#cluster
fviz_nbclust(blind2, kmeans, method = "gap_stat")
km2.res2 <- kmeans(blind2, 2, nstart = 25)
fviz_cluster(km2.res2, data = blind2) #visualize
#now with level2
rownames(blind2) <- with(blind1, paste(level1, rownames(blind1), sep = ":"))
set.seed(1)
#cluster
fviz_nbclust(blind2, kmeans, method = "gap_stat")
km2.res2 <- kmeans(blind2, 2, nstart = 25)
fviz_cluster(km2.res3, data = blind2) #visualize
#lets try 3 with the region labels
km2.res3 <- kmeans(blind2, 3, nstart = 25)
fviz_cluster(km2.res3, data = blind2) #visualize
#and 4
km2.res4 <- kmeans(blind2, 4, nstart = 25)
fviz_cluster(km2.res4, data = blind2) #visualize

#remove yield, population and re-run
blind3 <- blind1 %>% select(6:23)
rownames(blind3) <- with(blind1, paste(level1, rownames(blind1), sep = ":"))
blind3 <- scale(blind3)
set.seed(1)
fviz_nbclust(blind3, kmeans, method = "gap_stat")
km3.res2 <- kmeans(blind3, 2, nstart = 25)
fviz_cluster(km3.res2, data = blind3) #visualize
#lets try 3 with the region labels
km3.res3 <- kmeans(blind3, 3, nstart = 25)
fviz_cluster(km2.res3, data = blind2) #visualize
#and 4
km3.res4 <- kmeans(blind3, 4, nstart = 25)
fviz_cluster(km2.res4, data = blind2) #visualize
##-------------------------------------------------------#
##-------------------------------------------------------#
#try cluster will full regions
blind1 <- na.omit(crops)
blind2 <- blind1 %>% select(6:29)
rownames(blind2) <- with(blind1, paste(level1, rownames(blind1), sep = ":"))
blind2 <- scale(blind2)
set.seed(1)
#cluster
fviz_nbclust(blind2, kmeans, method = "gap_stat")
fviz_nbclust(blind2, kmeans, method = "wss")
fviz_nbclust(blind2, kmeans, method = "silhouette")
#7 or 8 is optimal here - only by adding northern region
kmfull2 <- kmeans(blind2, 2, nstart = 25)
fviz_cluster(kmfull2, data = blind2) #visualize
#lets try 7 with the region labels
kmfull7 <- kmeans(blind2, 7, nstart = 25)
fviz_cluster(kmfull7, data = blind2) #visualize
kmfull8 <- kmeans(blind2, 8, nstart = 25)
fviz_cluster(kmfull8, data = blind2) #visualize
kmfull6 <- kmeans(blind2, 6, nstart = 25)
fviz_cluster(kmfull6, data = blind2) #visualize
#PCA on 7 cluster version
res.pca <- PCA(blind2,  graph = FALSE)
fviz_screeplot(res.pca, addlabels = TRUE, ylim = c(0, 50))
var <- get_pca_var(res.pca)
var
head(var$coord)
(var$coord)
head(var$contrib)
(var$contrib)
#graph of contributions
fviz_pca_var(res.pca, col.var="contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE # Avoid text overlapping
)
#add'l vizs
plot(res.pca, choix = "var") #simple
fviz_pca_var(res.pca) #simple
fviz_pca_var(res.pca, col.var="contrib")+  #alternate color scheme
  scale_color_gradient2(low="blue", mid="white", 
                        high="red", midpoint=55)+theme_bw()

head(res.pca$ind$coord)
head(res.pca$ind$cos2)
head(res.pca$ind$contrib)
plot(res.pca, choix = "ind")
fviz_pca_ind(res.pca)
fviz_pca_ind(res.pca, geom="text")

fviz_pca_ind(res.pca, col.ind="cos2") +
  scale_color_gradient2(low="blue", mid="white", 
                        high="red", midpoint=0.50)

fviz_pca_ind(res.pca,  col.ind="cos2") +
  scale_color_gradient2(low="#00AFBB", mid="#E7B800", 
                        high="#FC4E07", midpoint=0.50)+
  theme_minimal()


fviz_pca_biplot(res.pca,  geom = "text")

#*******let me do this better now for color coded labels on level1 (as.factor)
#blind1 <- na.omit(crops) #********
blind1 <- na.omit(two_region_crops)
level1 <- blind1$level1
blind2 <- blind1 %>% select(6:29)
blind2 <- scale(blind2)
blind3 <- cbind.data.frame(blind2, level1)
blind3$level1 = as.factor(blind3$level1)
set.seed(1)

#pca
res.pca <- PCA(blind3[,-25],  graph = FALSE)
#add'l visuals
fviz_pca_ind(res.pca, label="none") #nice simple scatter plot
fviz_pca_ind(res.pca, col.ind = "blue", pointsize =4)+
  theme_minimal()
fviz_pca_ind(res.pca, col.ind="cos2")
fviz_pca_ind(res.pca, col.ind="cos2", geom ="point")
fviz_pca_ind(res.pca, col.ind="cos2", geom = "point") +
  scale_color_gradient2(low="white", mid="blue",
                        high="red", midpoint=0.6)+ theme_minimal()

fviz_pca_ind(res.pca, label="none", habillage=blind3$level1)

# Add ellipses
p <- fviz_pca_ind(res.pca, label="none", habillage=blind3$level1,
                  addEllipses=TRUE, ellipse.level=0.95)
print(p)
#p + scale_color_brewer(palette="Dark2") +
#  theme_minimal()

#cluster
fviz_nbclust(blind3[-25], kmeans, method = "gap_stat")
fviz_nbclust(blind3[-25], kmeans, method = "wss")
fviz_nbclust(blind3[-25], kmeans, method = "silhouette")

km2 <- kmeans(blind3[-25], 2, nstart = 25)
fviz_cluster(km2, data = blind3[-25], geom="text")
fviz_cluster(km2, data = blind3[-25], geom="point")
fviz_cluster(km2, data = blind3[-25], habillage=blind3$level1)

#PAM
pam.res <- pam(blind3[,-25], 2)
fviz_cluster(pam.res, geom = "point", ellipse.type = "norm")

#Hierarchical
hc.cut <- hcut(blind3[,-25], k = 2, hc_method = "complete")
# Visualize dendrogram
fviz_dend(hc.cut, show_labels = FALSE, rect = TRUE)
# Visualize cluster
fviz_cluster(hc.cut, ellipse.type = "convex")
###----------------------------------------------------###