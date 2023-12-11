# Write a Python program that collects, summarizes, and e-mails all the programming assignments for this course.
import os
import re


def createHTML(index):
    index.write("<!DOCTYPE html>\n"
                "<html lang=\"en\">\n"
                "<head>\n"
                "<link rel='stylesheet' href='mystyle.css'>"
                "<title> Summary of CSC344 Fall 2023 </title>\n"
                "</head>\n\n")

    index.write("<body"
                "<h2> All of the programming challenges: </h2>\n"
                "<ol>\n"
                "<li> C Program: </li>" + "<a href=./a1/summary_a1.html> TuringMachine.c </a>\n" 
                "<li> Clojure Program: </li>" + "<a href=./a2/summary_a2.html> InferenceSys.clj</a>\n"
                "<li> OCaml Program: </li>" + "<a href=./a3/summary_a3.html> PatternMatching.ml</a>\n"
                "<li> ASP Program: </li>" + "<a href=./a4/summary_a4.html> DistancingSim.lp</a>\n"
                "<li> Python Program: </li>" + "<a href=./a5/summary_a5.html> SummaryOfCSC344.py</a>\n"
                "</body")


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
    identifiers = set()
    foundKeyWord = False
    if (programSuffix == "clj"):
        with programFile as file:
            for line in file:
                if ";;" in line:
                    continue
                if "defn" in line:
                    identifiers.add(line.split()[1])
                if "let" in line or "for" in line:
                    identifiers.add(line.split()[1][1:])
                if "[" in line:
                    if line.split()[0][0] == "[":
                        if len(line.split()) == 1:
                            identifiers.add(line.split()[0][1: len(line.split()[0]) - 1])
                        if len(line.split()) > 1:
                            identifiers.add(line.split()[0][1:])
                            identifiers.add(line.split()[1][0: line.split()[1].index("]")])
                if ("[" in line and "]" not in line):
                    identifiers.add(line.split()[1][1:])
                    identifiers.add(line.split()[2][2:6])
                if ("]" in line and "[" not in line):
                    identifiers.add(line.split()[0])
                    identifiers.add(line.split()[1][0:5])


    # Complete - sorted not working properly
    elif (programSuffix == ".ml"):
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
                if "=" in line.split():
                    if "rec" in line:
                        if "()" in line.split():
                            for item in line.split()[2:line.split().index("()")]:
                                identifiers.add(item)
                        else:
                            for item in line.split()[2:line.split().index("=")]:
                                identifiers.add(item)
                if "let" in line.split():
                    if "rec" in line:
                        if "()" in line.split():
                            for item in line.split()[2:line.split().index("()")]:
                                identifiers.add(item)
                        else:
                            for item in line.split()[2:line.split().index("=")]:
                                identifiers.add(item)
                    else:
                        if "()" in line.split():
                            for item in line.split()[1:line.split().index("()")]:
                                # print(line.split()[1:line.split().index("()")])
                                if item != "=":
                                    identifiers.add(item)
                        else:
                            for item in line.split()[1:line.split().index("=")]:
                                # print(item)
                                if "=" not in item:
                                    identifiers.add(item)
                        identifiers.add(line.split()[1])
                # Grab the alphabet
                if "|" in line.split():
                    if "(h::t)" in line.split():
                        identifiers.add(line.split()[1][1])
                        identifiers.add(line.split()[1][4])
                    else:
                        identifiers.add(line.split()[line.split().index("|") + 1])

    # ASP - Complete
    elif (programSuffix == ".lp"):
        with programFile as file:
            for line in file:
                # print(line, end="")
                if "%" in line:
                    continue
                # Find pattern text(text,text)text
                pattern = r'^\w+\(.+,.+\).+$'
                if re.match(pattern, line):
                    var = line[0: (line.index("("))]
                    # print(var)
                    identifiers.add(var)
                if "=" in line.split():
                    identifiers.add(line.split()[line.split().index("=") - 1])
                if "{" in line:
                    identifiers.add(line.split()[0][1:(line.index("("))])

    # C - Complete
    elif (programSuffix[-2:] == ".c"):
        with programFile as file:
            for line in file:
                # print(line, end="")
                if "//" in line:
                    if "Global" in line:
                        pass
                    else:
                        continue
                if "=" in line.split():
                    equalIndex = line.split().index("=")
                    if "*" not in line and "->" not in line and "." not in line:
                        identifiers.add(line.split()[equalIndex - 1])
                        # print(line.split()[equalIndex - 1])
                    elif "->" in line:
                        for item in line.split():
                            if "->" in item:
                                # print (item)
                                if ";" in item:
                                    if "]" in item:
                                        pass
                                    else:
                                        # print((item[item.index(">") + 1: item.index(";")]))
                                        identifiers.add(item[item.index(">") + 1: item.index(";")])
                                else:
                                    # print((item[item.index(">") + 1:]))
                                    identifiers.add(item[item.index(">") + 1:])

                if "void" in line.split():
                    identifiers.add(line.split()[1][0:line.split()[1].index("(")])
                if "//Global" in line:
                    foundKeyWord = True
                if "main" in line:
                    foundKeyWord = False
                if foundKeyWord:
                    if len(line.split()) == 0:
                        pass
                    elif "struct" in line:
                        if ";" in line.split()[2]:
                            identifiers.add(line.split()[2][0: line.split()[2].index(";")])
                        elif "(" in line.split()[2]:
                            identifiers.add(line.split()[2][0: line.split()[2].index("(")])
                    else:
                        if "(" in line.split()[1]:
                            identifiers.add(line.split()[1][0: line.split()[1].index("(")])
                        else:
                            identifiers.add(line.split()[1])


    # Python - complete
    elif (programSuffix == ".py"):
        with programFile as file:
            for line in file:
                if "#" in line:
                    continue
                if "def" in line.split():
                    if "(" in line:
                        identifiers.add(line.split()[1][0: line.split()[1].index("(")])
                    else:
                        identifiers.add(line.split()[1])
                if "=" in line:
                    lineList = line.split()
                    if ("=" in lineList):
                        equalIndex = lineList.index("=")
                        identifiers.add(line.split()[equalIndex - 1])
                if "with" in line.split() or "for" in line.split():
                    if "." in line:
                        continue
                    elif ":" in line:
                        identifiers.add(line.split()[1])
                        identifiers.add(line.split()[3][0: line.split()[3].index(":")])
                    else:
                        identifiers.add(line.split()[1])
                        identifiers.add(line.split()[3])

    identifiersList = list(identifiers)
    identifiersList.sort()
    writeList(identifiersList, summaryFile)
    identifiersList.clear()


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
# /home/slamich2/CSC344/python_Proj2/csc344
fileDirectory = input("Enter the file directory: ")
# fileDirectory = "/Users/survive/Desktop/EEATO/23Fall/CSC344/csc344"
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
index.close()

# Email to Dan and Daisy
email = input("Who would you like to send the tar file to: ")
os.chdir('..')
os.system("tar -czf csc344.tar.gz csc344")
os.system("echo 'Final project for CSC344' | mutt -s 'Project 5: Python' " + email + " -a './csc344.tar.gz'")# Write a Python program that collects, summarizes, and e-mails all the programming assignments for this course.
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
    identifiers = set()
    if (programSuffix == "clj"):
        with programFile as file:
            for line in file:
                if ";;" in line:
                    continue
                if "defn" in line:
                    identifiers.add(line.split()[1])
                if "let" in line or "for" in line:
                    identifiers.add(line.split()[1][1:])
                if "[" in line:
                    if line.split()[0][0] == "[":
                        if len(line.split()) == 1:
                            identifiers.add(line.split()[0][1: len(line.split()[0]) - 1])
                        if len(line.split()) > 1:
                            identifiers.add(line.split()[0][1:])
                            identifiers.add(line.split()[1][0: line.split()[1].index("]")])
                if ("[" in line and "]" not in line):
                    identifiers.add(line.split()[1][1:])
                    identifiers.add(line.split()[2][2:6])
                if ("]" in line and "[" not in line):
                    identifiers.add(line.split()[0])
                    identifiers.add(line.split()[1][0:5])


    # Mostly works: Remove =
    elif (programSuffix == ".ml"):
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
                if "=" in line.split():
                    if "rec" in line:
                        if "()" in line.split():
                            for item in line.split()[2:line.split().index("()")]:
                                identifiers.add(item)
                        else:
                            for item in line.split()[2:line.split().index("=")]:
                                identifiers.add(item)
                if "let" in line.split():
                    if "rec" in line:
                        if "()" in line.split():
                            for item in line.split()[2:line.split().index("()")]:
                                identifiers.add(item)
                        else:
                            for item in line.split()[2:line.split().index("=")]:
                                identifiers.add(item)
                    else:
                        if "()" in line.split():
                            for item in line.split()[1:line.split().index("()")]:
                                # print(line.split()[1:line.split().index("()")])
                                identifiers.add(item)
                        else:
                            for item in line.split()[1:line.split().index("=")]:
                                # print(item)
                                if "=" not in item:
                                    identifiers.add(item)
                        identifiers.add(line.split()[1])
                # Grab the alphabet
                if "|" in line.split():
                    if "(h::t)" in line.split():
                        identifiers.add(line.split()[1][1])
                        identifiers.add(line.split()[1][4])
                    else:
                        identifiers.add(line.split()[line.split().index("|") + 1])

    # ASP - Complete
    elif (programSuffix == ".lp"):
        with programFile as file:
            for line in file:
                # print(line, end="")
                if "%" in line:
                    continue
                # Find pattern text(text,text)text
                pattern = r'^\w+\(.+,.+\).+$'
                if re.match(pattern, line):
                    var = line[0: (line.index("("))]
                    # print(var)
                    identifiers.add(var)
                if "=" in line.split():
                    identifiers.add(line.split()[line.split().index("=") - 1])
                if "{" in line:
                    identifiers.add(line.split()[0][1:(line.index("("))])

    # C
    elif (programSuffix[-2:] == ".c"):
        with programFile as file:
            for line in file:
                # print(line, end="")
                if "//" in line:
                    if "global" in line:
                        pass
                    else:
                        continue
                if "=" in line.split():
                    equalIndex = line.split().index("=")
                    if "*" not in line and "->" not in line and "." not in line:
                        identifiers.add(line.split()[equalIndex - 1])
                        # print(line.split()[equalIndex - 1])
                if "void" in line.split():
                    identifiers.add(line.split()[1][0:line.split()[1].index("(")])
                # if "global" in line:
                #     functions = True;
                # if functions:
                #     if "struct" in line:
                #         print(line.split().index()[2])


    # Python
    elif (programSuffix == ".py"):
        with programFile as file:
            for line in file:
                if "#" in line:
                    continue
                if "def" in line.split():
                    if "(" in line:
                        identifiers.add(line.split()[1][0: line.split()[1].index("(")])
                    else:
                        identifiers.add(line.split()[1])
                if "=" in line:
                    lineList = line.split()
                    if ("=" in lineList):
                        equalIndex = lineList.index("=")
                        identifiers.add(line.split()[equalIndex - 1])
                if "with" in line.split() or "for" in line.split():
                    if "." in line:
                        continue
                    elif ":" in line:
                        identifiers.add(line.split()[1])
                        identifiers.add(line.split()[3][0: line.split()[3].index(":")])
                    else:
                        identifiers.add(line.split()[1])
                        identifiers.add(line.split()[3])



    identifiersList = list(identifiers)
    identifiersList.sort()
    writeList(identifiersList, summaryFile)
    identifiersList.clear()


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
email = input("Who would you like to send the tar file to: ")
os.system("cd ..; tar czf csc344.tar.gz csc344 ")
os.system("cd ..; echo 'Final project for CSC344' | mutt -s 'Project 5: Python' " + email + " -a ./csc344.tar.gz")
