#!/bin/bash

# Splash_after_blast.

# Remove the transcripts with a hit in the database.
echo "Using blastX_reader_fromat6.py"
python3 BlastXreaderFormat6.py

# Create a file to concatenate the results.
touch Final.fasta

# Create a list of the No-hit file names.
ls No-hit*.fasta > no-hit.names

# Loop through each name in the No-hit file.
echo "Concatenating files."
for name in $(less no-hit.names);
do
  echo $name
  # Add the file contents to the Final file.
  cat $name >> Final.fasta
done

mkdir blast_output
mv *.output blast_output
