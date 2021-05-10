#!/bin/bash
for file in *.bam
do
#Choose the correct id for you and modify it. In my case, only the first 5 letters of the file name
id=${file:0:5}
echo $id starting...
echo $id indexing via samtools... 
samtools index $file
echo $id indexed. $file.bai has been created
echo $id variant calling via freebayes...
#In my case, I have chosen only to call variants from chr1 with parameter -r. Remove it if u want a full variant calling
#Make sure you provide a .fa reference genome file. In my case is GRCh37-lite.fa
freebayes -f GRCh37-lite.fa -r 1 $file > $id.vcf
echo $id variant call done
echo $id.vcf has been created
out=$id.imputed
echo imputation starts for $id
#ref and map files has been downloaded from Beagle resource webpage
beagle gp=true impute=true gt=$id.vcf ref=chr1.1kg.phase3.v5a.vcf.gz map=plink.chr1.GRCh37.map out=$out
echo imputation for $id done. $out.vcf.gz has been created
echo decompressing the file...
gunzip $out.vcf.gz
echo Both .vcf files, imputed and not imputed, have been created for $id
done
