# Different ways to plot ROH analysis
## Data and format
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

```


