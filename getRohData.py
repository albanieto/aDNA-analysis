#!/usr/bin/env python
# coding: utf-8

# In[12]:


import os
import argparse


# In[13]:


carpeta=os.listdir() #all files in this directory


# In[ ]:





# In[48]:


act=os.getcwd()


# In[14]:





# In[76]:


parser = argparse.ArgumentParser(description='This is a simple script that takes all the .hom files generated with --homozyg plink function and put it in a .tsv file.\nThis provide you an option to filter if your files have been imputed by the quality of its imputation')
parser.add_argument("output", help="The .tsv name you want", action="store", default="rohdata", type=str)
parser.add_argument("sizeFilter", help="The minimum size of the original .vcf (not imputed). Recomendable to set a minimum size in KB to obtain the reliable results", action="store", default=0, type=int)
parser.add_argument("path", help="Path where the .vcf files are stored. Must be set if -sf has ben set", action="store", type=str, default=act)
parser.parse_args()
args = parser.parse_args()


# In[ ]:





# %tb

# In[77]:


name=args.output
print(name)
path=args.path
print(path)
sf=(args.sizeFilter)*1000
print(sf)


# In[17]:


homs=[] #we only take the ones with relevant information for ROH plots we want
for file in carpeta: 
    if file.endswith(".hom")==True:
        homs.append(file)


# In[78]:


if args.sizeFilter!=0:
    print("A minimum size has been set")
    if len(path)==0:
        print("A path where the not imputed (original) .vcf are is needed because you set a kB filter")
        quit()
    else:
        for arxiu in homs: 
            vcf=homs[homs.index(arxiu)][:-4]
            file_size = int(os.stat(path+"/"+vcf+".vcf").st_size)
            if file_size<sf:
                homs.remove(arxiu)
                print(vcf+".vcf has less than ",sf,"Bytes, so its file .hom is not considered:",file_size,"Bytes")
print("There are ",len(homs),"individuals that have passed the filter")


# In[61]:


with open(name+".tsv","w") as f:
    cap=["ID","KB","CHR"]
    print(*cap, sep="\t",file=f, end="\n") #we make the heading
    for i in range (0,len(homs)):
        with open (homs[i],"r") as r: #we iterate in all .hom files
            ID=homs[i][:-4]
            todo=r.readlines()[1:]
            listroh=[]
            for linea in todo: 
                raw=linea.split(" ") #extract and clean every line
                roh=[]
                for item in raw: 
                    if len(item)>0:
                        roh.append(item) #lines clean are in roh object
                ap=[ID,roh[8],roh[3]] #we take just id (individual), kb and chr for every roh
                print(*ap, sep="\t",file=f, end="\n") #we write it in our final file
            
                
                


# In[68]:


print("A file called ",name,".tsv has been created",sep="")


# In[ ]:




