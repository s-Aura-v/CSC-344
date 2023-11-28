# Write a Python program that collects, summarizes, and e-mails all the programming assignments for this course.
import os
import re

def createHTML(index):
    index.write("<!DOCTYPE html>\n"
                "<html lang=\"en\">\n"
                "<head>\n"
                "<title> Summary of CSC344 Fall 2023 </title>\n"
                "</head>\n\n")

    index.write("<h2> All of the programming challenges: </h2>\n"
                "<ol>\n"
                "<li> C Program: </li>" + "<a href=./a1/summary_a1.html> TuringMachine.c </a>\n" 
                "<li> Clojure Program: </li>" + "<a href=./a2/summary_a2.html> InferenceSys.clj</a>\n"
                "<li> OCaml Program: </li>" + "<a href=./a3/summary_a3.html> PatternMatching.ml</a>\n"
                "<li> ASP Program: </li>" + "<a href=./a4/summary_a4.html> DistancingSim.lp</a>\n"
                "<li> Python Program: </li>" + "<a href=./a5/summary_a5.html> SummaryOfCSC344.py</a>\n")


def writeList(identifiers, summaryFile):
    summaryFile.write("<p> Here are the ordered list of identifiers: </p>")
    summaryFile.write("<ol> \n")
    for identifier in identifiers:
        summaryFile.write("<li> " + identifier + " </li>\n")
    summaryFile.write("</ol> \n")


def createKeywordList(programName, summaryFile):
    # Clojure
    programFile = open(programName, "r")
    programSuffix = programName[-3:];
    if (programSuffix == "clj"):
        identifiersCLJ = set()
        with programFile as file:
            for line in file:
                # print(line, end="")
                if ";;" in line:
                    continue
                if "defn" in line:
                    identifiersCLJ.add(line.split()[1])
                if "let" in line or "for" in line:
                    identifiersCLJ.add(line.split()[1][1:])
                if "[" in line:
                    if line.split()[0][0] == "[":
                        if len(line.split()) == 1:
                            identifiersCLJ.add(line.split()[0][1: len(line.split()[0]) - 1])
                        if len(line.split()) > 1:
                            identifiersCLJ.add(line.split()[0][1:])
                            identifiersCLJ.add(line.split()[1][0: line.split()[1].index("]")])
                if ("[" in line and "]" not in line):
                    identifiersCLJ.add(line.split()[1][1:])
                    identifiersCLJ.add(line.split()[2][2:6])
                    # print(line.split()[1][1:])
                    # print(line.split()[2][2:6])
                if ("]" in line and "[" not in line):
                    identifiersCLJ.add(line.split()[0])
                    identifiersCLJ.add(line.split()[1][0:5])
                    # print(line.split()[0])
                    # print(line.split()[1][0:5])


    # Mostly works: Add TOK_Identifiers and remove comments + remove Some: incomplete
    elif (programSuffix == ".ml"):
        identifiers = set()
        with programFile as file:
            for line in file:
                # print(line, end="")
                # ignore comments
                if "(*" in line:
                    comment = True
                if "*)" in line:
                    comment = False
                if comment:
                    continue

                if "=" in line:
                    if "rec" in line:
                        # print(line.split()[2])
                        identifiers.add(line.split()[2])
                    else:
                        # print(line.split()[1])
                        identifiers.add(line.split()[1])

                # Grab the alphabet
                # if "|" in line:
                #     if "|" in line.split():
                #         print("hi")
                        # print(line)
                        # print(line.split()[line.split().index("|") + 1])

    # ASP - Complete
    elif (programSuffix == ".lp"):
        identifersLP = set()
        with programFile as file:
            for line in file:
                # print(line, end="")
                if "%" in line:
                    continue
                pattern = r'^\w+\(.+,.+\).+$'  # Regular expression pattern
                if re.match(pattern, line):
                    var = line[0: (line.index("("))]
                    # print(var)
                    identifersLP.add(var)
                if "=" in line.split():
                    identifersLP.add(line.split()[line.split().index("=") - 1])
                if "{" in line:
                    identifersLP.add(line.split()[0][1:(line.index("("))])


    # C
    elif (programSuffix[-2:] == ".c"):
        identifiersC = set()
        with programFile as file:
            for line in file:
                # print(line, end="")
                if "=" in line:
                    lineList = line.split()
                    if ("=" in lineList):
                        equalIndex = lineList.index("=")
                        identifiersC.add(line.split()[equalIndex - 1])
    # Python
    elif (programSuffix == ".py"):
        identifersPY = set()
        with programFile as file:
            for line in file:
                if "def" in line:
                    identifersPY.add(line.split()[1])
                if "=" in line:
                    lineList = line.split()
                    if ("=" in lineList):
                        equalIndex = lineList.index("=")
                        identifersPY.add(line.split()[equalIndex - 1])
                if "with" in line:
                    identifersPY.add(line.split()[1])
                    identifersPY.add(line.split()[3])


    if (programSuffix == ".ml"):
        # identifiers.sort()
        identifiersList = list(identifiers)
        identifiersList.sort()
        writeList(identifiersList, summaryFile)
    elif (programSuffix == "clj"):
        identifiersList = list(identifiersCLJ)
        identifiersList.sort()
        writeList(identifiersList, summaryFile)
    elif (programSuffix == ".lp"):
        identifiersList = list(identifersLP)
        identifiersList.sort()
        writeList(identifiersList, summaryFile)
    elif (programSuffix[-2:] == ".c"):
        identifiersList = list(identifiersC)
        identifiersList.sort()
        writeList(identifiersList, summaryFile)
    elif (programSuffix == ".py"):
        identifersList = list(identifersPY)
        identifersList.sort()
        writeList(identifersList, summaryFile)


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

    createKeywordList(programName, summaryFile)

# Set Directory
# /Users/survive/Desktop/EEATO/23Fall/CSC 344/csc344
# fileDirectory = input("Enter the file directory: ")
fileDirectory = "/Users/survive/Desktop/EEATO/23Fall/CSC344/csc344"
os.chdir(fileDirectory)
# Go through each directory and print the amount of lines

# Go through each directory
for file in os.listdir(fileDirectory):
    os.chdir(fileDirectory)
    # Ignore Hidden Files
    if (os.fsdecode(file)[0] == "." or os.fsdecode(file) == "index.html"):
        continue
    else:
        fileName = os.fsdecode(file)
        print(os.path.join(fileDirectory, fileName))
    # Find the code text in each file and create an HTML file
    for program in os.listdir(fileName): # triees to access index.html as a directory in the csc344 folder
        programName = os.fsdecode(program)
        if (programName[0] == "s" or programName[0] == "."):
            continue
        else:
            test = fileDirectory + "/" + fileName
            os.chdir(fileDirectory + "/" + fileName)
            currentDirectory = (fileDirectory + "/" + fileName)

            summaryFile = open("summary_" + fileName + ".html", 'w')
            print(programName)

            # Do the HTML magic
            boilerplate(summaryFile, programName)
            summarize(summaryFile, programName, currentDirectory)

            # Close the file
            summaryFile.close()

os.chdir(fileDirectory)
index = open("index.html", "w")
createHTML(index)

# Email to Dan and Daisy
# email = input("Who would you like to send the tar file to: ")
# os.system("cd ..; tar czf csc344.tar.gz csc344 ")
# os.system("cd ..; echo 'Final project for CSC344' | mutt -s 'Project 5: Python' " + email + " -a ./csc344.tar.gz")
