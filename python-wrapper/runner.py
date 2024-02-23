import os
import re

# List of executable files
FILES = ('cpu', 'cuda', 'mpi')
FOLDERS = ('single', 'strong', 'weak')

# Define a regular expression pattern to match the desired output
output_pattern = re.compile(r'Overall best.*?(?=Overall best|\Z)', re.DOTALL)

# Output file path
output_file_path = 'output.txt'

# Open the output file for writing
with open(output_file_path, 'w') as output_file:
    # Iterate over each executable file and folder combination
    for eachexe in FILES:
        for eachfolder in FOLDERS:
            # Command to run for each executable
            command = f'../LC-framework/lc ../bricklib/install/bin/brick/{eachfolder}/{eachexe} CR "" ".+"'

            # Run the command and capture its output
            output = os.popen(command).read()

            # Find matches using the regular expression pattern
            matches = output_pattern.findall(output)

            # Write the matched parts of the output to the file
            if matches:
                output_file.write(f"Output for {eachexe} in {eachfolder}:\n")
                for match in matches:
                    output_file.write(match.strip() + '\n')
            else:
                output_file.write(f"No output found for {eachexe} in {eachfolder}\n")

# Print a message indicating that the output has been written to the file
print(f"Output has been written to {output_file_path}")
