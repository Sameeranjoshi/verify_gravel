import os
import re
import subprocess

# return true/false depending on built success
def build_bricklib(brickliblocation):
    try:
    # Change to the desired directory within a context manager
        os.chdir(brickliblocation)
        # Code within this block will run with the changed working directory
        # dict error  = python missing
        commands = """
        ml gcc/11.2.0 openmpi cuda python/3.11.7 \
        && mkdir build/ -p \
        && mkdir install/ -p \
        && cd build/ \
        && cmake ../ -DCMAKE_INSTALL_PREFIX=../install \
        && make -j12 \
        && make install -j12
        """
        print("Running Command")
        print (commands)    
        subprocess.run(commands, shell=True, check=True,  stdout=subprocess.PIPE)
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
        subprocess.run(commands, shell=True, check=True,  stdout=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

#depricated
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
                # Generic command - to move to compressor and decompressor choose some fixed algorithms.
                # command = f'../LC-framework/lc ../bricklib/install/bin/brick/{eachfolder}/{eachexe} CR "" ".+ .+"'

                # This gives the best performance for now, choose this set to begin.
                command = f'../LC-framework/lc ../bricklib/install/bin/brick/{eachfolder}/{eachexe} CR "" "RZE_1 CLOG_1"'
                print ("running command")
                print(command)
                # Run the command and capture its output
                output = os.popen(command).read()

                # You can use this when you are using heuristics to find the best schedule.
                matches = output_pattern.findall(output)

                # Write the matched parts of the output to the file
                if matches:
                    output_file.write(f"Output for '{eachfolder}/{eachexe}':\n")
                    for match in matches:
                        output_file.write(match.strip() + '\n')
                else:
                    output_file.write(f"No output found for {eachexe} in {eachfolder}\n")

    # Print a message indicating that the output has been written to the file
    print(f"Output has been written to {output_file_path}")

def run_CDC_pipeline(BEST_CHOOSEN_PREPROCESSOR,     # What is the best preprocessor I can choose for this computation
                     BEST_CHOOSEN_COMPONENT,        # Best component for this computation
                     ORIGINAL_INPUT,                # original file to compress, full path
                     COMPRESSED_INPUT,              # file name after compression, an intermediate file
                     CDC_INPUT):                    # File name after compression-decompression step
    current_directory = os.path.dirname(os.path.realpath(__file__))
    commands = [
        ['./generate_standalone_CPU_compressor_decompressor.py', f'"{BEST_CHOOSEN_PREPROCESSOR}"', f'"{BEST_CHOOSEN_COMPONENT}"'],
        ['g++', '-O3', '-march=native', '-fopenmp', '-mno-fma', '-I.', '-std=c++17', '-o', 'compress', 'compressor-standalone.cpp'],
        ['g++', '-O3', '-march=native', '-fopenmp', '-mno-fma', '-I.', '-std=c++17', '-o', 'decompress', 'decompressor-standalone.cpp'],
        ['./compress', f'{ORIGINAL_INPUT}', f'{current_directory}/{COMPRESSED_INPUT}', 'y'],
        ['./decompress', f'{current_directory}/{COMPRESSED_INPUT}', f'{current_directory}/{CDC_INPUT}', 'y'],
        ['cp', f'{ORIGINAL_INPUT}', '.'],
        ['chmod', '777', f'{current_directory}/{CDC_INPUT}']
    ]
    print(" Current directory : ", os.getcwd())
    # Run the commands sequentially
    for cmd in commands:
        try:
            # Run the command
            print (cmd)
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            # If the command fails, print an error message
            print(f"Command '{' '.join(cmd)}' failed with exit code {e.returncode}")
            break
    else:
        # All commands executed successfully
        print("All commands executed successfully")

def run_gravel(crusherlocation):
    # List of executable files
    FILES = ('cpu', ) #, 'cuda')
    FOLDERS = ('single', )#, 'strong', 'weak')

    # Output file path
    output_file_path = 'output.txt'

    os.chdir(os.path.expanduser(crusherlocation))


    # Open the output file for writing
    with open(output_file_path, 'a') as output_file:
        # Iterate over each executable file and folder combination
        for eachexe in FILES:
            for eachfolder in FOLDERS:                
                # command = f'../LC-framework/lc ../bricklib/install/bin/brick/{eachfolder}/{eachexe} CR "" "RZE_1 CLOG_1"'
                # This gives the best performance for now, choose this set to begin.
                BEST_CHOOSEN_PREPROCESSOR=""
                BEST_CHOOSEN_COMPONENT="RZE_1 CLOG_1"
                #TODO: THIS SHOULD BE FROM install/
                ORIGINAL_INPUT=f"../bricklib/build/{eachfolder}/{eachexe}"
                COMPRESSED_INPUT="compressed_cpu"
                CDC_INPUT="cdc_cpu"
                
                run_CDC_pipeline(BEST_CHOOSEN_PREPROCESSOR, BEST_CHOOSEN_COMPONENT, ORIGINAL_INPUT, COMPRESSED_INPUT, CDC_INPUT)



def main():
    print("Building BrickLib")
    if (build_bricklib('../bricklib')):
        print("Building BrickLib success")
        print("Building CRUSHER")
        if (build_crusher('../LC-framework')):
            print("Built CRUSHER success")
            print("Running Python Wrapper")
            run_gravel('../LC-framework')

if __name__ == "__main__":
    # Call the main function
    main()
