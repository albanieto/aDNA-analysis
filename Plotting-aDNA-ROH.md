# Different ways to plot ROH analysis
## Data and format
Two files are used to build the main dataframes:
\begin{enumerate}
  \item \textbf{"Roh data"}: Data obtanied processing the plink \textit{"-homozyg"} output (multiple files) via getROHData.py script available in this repository. It consists of a .csv (it can be .tsv or any other type of delimitation) in which each of the rows corresponds to a detected ROH. The columns are as follows:
    \begin{itemize}
      \item \textit{"ID"}: The sample identification or name where the ROH has been found. There will be as many rows with the same ID as ROH has been detected in this sample. (ex: I0426)
      \item \textit{"KB"}: The ROH size. The plink output is given in KB. However, it may be more convenient convert it to Mb via R. All the plots have been created doing the conversion at the moment of plotting (column in KB). (ex: 798.381)
       \item \textit{"CHR"}: Chromosome where the ROH has been detected. (ex: 1)
        \item \textit{"INITIAL"}: Position  (b) where the ROH starts. (ex: 10177)
         \item \textit{"FINAL"}: Position (b) where the ROH ends.  (ex: 808557)
       \end{itemize}
  \item \textbf{Metadata}: This file includes all the relevant information per individual/sample. Content will depend on  the study objectives. All theese data usually can be found at the suplementary materials from publicly available data papers. Here is an example: 
     \begin{itemize}
      \item \textit{"ID"}: The sample identification or name. There will be as only a row per ID. (ex: I0426)
      \item \textit{"Age"}: Average dating for every sample. Only a single number (without BCE or ACE). (ex: 2310)
      \item \textit{"Location"}: This is important as the plots are coloured by this. (ex: Paris Street, Cerdanyola del Valles, Barcelona)
      \item \textit{"nSNP"}: It is the number of SNP that where captured using the 1240k David Reich's panel. However any other parameter that can be used as a quality control (such as BAM coverage, size of .vcf, or a simple TRUE/FALSE settled down by oneself corredponding to a manual filter will work)  (ex: 374793)
      \end{itemize}
\end{enumerate}
