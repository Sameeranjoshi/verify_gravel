import os
import re
import subprocess
import sys

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

# Creates a configuration, Runs the compression followed by decompression.
def run_CDC_pipeline(BEST_CHOOSEN_PREPROCESSOR,     # What is the best preprocessor I can choose for this computation
                     BEST_CHOOSEN_COMPONENT,        # Best component for this computation
                     ORIGINAL_INPUT,                # original file to compress, full path
                     COMPRESSED_INPUT,              # file name after compression, an intermediate file
                     CDC_INPUT):                    # File name after compression-decompression step
    current_directory = os.path.dirname(os.path.realpath(__file__))
    output_file_location = "../bricklib/"
    commands = [
        ['./generate_standalone_CPU_compressor_decompressor.py', f'"{BEST_CHOOSEN_PREPROCESSOR}"', f'"{BEST_CHOOSEN_COMPONENT}"'],
        ['g++', '-O3', '-march=native', '-fopenmp', '-mno-fma', '-I.', '-std=c++17', '-o', 'compress', 'compressor-standalone.cpp'],
        ['g++', '-O3', '-march=native', '-fopenmp', '-mno-fma', '-I.', '-std=c++17', '-o', 'decompress', 'decompressor-standalone.cpp'],
        ['./compress', f'{ORIGINAL_INPUT}', f'{output_file_location}/{COMPRESSED_INPUT}', 'y'],
        ['./decompress', f'{output_file_location}/{COMPRESSED_INPUT}', f'{output_file_location}/{CDC_INPUT}', 'y'],
        
        #['./decompress', f'{current_directory}/{COMPRESSED_INPUT}', f'{current_directory}/{CDC_INPUT}', 'y'],
        # ['cp', f'{ORIGINAL_INPUT}', f'{current_directory}'],
        # ['chmod', '777', f'{current_directory}/{CDC_INPUT}'],
        # [f'{current_directory}/{CDC_INPUT}']
    ]
    print(" Current directory : ", os.getcwd())
    # Run the commands sequentially
    for cmd in commands:
        try:
            # Run the command
            # print (cmd)
            print(" ".join(cmd))
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            # If the command fails, print an error message
            print(f"Command '{' '.join(cmd)}' failed with exit code {e.returncode}")
            break
    else:
        # All commands executed successfully
        print("All commands executed successfully")

# Runs compression-decompression on each input executable.
def run_gravel(crusherlocation, coeff_original, brick_original):
    # List of executable files
    # FILES = ('grid_contents.txt', "coefficients.txt", "output_grid_data_dmp.txt", ) #, 'cuda')
    FILES = (coeff_original, brick_original, )
    # FOLDERS = ('/uufs/chpc.utah.edu/common/home/u1418973/other/verify_gravel/python-wrapper', )#, 'strong', 'weak')
    FOLDERS = ('../bricklib', )
    
    # Output file path
    output_file_path = 'output.txt'

    #  std::string filename_brick_original = "brick_original.txt";
    # std::string filename_brick_CDC = "brick_CDC.txt"; // should be CDC brick at some point.
    # std::string filename_coeff_original = "coeff_original.txt";
    # std::string filename_coeff_CDC = "coeff_CDC.txt";
    # CDC_{coeff_original}

    os.chdir(os.path.expanduser(crusherlocation))

    # Open the output file for writing
    with open(output_file_path, 'a') as output_file:
        # Iterate over each executable file and folder combination
        for eachexe in FILES:
            for eachfolder in FOLDERS:                
                # command = f'../LC-framework/lc ../bricklib/install/bin/brick/{eachfolder}/{eachexe} CR "" "RZE_1 CLOG_1"'
                # This gives the best performance for now, choose this set to begin.
                BEST_CHOOSEN_PREPROCESSOR=""
                BEST_CHOOSEN_COMPONENT="RZE_1 CLOG_1"   # temporary value
                #TODO: THIS SHOULD BE FROM install/
                ORIGINAL_INPUT=f"{eachfolder}/{eachexe}"
                COMPRESSED_INPUT= eachexe.replace("original", "compressed")
                CDC_INPUT = eachexe.replace("original", "CDC")
                
                print(BEST_CHOOSEN_PREPROCESSOR,BEST_CHOOSEN_COMPONENT, ORIGINAL_INPUT, COMPRESSED_INPUT, CDC_INPUT)
                run_CDC_pipeline(BEST_CHOOSEN_PREPROCESSOR, BEST_CHOOSEN_COMPONENT, ORIGINAL_INPUT, COMPRESSED_INPUT, CDC_INPUT)
                print("\n")

# E2E workflow
# Build both tools followed by CDC pipeline.
def main():
    coeff_original = sys.argv[1]
    brick_original = sys.argv[2]
    

    # print("Building BrickLib")
    # if (build_bricklib('../bricklib')):
    #     print("Building BrickLib success")
    #     print("Building CRUSHER")
    #     if (build_crusher('../LC-framework')):
    #         print("Built CRUSHER success")
    #         print("Running Python Wrapper")
    run_gravel('../LC-framework', coeff_original, brick_original)

if __name__ == "__main__":
    # Call the main function
    main()
