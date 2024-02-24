import os
import re
import subprocess

# return true/false depending on built success
def build_bricklib():
    try:
    # Change to the desired directory within a context manager
        os.chdir('../bricklib/')
        # Code within this block will run with the changed working directory
        # ml gcc/11.2.0 openmpi cuda \
        commands = """
        mkdir build/ -p \
        && mkdir install/ -p \
        && cd build/ \
        && cmake ../ -DCMAKE_INSTALL_PREFIX=../install \
        && make \
        && make install -j12
        """
        subprocess.run(commands, shell=True, check=True)
        os.chdir('../')
        # All commands executed successfully
        return True
    except subprocess.CalledProcessError:
        # Handle errors if needed
        return False

# return true/false depending on built success
def build_crusher():
    pass

def run():
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


def main():
    print("Building BrickLib")
    if (build_bricklib()):
        print("Built BrickLib success")
        print("Building CRUSHER")
        # if (build_crusher()):
        #     print("Built CRUSHER success")
        #     # Built both libraries success
        #     run()



if __name__ == "__main__":
    # Call the main function
    main()
