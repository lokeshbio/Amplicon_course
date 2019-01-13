-   [QIIME2](#qiime2)
    -   [GitHub files information](#github-files-information)
    -   [Importing sequence files](#importing-sequence-files)
        -   [Fastq Manifest format](#fastq-manifest-format)
        -   [EMP format](#emp-format)
        -   [Paired-end](#paired-end)
        -   [Trimming](#trimming)
    -   [Summarizing samples](#summarizing-samples)
    -   [DADA2 analysis](#dada2-analysis)
        -   [Visualizing DADA2 results](#visualizing-dada2-results)
    -   [Taxonomic classifications](#taxonomic-classifications)
    -   [Bar plots](#bar-plots)
    -   [Exporting classifications and table](#exporting-classifications-and-table)
    -   [Krona plots](#krona-plots)
    -   [PhyloSeq](#phyloseq)

QIIME2
======

This is the readme file for the Qiime2 pipeline to use for the analysis of 16S amplicons for example! The pipeline below is maonly based on the actual Qiime2 tutorial that is called [Moving Pictures](https://docs.qiime2.org/2018.11/tutorials/moving-pictures).

Open your `Terminal` in the linux environment!

You can activate Qiime2 by the following command in your terminal:

``` bash
conda info --envs
# copy the exact qiime2 name in the above list and replace "qiime2" in the following command with that
source activate qiime2
```

GitHub files information
------------------------

All the files related to this course are in my github page under the repository "Amplicon\_course"

You can download all the files that are in there using the following command.

``` bash
git clone https://github.com/lokeshbio/Amplicon_course.git
```

In here, you can see that I have 3 different directories with the files necessary for each of the exercise. For the sake of the course and it's simplicity, we will work on the 16S amplicons. If I forgot to explain why 16S in this case is simpler than amoA, SCREAM AT ME!!!

``` bash
cd 16S_related
fastqc sample1.fastq.gz
```

`open the html file in a browser` to see the results

Now we have run `fastqc` which basically tells you how the sequencing has been done for this sample and also the sequence processing it has went through! As you might notice that there is almost no Adaptors for example! This is because these samples have been already processed for their quality and trimming and so on.


Importing sequence files
------------------------

In this section, I will try to show the different ways of imporing your sequence data depending on what format you have the data. Like you can have a multiplexed sequence data, an already demultiplexed data that are either in single-end or paired-end mode!

For this course, we will use the Manifest format!

### Fastq Manifest format

This means that the sequence data is already demultiplexed and you have all your samples separately as different files! So you use a text file that explains the different `fastq.gz` files for the different samples. An example is given below:

The `fastq.gz` absolute filepaths may contain environment variables (e.g., $HOME or $PWD). The following example illustrates a simple fastq manifest file for paired-end read data for two samples. It is basically a `csv` file with a header.

``` bash
sample-id,absolute-filepath,direction
# Lines starting with '#' are ignored and can be used to create
# "comments" or even "comment out" entries
sample-1,$PWD/some/filepath/sample1_R1.fastq.gz,forward
sample-2,$PWD/some/filepath/sample2_R1.fastq.gz,forward
sample-1,$PWD/some/filepath/sample1_R2.fastq.gz,reverse
sample-2,$PWD/some/filepath/sample2_R2.fastq.gz,reverse
```

Then you could use this file to make your QIIME artefact! For the course, please use the `manifest.txt` file that was provided!

``` bash
qiime tools import --type 'SampleData[SequencesWithQuality]' --input-path manifest.txt --output-path Amp_course_demux.qza --input-format SingleEndFastqManifestPhred33
```

The file `Amp_course_demux.qza` will be your demultiplexed QIIME artefact. Now you can visualize the different general properties of the samples by the following command.

For the course, now you can jump directly to `Summarizing samples` step!!

### EMP format

In this case it is a multiplexed sequence data, meaning the samples are not separated in yet based on their barcodes (indexes). The EMP (Earth Microbiome Project) format always contains the amplicon reads in two files: "reads.fq.sh" file and the "barcodes.fq.sh" file.

We can get these two files separately from a single fastq file from Ion-Torrent data that has the barcodes in the sequence (also called in-line barcodes) by using the commnad from Qiime1 "extract\_barcodes.py".

You can skip this step and go to `qiime tools import` step, if you already have barcodes in a separate file.

``` bash
extract_barcodes.py -f IonTorrent_Run2.fastq.corrected -l 8 -m Sample_metadata.txt
```

Here the `-l` represents the length of the barcode and `-m` the mapping file for the samples.

then we have the output of the above command in a folder called `Bar_a_seq`

First, we import the reads and barcodes into a QIIME artifact

``` bash
qiime tools import --type EMPSingleEndSequences --input-path Bar_a_seq --output-path Amp170209.qza
```

Then, we demultiplex the reads into samples using the mapping file.

``` bash
qiime demux emp-single --i-seqs Amp170209.qza --m-barcodes-file ../Asg_090217_sam_map.txt --m-barcodes-category BarcodeSequence --o-per-sample-sequences Amp170209.demux.qza
```

### Paired-end

This step only imports Forwrd reads `forward.fastq.gz`, Reverse reads `reverse.fastq.gz` and the Barcodes `barcodes.fastq.gz` file in the EMP format. Similarly, you can also the `fastq manifest` as mentioned above to import the data as well.

``` bash
qiime tools import --type EMPPairedEndSequences --input-path . --output-path amp_nov_2018.qza
```

Now comes demultiplexing! In here demultiplex samples based on barcodes first before you do primer/adaptor removal. In the map file you can specify a selected number of samples to make a small file.

``` bash
qiime demux emp-paired --m-barcodes-file DG280F_map.tsv --m-barcodes-column BarcodeSequence --i-seqs ../amp_nov_2018.qza --o-per-sample-sequences DG280F.qza
```

It's time to cutadapt trimming, as it is implemented in qiime2

### Trimming

In this step you trim all the sequences to remove adaptors and primers. This is necessary, when you analyse your raw data. You can learn about the different options I have used by typing `qiime cutadapt trim-paired --help`

``` bash
qiime cutadapt trim-paired --i-demultiplexed-sequences DG280F.qza --p-front-f AATCGNTANGGGCCGTGA --p-adapter-f AGATCGGAAGAGCACACGTC --p-front-r GACCACTTGAAGAGCTGGT --p-adapter-r AGATCGGAAGAGCGTCGTGT --o-trimmed-sequences DG280F_trimmed.qza --output-dir cutadapt_di --verbose > cutadapt_trim.log
```

Summarizing samples
-------------------

Here, we summarize the demultiplexed samples and their individual sequence counts and also to look at the sequence quality plot to choose parameters for trimming in the following steps.

``` bash
qiime demux summarize --i-data Amp_course_demux.qza --o-visualization Amp_course_demux.qzv
```

Then, we can visialize the summary file in a web browser by:

``` bash
qiime tools view Amp_course_demux.qzv
```

DADA2 analysis
--------------

After the demultiplexing step, the quality control, 'ASV' selection, chimera checking and many other qulaity steps are done by the pipleline `DADA2` along with extracting the representative sequnces and building a table for the representatives. All of this is done by just one command:

``` bash
qiime dada2 denoise-single --i-demultiplexed-seqs Amp_course_demux.qza --p-trim-left 20 --p-trunc-len 245 --p-n-threads 5 --o-representative-sequences Amp_course.rep-seqs-dada2.qza --o-table Amp_course.table-dada2.qza --o-denoising-stats dada2_stats.txt
```

Note that the `--p-trim-left 20` is to remove the forward primer and `--p-trunc-len` is to remove the reverse primer and also based on how the quality of the sequences looked like from the previous step. `Amp_course.rep-seqs-dada2.qza` contains the representative sequences and `Amp_course.table-dada2.qza` contains their respective abundance.

### Visualizing DADA2 results

We can visialize the different characteristics of the reprentstavive sequences and the table by the following commands:

``` bash
qiime feature-table tabulate-seqs --i-data Amp_course.rep-seqs-dada2.qza --o-visualization Amp_course.rep-seqs-dada2.qzv
qiime feature-table summarize --i-table Amp_course.table-dada2.qza --o-visualization Amp_course.table-dada2.qzv --m-sample-metadata-file metadata_file.txt

qiime tools view Amp_course.table-dada2.qzv
qiime tools view Amp_course.rep-seqs-dada2.qzv
```

Taxonomic classifications
-------------------------

Now, we can classify the representative sequences to their respective taxonomic unit using the already existing reference sequences such as the SILVA database.

``` bash

qiime feature-classifier classify-consensus-vsearch --i-query Amp_course.rep-seqs-dada2.qza --i-reference-reads $PWD/16S_SILVA132_99_otus.qza --i-reference-taxonomy $PWD/16S_SILVA132_99_taxa.qza --p-threads 5 --output-dir Silva_classified
```

Bar plots
---------

The Qiime barplots can be plotted using the following commnad:

``` bash

qiime taxa barplot --i-table Amp_course.table-dada2.qza --i-taxonomy Silva_classified/classification.qza --m-metadata-file  metadata_file.txt --o-visualization silva_taxa-bar-plots.qzv
```

Exporting classifications and table
-----------------------------------

``` bash
qiime tools export --input-path Silva_classified/classification.qza --output-path .
qiime tools export --input-path Amp_course.table-dada2.qza --output-path .
```

The classfication table has a name `taxonomy.tsv` as an output with taxonomy for each ASV and the table output is in biom format!

Krona plots
-----------

Installing Krona-Tools:

``` bash

tar xvf KronaTools-2.7.tar
cd KronaTools-2.7
sudo ./install.pl
cd ..
```

Type the `password` and it should be fine. If you run into problems, let me know!!

Here, we would combine the taxonomy classifications and the abundance table from the biom table to make Krona plots

``` bash

biom convert -i feature-table.biom -o Amp_course.table-dada2.tab --to-tsv

mkdir txt_files
cd txt_files
../../krona_qiime.py ../taxonomy.tsv ../Amp_course.table-dada2.tab
cd ..
```

The above `biom` command will create a normal ASV abundance table. then, we combine the the taxonomic classification of the ASV to their abundance using my own `krona_qiime.py` command. This will create text files for each sample in the analysis. then we would combine the text files to make the krona plots.

``` bash
ktImportText txt_files/* -o Amp_course_silva132_krona.html
```

PhyloSeq
--------

Now let's move on to making some prettier plots!! By which I mean making stacked bar plots ;)

For this we need to convert the `taxonomy.tsv` and `Amp_course.table-dada2.tab` files to a format that the phyloseq can understand!

``` bash

tsv_to_phyloseq.py taxonomy.tsv phyloseq_taxa.tsv
perl -pe 's/\#OTU/OTU/' Amp_course.table-dada2.tab > phyloseq_otu.tsv
```

Please run the following commands in R studio!!

``` r
library("phyloseq")
library("ggplot2")
otumat <- as.matrix(read.table("phyloseq_otu.tsv",row.names = 1,header = T,sep = "\t"))
taxmat <- as.matrix(read.table("phyloseq_taxa.tsv",row.names = 1,header = T,sep = "\t"))
metamat <- as.data.frame(read.table("metadata_phyloseq.txt",row.names = 1,header = T,sep = "\t"))
# Normal abundance
OTU = otu_table(otumat, taxa_are_rows = TRUE)
# Relative abundance
OTUr = transform_sample_counts(OTU, function(x) x*100/sum(x))

TAX = tax_table(taxmat)

META = sample_data(metamat)
physeq = phyloseq(OTU, TAX, META)
physeq_r = phyloseq(OTUr, TAX, META)
arc = subset_taxa(physeq, kingdom == "Archaea")
arc_r = subset_taxa(physeq_r, kingdom == "Archaea")

plot_bar(arc,fill = "phylum",x="Description", title = "Archaeal abundance")
plot_bar(arc_r,fill = "phylum",x="Description", title = "Archaeal relative abundance")
```

here you should be able to see more nicer plots than the previous one! In Phyloseq we can also go a bit more deep into look to only particular groups and so on.

``` r
thaum_r = subset_taxa(physeq_r, phylum == "Thaumarchaeota")
plot_bar(thaum_r,fill = "class",x="Description", title = "Thaumi abundance")
```

We can also subset samples!

``` r
Enr = subset_samples(physeq_r, Project == "Enrichment")
Enr_thaum = subset_taxa(Enr, phylum == "Thaumarchaeota")
plot_bar(Enr_thaum,fill = "class",x="Description", title = "Thaum relative abundance in Enrichment")
```

``` r
Bio = subset_samples(physeq_r, Project == "Bioreactor")
Bio_eury = subset_taxa(Bio, phylum == "Euryarchaeota")
plot_bar(Bio_eury,fill = "class",x="Description", title = "Euryarchaeota relative abundance in Bioreactor")
```
