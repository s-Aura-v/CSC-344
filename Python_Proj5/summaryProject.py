# Write a Python program that collects, summarizes, and e-mails all the programming assignments for this course.

import os

# Set Directory
# /Users/survive/Desktop/EEATO/23Fall/CSC 344/csc344
# fileDirectory = input("Enter the file directory: ")
fileDirectory = "/Users/survive/Desktop/EEATO/23Fall/CSC344/csc344"
os.chdir(fileDirectory)
os.system("ls")

# Go through each directory and print the amount of lines
os.system("find " + os.curdir + " -type f ! -name '.*' -print0 | xargs -0 wc -l ")
# Go through each directory
for file in os.listdir(fileDirectory):
    if (os.fsdecode(file)[0] == '.'):
        continue
    else:
        fileName = os.fsdecode(file)
    print(os.path.join(fileDirectory, fileName))

    # Find the code text in each file
    for program in os.listdir(fileName):
        programName = os.fsdecode(program)
        test = fileDirectory + "/" + fileName
        # os.chdir(fileDirectory + "/" + fileName)
        f = open("summary_" + fileName + ".html", 'w')
        print(programName)



# f = open("summary_" + fileName + ".html", 'w')
# fileName = "a1"
# f = open(fileName + ".html", 'w')


# def createHTML():
#     f = open()