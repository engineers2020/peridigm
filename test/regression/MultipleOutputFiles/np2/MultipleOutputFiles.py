#! /usr/bin/env python

import sys
import os
import re
from subprocess import Popen

test_dir = "MultipleOutputFiles/np2"
base_name = "MultipleOutputFiles"

if __name__ == "__main__":

    result = 0

    # log file will be dumped if verbose option is given
    verbose = False
    if "-verbose" in sys.argv:
        verbose = True

    # change to the specified test directory
    os.chdir(test_dir)

    # open log file
    log_file_name = base_name + ".log"
    if os.path.exists(log_file_name):
        os.remove(log_file_name)
    logfile = open(log_file_name, 'w')

    # remove old output files, if any
    files_to_remove = [base_name + "1" + ".e", base_name + "2" + ".e"]
    for file in os.listdir(os.getcwd()):
      if file in files_to_remove:
        os.remove(file)

    # run Peridigm
    command = ["mpiexec", "-np", "2", "../../../../src/Peridigm", "../"+base_name+".xml"]
    p = Popen(command, stdout=logfile, stderr=logfile)
    return_code = p.wait()
    if return_code != 0:
        result = return_code

    # compare output files against gold files
    command = ["../../../../scripts/MergeFiles.py", base_name+"1", "2"]
    p = Popen(command, stdout=logfile, stderr=logfile)
    return_code = p.wait()
    if return_code != 0:
        result = return_code
    command = ["../../../../scripts/exodiff", \
               "-stat", \
               "-f", \
               "../"+base_name+"1"+".comp", \
               base_name+"1"+".e", \
               "../"+base_name+"1"+"_gold.e"]
    p = Popen(command, stdout=logfile, stderr=logfile)
    return_code = p.wait()
    if return_code != 0:
      result = return_code

    command = ["../../../../scripts/MergeFiles.py", base_name+"2", "2"]
    p = Popen(command, stdout=logfile, stderr=logfile)
    return_code = p.wait()
    if return_code != 0:
        result = return_code
    command = ["../../../../scripts/exodiff", \
               "-stat", \
               "-f", \
               "../"+base_name+"2"+".comp", \
               base_name+"2"+".e", \
               "../"+base_name+"2"+"_gold.e"]
    p = Popen(command, stdout=logfile, stderr=logfile)
    return_code = p.wait()
    if return_code != 0:
      result = return_code

    logfile.close()

    # dump the output if the user requested verbose
    if verbose == True:
        os.system("cat " + log_file_name)

    sys.exit(result)
