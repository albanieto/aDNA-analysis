# Data and format pre-processing
## Data needed
Two files are used to build the main dataframes:

**1. Roh data**: Data obtanied processing the plink \textit{"-homozyg"} output (multiple files) via getROHData.py script available in this repository. It consists of a .csv (it can be .tsv or any other type of delimitation) in which each of the rows corresponds to a detected ROH. The columns are as follows:
- *ID*: The sample identification or name where the ROH has been found. There will be as many rows with the same ID as ROH has been detected in this sample. (ex: I0426)
- *KB*: The ROH size. The plink output is given in KB. However, it may be more convenient convert it to Mb via R. All the plots have been created doing the conversion at the moment of plotting (column in KB). (ex: 798.381)
- *CHR*: Chromosome where the ROH has been detected. (ex: 1)
- *INITIAL*: Position  (b) where the ROH starts. (ex: 10177)
- *FINAL*: Position (b) where the ROH ends.  (ex: 808557)

**2. Metadata**: This file includes all the relevant information per individual/sample. Content will depend on  the study objectives. All theese data usually can be found at the suplementary materials from publicly available data papers. Here is an example: 
- *ID*: The sample identification or name. There will be as only a row per ID. (ex: I0426)
- *Age*: Average dating for every sample. Only a single number (without BCE or ACE). (ex: 2310)
- *Location*: This is important as the plots are coloured by this. (ex: Paris Street, Cerdanyola del Valles, Barcelona)
- *nSNP*: It is the number of SNP that where captured using the 1240k David Reich's panel. However any other parameter that can be used as a quality control (such as BAM coverage, size of .vcf, or a simple TRUE/FALSE settled down by oneself corredponding to a manual filter will work)  (ex: 374793)
Roh data is named in this process as *alltram* and Metadata is named after the researcher of the article from which the public samples were obtained for the Final Year BSc project, *Olalde*. 

Other examples of metadata are Longitude, Latitude, type of bone...

*Olalde I, Brace S, Allentoft ME, Armit I, Kristiansen K, Booth T, et al. The Beaker phenomenon and the genomic transformation of northwest Europe. Nature. 2018*

## Data quality filtering
This is the point when a minimum quality threshold is set. This step can be ignored if you are sure your data is good enough. However, this is highly recommended if the data has been through an imputation process. In this project, two datasets (filtered and non-filtered) are conservated to compare the results. 
The threshold can be set from quantiles or a previously established parameter (such as the x% of the panel mapped). 
```r
th<-unname(quantile(Olalde$nSNP)[3])
th<-142000
OlaldeFILTER<-Olalde[Olalde$nSNP >= th,] 
```
## Merging
Now the two datasets (Metadata and Roh data) are merged. At this step, ROHs from Roh data are classified depending on their size: *>1Mb, 1-2Mb, 2-4Mb, 4-8Mb, 8-16Mb, >16Mb*. This sorting has been done following Kirin et. al. (2010) guidelines. 

*Kirin M, McQuillan R, Franklin CS, Campbell H, McKeigue PM, Wilson JF. Genomic Runs of Homozygosity Record Population History and Consanguinity. Kayser M, editor. PLoS One [Internet]. 2010 Nov 15 [cited 2021 Apr 29];5(11):e13996. Available from: https://dx.plos.org/10.1371/journal.pone.0013996*

```r
alltram=merge(x = rohdata, y = Olalde, by = c("ID", "ID")) #merging  to get all metadata information in every ROH
alltram$class<-(ifelse(alltram$KB<1000,"<1Mb",
                       ifelse(alltram$KB<2000,"1-2Mb",
                              ifelse(alltram$KB<4000,"2-4Mb",
                                     ifelse(alltram$KB<8000,"4-8Mb",
                                            ifelse(alltram$KB<16000,"8-16Mb",">16Mb"))))))  #sorting every ROH by size
library(dplyr)
alltramFilter=semi_join(x=alltram, OlaldeFILTER, "ID") #Just ROH that passed the filter
OlaldeFILTER=semi_join(OlaldeFILTER, alltramFilter, "ID")  #The ones that passed the filter
idList<-c(Olalde$ID) #list of non filtered
idListF<-c(OlaldeFILTER$ID) #list applying the threshold

#We create a column for every type of ROH defined
Olalde$"SROH"<-0 #SROH in general and for every type of ROH per individual
Olalde$"s<1Mb"<-0
Olalde$"s1-2Mb"<-0
Olalde$"s2-4Mb"<-0
Olalde$"s4-8Mb"<-0
Olalde$"s8-16Mb"<-0
Olalde$"s>16Mb"<-0


Olalde$"NROH"<-0 #NROH in general and for every type of ROH per individual
Olalde$"n<1Mb"<-0
Olalde$"n1-2Mb"<-0
Olalde$"n2-4Mb"<-0
Olalde$"n4-8Mb"<-0
Olalde$"n8-16Mb"<-0
Olalde$"n>16Mb"<-0
#Bucle to get SROH and NROH of all types of ROH per individual
for(j in 1:length(idList)) {
  thisID<-idList[j]
  IDrohs<-alltram[alltram$ID == idList[j],]
  toCount<-c(IDrohs$ID)
  totalL<-sum(IDrohs$"KB")
  Olalde[j,"SROH"]<-totalL
  Olalde[j,"NROH"]<-length(toCount)
  Olalde[j,"Ratio"]<-totalL/length(toCount)
  #Filter category
  less1Mb<-IDrohs[IDrohs$class == "<1Mb",]
  de1a2Mb<-IDrohs[IDrohs$class == "1-2Mb",]
  de2a4Mb<-IDrohs[IDrohs$class == "2-4Mb",]
  de4a8Mb<-IDrohs[IDrohs$class == "4-8Mb",]
  de8a16Mb<-IDrohs[IDrohs$class == "8-16Mb",]
  more16Mb<-IDrohs[IDrohs$class == ">16Mb",]
  #Size of Roh Mb
  Olalde[j,"s<1Mb"]<-(sum(less1Mb$"KB"))
  Olalde[j,"s1-2Mb"]<-(sum(de1a2Mb$"KB"))
  Olalde[j,"s2-4Mb"]<-(sum(de2a4Mb$"KB"))
  Olalde[j,"s4-8Mb"]<-(sum(de4a8Mb$"KB"))
  Olalde[j,"s8-16Mb"]<-(sum(de8a16Mb$"KB"))
  Olalde[j,"s>16Mb"]<-(sum(more16Mb$"KB"))
  #number of Roh for each type
  Olalde[j,"n<1Mb"]<-nrow(less1Mb)
  Olalde[j,"n1-2Mb"]<-nrow(de1a2Mb)
  Olalde[j,"n2-4Mb"]<-nrow(de2a4Mb)
  Olalde[j,"n4-8Mb"]<-nrow(de4a8Mb)
  Olalde[j,"n8-16Mb"]<-nrow(de8a16Mb)
  Olalde[j,"n>16Mb"]<-nrow(more16Mb)
}
Olalde$LogLatitude<-log10(Olalde$Latitude) #Latitude is too different to plot it

```
# Ploting time!
Most plots are build via ggplot2.
```r
library(ggplot2)
```
https://ggplot2.tidyverse.org/

## Plotting medium values per region
### Getting medium values per region
```r
library(dplyr)
Olalde<-Olalde[order(Olalde$Latitude),] #We order by latitude by personal preference
places<-distinct(as_data_frame(Olalde$Location))
names(places)<-c("Location")
lugares<-c(places$Location)
lugares<-as.array(lugares)
typeROH<-c("<1Mb","1-2Mb","2-4Mb","4-8Mb","8-16Mb",">16Mb")
names(places)<-c("Location")
places$"meanSROH"<-0
places$"meanNROH"<-0
places$"maxNROH"<-0
places$"maxSROH"<-0
places$"minSROH"<-0
places$"minNROH"<-0
places$"class"<-"nada"
places$"indv"<-0
places$"color"<-"nada"
blankplaces<-places
dupPlaces<-places[1,]
dupPlaces[1,1]<-"lugar"
blank<-dupPlaces
library(ggplot2)
plot<-ggplot()
for(p in 1:length(lugares)) {
  thisPlace<-alltram[alltram$Location == lugares[p],]
  print(lugares[p])
  print(p)
  individuals<-Olalde$ID[Olalde$Location == lugares[p]]
  for(t in 1:length(typeROH)){
    thisType<-thisPlace[thisPlace$class==typeROH[t],]
    dupPlaces[,"indv"]<-length(individuals)
    sitio<-as.character(lugares[p])
    print(sitio,p)
    dupPlaces[,"Location"]<-sitio
    nrohCounts<-c()
    srohCounts<-c()
    for(c in 1:length(individuals)){
      thisIndv<-thisType[thisType$ID==individuals[c],]
      nrohCounts<-c(nrohCounts,nrow(thisIndv))
      srohCounts<-c(srohCounts,sum(thisIndv$"KB")/1000)
    }
    dupPlaces[,"class"]<-typeROH[t]
    dupPlaces[,"meanSROH"]<-(mean(srohCounts))
    dupPlaces[,"meanNROH"]<-(mean(nrohCounts))
    dupPlaces[,"minSROH"]<-(min(srohCounts))
    dupPlaces[,"minNROH"]<-(min(nrohCounts))
    dupPlaces[,"maxNROH"]<-(max(nrohCounts))
    dupPlaces[,"maxSROH"]<-(max(srohCounts))
    dupPlaces[,"color"]<-miPaleta[p]
    places<-rbind(places,dupPlaces)
    dupPlaces<-blank
  }
  places<-filter(places, class!="nada")
  
}
places<-filter(places, class!="nada")
places$Location<-as.factor(places$Location)
places$Location <- factor(places$Location,levels = lugares) #Because we want them ordered, we levelize them (recomended)

```
The same process can be done with filtered data
### Create the plot
We can set a a custom palette
```r
miPaleta=c("#FFB200","#005949","#BA7300","#00FCDB","#FC8200","#46918F","#CC5200","#007375","#FF4900","#00B3A4")
```
NROH and SROH can be ploted the same way, just changing the *y variable* in ggplot *aes()* parameters from *meanSROH* to *meanNROH*.
First, the differences between filtered and non filtered can be seen plotting both datasets in the same plot.
```r
#combinated dot plots
plot<-ggplot(data=places, mapping=aes(x=class, y=meanSROH, order=Location, stat="identity", group=Location, color=Location))+geom_point(shape=16)+geom_line()+scale_x_discrete(limits=typeROH)+scale_color_manual(values=miPaleta, breaks=levels(places$Location))+labs(x="ROH class",y="mean ROH size (Mb)", title="ROH size amount per Location")+theme_minimal()
combi<-plot+geom_point(data=placesFilter, aes(x=class,y=meanSROH, group=Location, color=Location, shape=10))+geom_line(linetype="dashed", data=placesFilter)+scale_shape_identity()
combi
```
![Rplot109](https://user-images.githubusercontent.com/72131448/119585288-b1dc9980-bdca-11eb-888b-becc00501c75.png)


It can be represented with separated plots too.
```r
library(ggpubr)
nonF<-ggplot(data=places, mapping=aes(x=class, y=meanSROH, order=Location, stat="identity", group=Location, fill=Location))+geom_col(position = "dodge")+scale_x_discrete(limits=typeROH)+scale_fill_manual(values=miPaleta, breaks=levels(places$Location))+labs(x="ROH class",y="mean ROH size (Mb)", title="ROH size amount per Location")+theme_minimal()+ylim(0,210)
yesF<-ggplot(data=placesFilter, mapping=aes(x=class, y=meanSROH, order=Location, stat="identity", group=Location, fill=Location))+geom_col(position="dodge")+scale_x_discrete(limits=typeROH)+scale_fill_manual(values=miPaleta, breaks=levels(places$Location))+labs(x="ROH class",y="mean ROH size (Mb)", title="ROH size amount per Location (filtered by number of SNP mapped)")+theme_minimal()+ylim(0,210)
sep<-ggarrange(nonF,yesF,labels=c("A","B"),common.legend=TRUE, legend="bottom")
sep
```
![Rplot109](https://user-images.githubusercontent.com/72131448/119585203-7e9a0a80-bdca-11eb-823f-cc44c3f333aa.png)


