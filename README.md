# Splash

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

Splash, lets the user choose how the BlastX tool should run, so that he/she can save the maximum amount of time for their available resources.
The user can change the parameters in the BlastPrep.py file (which creates the Blast submition file) and submit the pipeline only once (instead of submiting every part [Splash, Blast_sucb_script.sh, SplashAB.py] as a separate entity)by adding True next to the Splash.sh filename during submission.

Examples:
++ Submit Splash.sh in a sub_script, then manually submit the Blast_sub_script.sh:

    /<absolute>/<path>/Splash.sh False
        
++ and finally submit the SplashAB.sh:
          
    /<absolute>/<path>/SplashAB.sh
  
  
  
++ Or the user can run the whole pipeline at once (with the default BlastX parameters):

    /<absolute>/<path>/Splash.sh True
