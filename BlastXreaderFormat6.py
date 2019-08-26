# Import libraries.
import pandas as pd
import glob

# List all fasta files in the directory and set the in a variable.
input_filenames = glob.glob("*.output")

for file_number in range(len(input_filenames)):
    # Insert the blast output.
    data = pd.read_csv('blast_'+str(file_number)+'.output', sep='\t')

    # Open the corresponding fasta file.
    file = open('blast_file_'+str(file_number)+'.fasta', 'r')
    fasta = file.read().splitlines()
    file.close()

    print("Length of fasta file before: " + str(len(fasta)))
    #
    fasta_ids = []
    fasta_seqs = []

    # Loop through every element of the fasta-list.
    for element in fasta:
        # If the element starts with ">" then its is the id.
        if element.startswith('>'):
            fasta_ids.append(element)
        # Else it is the sequence.
        elif element.startswith('A') or element.startswith('T') or element.startswith('G') or element.startswith('C'):
            fasta_seqs.append(element)

    # Keep the unique IDs from the blast.output file.
    blast_ids = data.iloc[:, 0]
    blast_ids = list(set(blast_ids))

    #
    to_remove = []

    #
    for number in range(len(fasta_ids)):
        for element in blast_ids:
            if ">"+element == fasta_ids[number]:
                to_remove.append(fasta_ids[number])
                to_remove.append(fasta_seqs[number])

    for removal in to_remove:
        for line in fasta:
            if line == removal:
                fasta.remove(line)

    print("Length of fasta file after: " + str(len(fasta)) + "\n")

    output_file = open('No-hits_'+str(file_number)+'.fasta', 'w+')
    for line in fasta:
        output_file.write(line + '\n')
    output_file.close()
