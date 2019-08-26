# The Splash pipeline was created at the Hellenic Center of Marine Research (HMCR), in Crete (August 2019).
# It's developers were John Louloudis, Tereza Manousaki and Alexandros Tsakogiannis.

# Import libraties
import sys

# List all fasta files in the directory and set the in a variable.
input_filename = sys.argv[1].split('.')[0].split('_')[0]


fasta_file = open(input_filename + '_NC.fasta', 'r')
fasta_contents = fasta_file.read().splitlines()
fasta_file.close()

file_number = 0
# Loop through, with a 4000 step.
for line in range(0, len(fasta_contents), 4000):
    # Parse through the fasta_contents 4000 lines at a time. (2000 transcripts)
    output = fasta_contents[line:line+4000]
    # Create a file to store the 2000 transcripts.
    blast_file = open('blast_file_'+str(file_number)+'.fasta', 'w+')
    blast_file.write('\n'.join(output))
    blast_file.close()
    # Add one to file_number, to create a new file name for the next 4000 lines.
    file_number += 1


print(file_number)

#---------------- Create a file to send the blast with. ----------------
script = open('Blast_sub_script.sh', 'w+')
script.write('#!/bin/bash\n')
script.write('#SBATCH --partition=batch\n')
script.write('#SBATCH --nodes=1\n')
script.write('#SBATCH --ntasks-per-node=20\n')
script.write('#SBATCH --mem-per-cpu=6000\n')
script.write('#SBATCH --job-name="BlastXarray"\n')
script.write('#SBATCH --output=z.BlastXarray.log\n')
script.write('#SBATCH --mail-user=john.louloudis.97@gmail.com\n')
script.write('#SBATCH --mail-type=ALL\n')
# Make sure that the arrays, are the same number as the files.
script.write('#SBATCH --array=0-'+str(file_number-1)+'\n')
script.write('\nDB=/mnt/dbs/uniprot_trembl/blastUniprotdb/uniprotBLAST\n')
script.write('\nblastx -query blast_file_$SLURM_ARRAY_TASK_ID.fasta -out blast_$SLURM_ARRAY_TASK_ID.output -db $DB -outfmt 6 -evalue 1e-2 -num_threads 20')
script.close()
