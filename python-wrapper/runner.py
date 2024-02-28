import os
import re
import subprocess

# return true/false depending on built success
def build_bricklib(brickliblocation):
    try:
    # Change to the desired directory within a context manager
        os.chdir(brickliblocation)
        # Code within this block will run with the changed working directory
        commands = """
        ml gcc/11.2.0 openmpi cuda \
        && mkdir build/ -p \
        && mkdir install/ -p \
        && cd build/ \
        && cmake ../ -DCMAKE_INSTALL_PREFIX=../install \
        && make -j12 \
        && make install -j12
        """
        print("Running Command")
        print (commands)    
        subprocess.run(commands, shell=True, check=True)
        # os.chdir('../')
        # All commands executed successfully
        return True
    except subprocess.CalledProcessError:
        # Handle errors if needed
        return False

# return true/false depending on built success
def build_crusher(crusherlocation):
    print("Changing directory OLD: ", os.getcwd())
    # relative path
    os.chdir(os.path.expanduser(crusherlocation))    
    print("NEW:", os.getcwd())
    commands = """
    ./generate_Host_LC-Framework.py \
    && g++ -O3 -march=native -fopenmp -DUSE_CPU -I. -std=c++17 -o lc lc.cpp
    """
    try:
        print("Running commands ")
        print (commands)
        subprocess.run(commands, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def run():
    # List of executable files
    FILES = ('cpu', ) #, 'cuda')
    FOLDERS = ('single', )#, 'strong', 'weak')

    # Define a regular expression pattern to match the desired output
    output_pattern = re.compile(r'Overall best.*?(?=Overall best|\Z)', re.DOTALL)

    # Output file path
    output_file_path = 'output.txt'

    # Open the output file for writing
    with open(output_file_path, 'a') as output_file:
        # Iterate over each executable file and folder combination
        for eachexe in FILES:
            for eachfolder in FOLDERS:
                # Command to run for each executable
                command = f'../LC-framework/lc ../bricklib/install/bin/brick/{eachfolder}/{eachexe} CR "" ".+"'
                print ("running command")
                print(command)
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
    if (build_bricklib('../bricklib')):
        print("Building BrickLib success")
        print("Building CRUSHER")
        if (build_crusher('../LC-framework')):
            print("Built CRUSHER success")
            #Built both libraries success
            run()



if __name__ == "__main__":
    # Call the main function
    main()
