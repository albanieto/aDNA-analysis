# aDNA-analysis
## Sobre este repositorio
Este repositorio ha sido creado para complementar mi trabajo de fin de grado de Genética en la Universidad Autònoma de Barcelona (UAB).
Aquí se recogen algunos scripts de bash y pipelines para el análisis del aDNA dirigido a personas principiantes o que no están habituados con el uso de estas herramientas bioinformáticas. 
Ha sido creado teniendo en cuenta los problemas que yo misma he enfrentado, de forma que los comento con el fin de poder ayudar a la comunidad. 
## Antes de comenzar el análsis
A la hora de realizar un análisis de cualquier tipo con aDNA, es necesario tener en cuenta algunas particularidades: 
- Las muestras serán siempre de muy bajo coverage, de forma que para la mayoría de procedimientos necesitaremos imputar nuestras variantes con el genoma de referencia
- De la calidad de la imputación dependerá después la fiablidad de los resultados. Conseguir un coverage muy grande a partir de muy pocas variantes tiene como consecuencia que una proporción de las variantes añadidas no se corresponderán con las que verdaderamente tendría nuestra muestra. 
- Para algunos análisis se deberá tener en cuenta el daño que el DNA ha sufrido por el paso del tiempo
## Preparación de las muestras: *aDNAprep.sh*
### Paquetes necesarios
- samtools (para el indexado: *.bai*)
- freebayes (para el variant calling: *.vcf*) 
- beagle (para la imputación: *.vcf.gz* <-- fichero comprimido. Si se utiliza el script proporcionado se designará tal que *.imputed.vcf.gz*)

Todas estas aplicaciones pueden instalarse mediante la terminal de linux de forma rápida: 
```bash
apt-get install samtools
apt-get install freebayes
apt-get install beagle
```

### A tener en cuenta al usar el script *aDNAprep.sh*
Se proporciona un script de bash con una pipeline básica para conseguir, a partir de ficheros .bam, ficheros .vcf con las variantes sin imputar y con las variantes imputadas.
A tener en cuenta:
- Se recomienda modificar el script al definir la variable $id (línea 5) con las preferencias del usuario. En mi caso, quería conservar las 5 primeras letras del nombre original del archivo.
- Es importante tener en cuenta que la nomenclatura de los cromosomas en el .bam debe coincidir con la del genoma de referencia (.fa) que se utiliza. Para conocer la nomenclatura se puede mostrar la cabecera del bam indexado. Es posible descargar el .fa de referencia del repositorio de Google cloud: https://console.cloud.google.com/storage/browser/genomics-public-data/references;tab=objects?prefix=&forceOnObjectsSortingFiltering=false
````bash
head *.bai
````
- A la hora de realizar el variant calling, por mi preferencia y para ilustrar el ejemplo, solamente se ha realizado del cromosoma 1 (línea 11). Elimine el comando -r si quiere el variant calling del genoma completo. 
- La imputación con Beagle requiere de un mapa genético y de un vcf de referencia de el/los cromosomas que se analizarán. Es posible obtenerlos a partir de los recursos de Beagle: https://faculty.washington.edu/browning/beagle/beagle.html
- El script ha sido diseñado teniendo en cuenta que está ubicado en el mismo lugar que los archivos .bam y los archivos de recurso mencionados antes. Además, todos los archivos se generan en la misma carpeta. No obstante, es posible cambiar el lugar de origen de los input y de destino de los output añadiendo la ruta linux del directorio en el que se encuentra.

Para ejecutar el script, simplemente es necesario o estar en el mismo directorio en el que se guarde script, tener las aplicaciones que utiliza instaladas y escribir: 
````bash
.\aDNAprep.sh
````
Si se quiere modificar el script, después de modificar el script y antes de ejecutacutarlo es necesario cambiar la notación a linux. Se puede hacer de la siguiente forma: 
````bash
awk '{ sub("\r$", ""); print }' aDNAprep.sh > aDNAprep2.sh
mv aDNAprep2.sh aDNAprep.sh
.\aDNAprep.sh
````


### Pasos a que se siguen: desglose del script
#### 1. Indexado del fichero .bam 
````bash
samtools index your.bam
````
Se obtiene un fichero .bai
#### 2. Variant Calling
````bash
freebayes -f your_ref_genome.fa -r chromosome/s your.bam > output_name_you_want.vcf
````
Para más opciones de variant calling se recomienda consultar el manual de freebayes (--help). En el script propuesto *aDNAprep.sh* se analiza solo el cromosoma 1. Es importante que al referenciar el cromosoma, este tenga la misma anotación que el .fa de referencia el cual, a su vez, debe tener la misma anotación que el .bam
#### 3. Imputación
````bash
beagle gp=true impute=true gt=your.vcf ref=chromosome_ref_from_beagle.vcf.gz map=your_chr_geneticmap_from_beagle.map out=name_and_path_you_want
````
Para más opciones, consultar el manual de Beagle. Todos los archivos han sido obtenidos a patir de los recursos en la propia página de Beagle. También es posible utilizar minimac4, el cual se suele recomendar para aDNA, para muestras en las que el coverage no sea muy bajo. De lo contrario, los criterios restrictivos y de calidad serán imposibles de asumir. Con Beagle es posible imputar sea cual sea el número de variantes que se van a añadir y, en definitiva, pese a que la calidad de la imputación no sea buena en algunas ventanas. 

