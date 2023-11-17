# Write a Python program that collects, summarizes, and e-mails all the programming assignments for this course.
import os


def boilerplate(summaryFile, programName):
    summaryFile.write("<!DOCTYPE html>\n")
    summaryFile.write("<html lang=\"en\">\n")
    summaryFile.write("<head>\n")
    summaryFile.write("<title> Summary of " + programName + " </title>\n")
    summaryFile.write("</head>\n\n")


def summarize(summaryFile, programName, currentDirectory):
    # Get necessary info
    numOfLines = os.popen("wc -l " + currentDirectory + "/" + programName).read().split()[0]
    # Write it in the HTML file
    summaryFile.write("<body>\n")
    summaryFile.write("<h4> Summary of " + programName + "</h4>\n")
    summaryFile.write("<p> The number of lines are: " + str(numOfLines) + "</p>\n")

# Set Directory
# /Users/survive/Desktop/EEATO/23Fall/CSC 344/csc344
# fileDirectory = input("Enter the file directory: ")
fileDirectory = "/Users/survive/Desktop/EEATO/23Fall/CSC344/csc344"
os.chdir(fileDirectory)
# Go through each directory and print the amount of lines

# Go through each directory
for file in os.listdir(fileDirectory):
    os.chdir(fileDirectory)
    # print(os.system("find " + os.curdir + " -type f ! -name '.*' -print0 | xargs -0 wc -l "))
    # my mca has those hidden files and i don't want to add it to the summary
    if (os.fsdecode(file)[0] == '.'):
        continue
    else:
        fileName = os.fsdecode(file)
        print(os.path.join(fileDirectory, fileName))

    # Find the code text in each file and create an HTML file
    for program in os.listdir(fileName):
        programName = os.fsdecode(program)
        test = fileDirectory + "/" + fileName
        os.chdir(fileDirectory + "/" + fileName)
        currentDirectory = (fileDirectory + "/" + fileName)

        summaryFile = open("summary_" + fileName + ".html", 'w')
        print(programName)

        #Do the HTML magic
        boilerplate(summaryFile, programName)
        summarize(summaryFile, programName, currentDirectory)

        #Close the file
        summaryFile.close()

        # variable = os.system("grep -o -i for " + programName + " | wc -l")
        # print(str(variable))
        # summaryFile.write(str(os.system("grep -o -i for " + programName + " | wc -l")))

#


# how to grab keywords
# grep -o -i KEYWORD NAMEOFFILE | wc -l

# def createHTML():
#     f = open()
'''
os.chdir(fileDirectory)
f = open("index.html")
'''
# numOfLines = os.system("grep -o -i for " + programName + " | wc -l")
