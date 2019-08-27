This project is licensed under the terms of the HCMR (Hellenic Center of Marine Research) license. Copyright (c) 2019 John Louloudis, Tereza Manousaki, Alexandros Tsakogiannis.

## Splash

A pipeline to identify Long Non-Coding RNAs in silico.

Splash can Identify, putative long non-coding RNAs from a pool of transcriptomics data, using ORF size, Coding potential and checks the dataset for hits against a protein database of choice.

The pipeline is written in BASH and broken into 3 main parts (Splash.sh, Blast_sub_script.sh, SplashAB.sh).
The pipeline, must be accompanied by 4 python scripts that are called at various points while it runs.
Also, there are three dependencies, that must be installed for Splash to run properly:
  -getorf
  -CPC2.py
  -blastX

ATTENTION!!!
After downloading the full Splash file, please open the main scripts and change the paths of the dependencies, python scripts, and database or you will get errors.
The database path should change from the BlastPrep.py file so that every time the Blast_submit_file.sh is created, your parameters are correct.

In order to save time Splash uses splits the dataset (into files of 2000 transcripts) and uses arrays at for the BlastX proccess.
Then, lets the user choose how the BlastX tool should run, so that he/she can save the maximum amount of time for their available resources.
The user can change the parameters in the BlastPrep.py file (which creates the Blast submition file) and submit the pipeline only once (instead of submiting every part [Splash, Blast_sucb_script.sh, SplashAB.py] as a separate entity)by adding True next to the Splash.sh filename during submission.

Examples:
  
++ Submit Splash.sh in a sub_script, then manually submit the Blast_sub_script.sh:

    /<absolute>/<path>/Splash.sh False
        
++ and finally submit the SplashAB.sh:
          
    /<absolute>/<path>/SplashAB.sh
  
  
  
++ Or the user can run the whole pipeline at once (with the default BlastX parameters):

    /<absolute>/<path>/Splash.sh True


Input file: 
  <file>.fasta
Final output: 
  Final.fasta 
Intermediate files:
  1. <file>_GF.fasta -> Output of getorf (Usually contains multiple ORFs per transcript)
  2. <file>_LO.fasta -> Longest ORF per transcript
  3. <file>_CPC2.tbl -> CPC2 output table
  4. <file>_NC.fasta -> Non-Coding ORFs (As they were characterized by CPC2)
  5. blast_file_<number>.fasta -> Files of 2000 transcripts (4000 lines) created for parallelazation of the BlastX process () Their number is arbitrary, and depends on the dataset.
  6. blast_<number>.output -> BlastX results, displayed in a table (Format 6), in the final step they will be concatenated, to create the final output.
