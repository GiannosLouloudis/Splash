#!/bin/bash


# List all fasta files in the directory and append their names (no extension) to the assemblies.tmp file.
ls *.fasta > assemblies.tmp
awk -F "." '{print $1}' assemblies.tmp > just_names.tmp && mv just_names.tmp assemblies.tmp

# Create a file with open reading frames above the minsize threshold.
echo "Applying getorf on selected files."

for assembly in $(less assemblies.tmp);
do
  echo $assembly
  echo
  getorf -find 2 -minsize 200 -sequence $assembly".fasta" -outseq $assembly"_GF.fasta"

done

echo "Getorf has finished."
echo
echo

### --------------------- Keep only the largest ORF found in the getorf output files for each transcript. ---------------------

rm *.tmp
ls *_GF.fasta > GF_names.tmp
awk -F "." '{print $1}' GF_names.tmp > assemblies_GF.tmp
awk -F "_" '{print $1}' assemblies_GF.tmp > assemblies.tmp

# Change the fasta file into single-line sequence after each ID.
for name in $(less assemblies.tmp);
do
  awk '{if(NR==1) {print $0} else {if($0 ~ /^>/) {print "\n"$0} else {printf $0}}}' $name"_GF.fasta" > $name"_singleline.fasta"
  awk '{print $1}' $name"_singleline.fasta" > tmp && mv tmp $name"_singleline.fasta"

  # Use GetLargeORF to extract the largest sequence per transcript.
  echo "Extracting largest sequence per transcript..."

  python3 GetLargeORF.py $name"_singleline.fasta"

  echo
  echo "Extraction completed"
  echo
  echo

done

### --------------------- Apply CPC2. ---------------------
# Remove previous temporary files.
rm *.tmp

# Create a list of all lo_*.fasta files that have passed the process.
ls *_LO.fasta >> fasta_names_unprocessed.tmp
awk -F "." '{print $1}' fasta_names_unprocessed.tmp >> fasta_names.tmp
awk -F "_" '{print $1}' fasta_names.tmp > assemblies.tmp

# Loop through every file in the list and apply CPC2 on it.
echo "Applying CPC2 on selected files."

for name in $(less assemblies.tmp);
do
  echo $name'_LO.fasta'
  echo

  /home1/louloudis/CPC2/2.CPC2/CPC2-beta/bin/CPC2.py -i $name'_LO.fasta' -o $name'_CPC2.tbl'

	sed -i "s/\t/,/g" $name'_CPC2.tbl'
done

echo "CPC2 has finished."
echo
echo

### --------------------- Remove coding reads from the fasta file based on the CPC2-output file. ---------------------
# Keep track of how many transcripts you start with.
for name in $(less assemblies.tmp);
do
  echo "Original file starts with this number of lines:" >> singleline.length
  wc -l $name"_LO.fasta" >> singleline.length
  echo >> singleline.length

  echo "Starting removing process."

  python3 CodingRemover.py $name"_LO.fasta"

  echo
  echo
  echo "After removing Coding Transcripts, the number of lines is: " >> singleline.length
  wc -l $name"_NC.fasta" >> singleline.length

  # Split the file into files of 2000 transcripts.
  echo "Splitting files and preparing blast submition file."
  python3 BlastPrep.py $name"_NC.fasta"
done

rm *.tmp

if [ $1 == "True"];
then
  sbatch Blast_sub_script.sh

  # After BlastX has finished blast.
  mkdir blast_output
  mv *.output blast_output
  cd ./blast_output

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

  rm no-hit.names
fi
