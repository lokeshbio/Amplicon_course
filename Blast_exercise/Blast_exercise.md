-   [Blast](#blast)
    -   [Making a local blast database](#making-a-local-blast-database)
        -   [Nucleotide database](#nucleotide-database)
        -   [Protein database](#protein-database)
    -   [Running blast commands](#running-blast-commands)
    -   [Main exercise](#main-exercise)

Blast
=====

Here we will look at how to make your own local blast database and then run your own blast analysis! These are very simple and small datasets.

Making a local blast database
-----------------------------

Since you are already using QIIME2 interface, they have all the blast tools installed locally. So let's start with making local database!

### Nucleotide database

Databases are made by the `makeblastdb` command as follows.

``` bash

makeblastdb -in nucleotide_db.fna -dbtype nucl -title Nucleotide_database_in_course -out nucleotide_db
```

When you run this command, you will notice that at the end there will be 3 files that were made from this command with extensions `.nhr`, `.nin` and `.nsq`. These are the binary indexes that when you run the `blastn` command, the command will make use of it. You don't have to look into these files much further.

### Protein database

it is exactly the same as above, but with important changes!

``` bash

makeblastdb -in protein_db.faa -dbtype prot -title protein_database_in_course -out protein_db
```

You will notice that similar to the previous command 3 files with extensions `.phr`, `.pin` and `.psq` will be made. This is an indication for you, if a certain database is `proteins` or `nucleotides`.

Running blast commands
----------------------

Now that we have made the databases, it is time to run some blast commands and look at the output!

The three main blast commands that are very commonly used `blastn`, `blastp` and `blastx` are very similar in their syntax! You just need to make sure you use the right `query` and `database`.

1.  BLASTN - Nucleotides vs Nucleotides
2.  BLASTP - Proteins vs Proteins
3.  BLASTX - Nucleotides vs Proteins

``` bash

blastn -db nucleotide_db -query nucleotide_query.fna -out Nuc_vs_Nuc.blastn -evalue 1E-10 -num_alignments 5 -num_descriptions 10
```

Notice hear that we only have to put `nucleotide_db` for the database without their file extension as the program will automatically look for the three related files.

Important information about all these three commands is that you can look up the different options using `blastn -h` for shorter help and `blastn -help` for a very descrptive help messages. These blast commands will by default produce the output in the original blast format.

You can take a quick look by:

``` bash

less Nuc_vs_Nuc.blastn 
# Press 'q' to exit
```

To get output in the tabular format:

``` bash

blastx -db protein_db -query nucleotide_query.fna -out Nuc_vs_Prot.tsv -evalue 1E-10 -num_alignments 5 -num_descriptions 10 -outfmt 6
```

Main exercise
-------------

Try to see the if the e-value remains the same for all the matches when you do a reverse blast. By which, I mean create a database out of the fasta filenames with `query` and then use the fasta files with `db` in filenames as query.

When you look at the score and the E-value for a same match in two different blast runs, what would remain the same and what would change? And why so?

Which of these blast programs do you think is the slowest and why?
