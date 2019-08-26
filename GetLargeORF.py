# Import libraries.
import sys

# Load input file from bash script.
input_filename = sys.argv[1].split('.')[0].split('_')[0]


print("\nRunning for file: " + str(input_filename), file=sys.stderr)
#--- Insert the data in the file. ---
# Open and read file.
file = open(input_filename + "_singleline.fasta", 'r')
contents = file.read()
# Create a list that contains the IDs and Sequences.
subset = contents.splitlines()
# We don't need the file anymore.
file.close()

#--- Separate IDs and Sequences.
# Create variables to store the IDs and Sequences separately.
ids = []
seqs = []

# Loop through every element in the susbset-list.
for element in range(len(subset)):
    # If the element starts with ">" append to the IDs list, if not append it to the Sequences list.
    if subset[element].startswith('>'):
        ids.append(subset[element])
    else:
        seqs.append(subset[element])

print("Phase 1: Complete (separated sequnces and ids)", file=sys.stderr)

#--- Remove the ORF number from the end of each ORF id. ---
# Create a list to store the resulting names.
ids_prepared_for_comparison = []

# Start a loop that parses through the ids list.
for  number in range(len(ids)):
    # Set a variable that represents an ID in each loop.
    x = ids[number]

    # Loop through the variable while it ends in a number.
    while x.endswith("0") or x.endswith("1") or x.endswith("2") or x.endswith("3") or x.endswith("4") or x.endswith("5") or x.endswith("6") or x.endswith("7") or x.endswith("8") or x.endswith("9"):
        # If the variable ends in a number remove the last letter from the name.
        x = x[:-1]

    # Append the resulting variable in the list.
    ids_prepared_for_comparison.append(x)

#--- Create a list that contains only Unique transcript names. ---
unique_transcripts = list(set(ids_prepared_for_comparison))

print("Phase 2: Complete (found transcripts)", file=sys.stderr)

#--- Create a dictionary that stores the transcript IDs as keys and the transcript sequences as values. ---
d = dict.fromkeys(unique_transcripts)

# Loop through each key in the dictionary.
for key, value in d.items():
    # Set each key's value equal to an empty list.
    d[key] = []
    # For every key in the dictionary loop through  the IDs' list.
    for list_number in range(len(ids)):
        # If the id starts with the key, the append the sequence corresponding to the id based on the fact that the "ids" and "seqs" list have analogous indexes.
        if ids[list_number].startswith(key):
            d[key].append(seqs[list_number])

print("Phase 3: Complete (created dictionary)", file=sys.stderr)

#--- Calculate the length of each sequence for every key and keep the largest one. ---
largest_orfs_ids = []
largest_orfs_seqs = []

for key, value in d.items():
    largest_orfs_ids.append(key)
    # Append the largest sequence to each responding key
    largest_orfs_seqs.append(max(d[key], key=len))

print("Phase 4: Complete (gathered largest transcripts)", file=sys.stderr)

#--- Open new file to store the data. ---
new_file = open(input_filename + "_LO.fasta", 'w+')

for i in range(len(largest_orfs_ids)):
    new_file.write(str(largest_orfs_ids[i]) + '\n' + str(largest_orfs_seqs[i]) + '\n')

new_file.close()
