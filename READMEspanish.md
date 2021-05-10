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
\begin{verbatim}
apt-get install samtools
apt-get install freebayes
apt-get install beagle
\end{verbatim}
### A tener en cuenta al usar el script *aDNAprep.sh*
Se proporciona un script de bash con una pipeline básica para conseguir, a partir de ficheros .bam, ficheros .vcf con las variantes sin imputar y con las variantes imputadas.
A tener en cuenta:
- Se recomienda modificar el script al definir la variable $id (línea 5) con las preferencias del usuario. En mi caso, quería conservar las 5 primeras letras del nombre original del archivo.
- Es importante tener en cuenta que la nomenclatura de los cromosomas en el .bam debe coincidir con la del genoma de referencia (.fa) que se utiliza.



#############
This repository has been created to compliment my final-year thesis in Genetics at Universitat Autònoma de Barcelona. 
