# Microproject 1:
# Compile using: py3compile microProj.py
# Run using: python [name inside __cache__]
import os

# Get the file directory:
# /Users/survive/Desktop/EEATO/23Fall/CSC\ 344/python_Proj5/testFiles
# /home/slamich2/CSC344/python_Proj2
fileDirectory = input("Enter the file directory: ")

#Go through the directory
os.system("find " + fileDirectory + " -type f -print0 | xargs -0 wc -l")