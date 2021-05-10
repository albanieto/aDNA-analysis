# aDNA-analysis
## About this repository
This repository has been created to complement my final-year thesis from my BSc in Genetics at the Universitat Autònoma de Barcelona (UAB).
Here are some bash scripts and pipelines for the analysis of aDNA aimed at people who are beginners or who are not used to the use of these bioinformatics tools.
It has been created taking into account the problems that I have faced myself, so I comment on them to help the community.
## Before starting the analysis
When performing an analysis of any kind with aDNA, it is necessary to take into account some particularities:
- The samples will always have very low coverage. This implies that for most procedures we will need to impute our variants with the reference genome
- The reliability of the results will depend on the quality of the imputation. Obtaining a very large coverage from very few variants has the consequence that a proportion of the added variants will not correspond to those that our sample would hypothetically have.
- For some analyzes, the damage that the DNA has suffered overtime must be taken into account
## Sample preparation: *aDNAprep.sh*
### Required packages
- samtools (for indexing: *.bai*)
- freebayes (for the calling variant: *.vcf*)
- beagle (for the imputed: *.vcf.gz* <- compressed file. If the provided script is used, it will be designated such that * .imputed.vcf.gz *)

All these applications can be installed through the Linux terminal quickly:

```bash
apt-get install samtools
apt-get install freebayes
apt-get install beagle
```

### To keep in mind when using the *aDNAprep.sh* script
A bash script is provided with a basic pipeline to get, from .bam files, .vcf files with the unimputed variants and with the imputed variants.
To consider:
- It is recommended to modify the script by defining the variable $ id (line 5) with the user's preferences. In my case, I wanted to keep the first 5 letters of the original file name.
- It is important to bear in mind that the nomenclature of the chromosomes in the .bam must coincide with that of the reference genome (.fa) that is used. To know the nomenclature, you can show the header of the indexed bam. You can download the reference .fa from the Google cloud repository: https://console.cloud.google.com/storage/browser/genomics-public-data/references;tab=objects?prefix=&forceOnObjectsSortingFiltering=false
`` bash
head * .bai
``
- At the time of making the variant calling, by my preference and to illustrate the example, it has only been done on chromosome 1 (line 11). Remove the -r command if you want the variant calling of the entire genome.
- The imputation with Beagle requires a genetic map and a reference vcf of the chromosomes to be analyzed. They can be obtained from the Beagle resources: https://faculty.washington.edu/browning/beagle/beagle.html
- The script has been designed keeping in mind that it is located in the same place as the .bam files and the resource files mentioned above. Also, all files are generated in the same folder. However, it is possible to change the source of the inputs and the destination of the outputs by adding the Linux path of the directory where it is located.
To run the script, it is simply necessary to either be in the same directory where the script is saved, have the applications it uses installed and write:
``` bash
.\ aDNAprep.sh
```
If you want to modify the script, after modifying the script and before executing it, it is necessary to change the notation to Linux. It can be done as follows:
``` bash
awk '{sub ("\ r $", ""); print} 'aDNAprep.sh > DNAprep2.sh
mv aDNAprep2.sh aDNAprep.sh
.\ aDNAprep.sh
```


### Steps to follow: script breakdown
#### 1. Indexing the .bam file
``` bash
samtools index your.bam
```
You get a .bai file
#### 2. Variant Calling
``` bash
freebayes -f your_ref_genome.fa -r chromosome your.bam > output_name_you_want.vcf
```
For more variant calling options it is recommended to consult the freebayes manual (--help). In the proposed script *aDNAprep.sh* only chromosome 1 is analyzed. It is important that when referencing the chromosome, it has the same annotation as the reference .fa which, in turn, must have the same annotation as the. bam
#### 3. Imputation
``` bash
beagle gp = true impute = true gt = your.vcf ref = chromosome_ref_from_beagle.vcf.gz map = your_chr_geneticmap_from_beagle.map out = name_and_path_you_want
```
For more options, consult the Beagle manual. All the files have been obtained from the resources on the Beagle page itself. It is also possible to use minimac4, which is usually recommended for aDNA, for samples in which the coverage is not very low. Otherwise, the restrictive and quality criteria will be impossible to assume. With Beagle, it is possible to impute whatever the number of variants that are going to be added and, in short, even though the quality of the imputation is not good in some windows.
