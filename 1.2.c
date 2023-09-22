//
// Created by Saurav Lamichhane on 9/10/23.
//
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LINE 2048


struct TapeCell {
    char data;
    struct TapeCell* prev;
    struct TapeCell* next;
};

struct Instruction {
    int currentState;
    char moveDirection; // 'L' for left, 'R' for right
    int newState;
    char readValue;
    char writeValue;
};

//Global variables
struct TapeCell* head = NULL;
struct Instruction** instructionTable;

//Functions
struct TapeCell* createNewCell(char charValue);
struct TapeCell* createBlankCell(struct TapeCell* tempCell);
void addNext(char charValue);
void initializeTable(char* input);
void finalTape();


int main() {
    //Initialize the head
    head = createNewCell('A');

    //Read for file name
    char fileName[] = "input.txt";
//    printf("Input the name of the file: ");
//    scanf("%s", fileName);

    //Read the file and add it into an array
    FILE *fp;
    fp = fopen(fileName, "r"); //r = file is created for reading
    char *line;
    line = malloc(sizeof(char *) * 100);
    (fgets(line, sizeof(line), fp) != NULL);      // f(gets): store, size, inputFile

    // Create the tape
    for (int i = 0; i < strlen(line) + 1; i++) {
        addNext(line[i]);
    }

    struct TapeCell *temp = head;
    printf("Initial Tape: ");
    while (temp->next != NULL) {
        printf("%c", temp->data);
        temp = temp->next;
    }
    printf("\n");


    //Instruction Setup
    int numOfStates; //initialize it based on input
    int startState;
    int endState;
    char numTest[100];

    //Go through the files lines, set each variable to proper line
    char buffer[MAX_LINE];
    bool keepReading = true;
    int currentLine = 0;

    //Insert value to variables
    do {
        fgets(buffer, 20, fp); //add the text to, max line for array, file
        if (feof(fp)) {
            keepReading = false;
        } else if (currentLine == 1) {
            numOfStates = atoi(buffer); //cpy buffer to
            instructionTable = (struct Instruction **) malloc(numOfStates * sizeof(struct Instruction **));
            for (int i = 0; i < numOfStates; i++) {
                instructionTable[i] = malloc(128 * sizeof(struct Instruction *));
            }
        } else if (currentLine == 2) {
            startState = atoi(buffer);
        } else if (currentLine == 3) {
            endState = atoi(buffer);
        } else if (currentLine > 3) {
            char *input = buffer;
            initializeTable(input);
        }
        currentLine++;
    } while (keepReading);
    fclose(fp);

    //tests
    printf("Line i: %c", line[0]);


    //Start read and write
    struct TapeCell *tempCell = head;
    int tempState = startState;
    while (startState != endState) {
        //get the value from the instruction table
        struct Instruction tempInstruct = instructionTable[tempState][tempCell->data];
        tempCell->data = tempInstruct.writeValue;
        if (tempInstruct.moveDirection == 'R') {
            if (tempCell->next != NULL) {
                tempCell = tempCell->next;
            } else {
                tempCell = createBlankCell(tempCell);
            }

        } else if (tempInstruct.moveDirection == 'L') {
            tempCell = tempCell->prev;
        }
        tempState = tempInstruct.newState;
    }



    //Output:
    finalTape();
    //End of program
    return 0;

}


struct TapeCell* createNewCell(char charValue) {
    struct TapeCell* newCell = (struct TapeCell*) malloc(sizeof (struct TapeCell));
    newCell->data = charValue;
    newCell->prev = NULL;
    newCell->next = NULL;
    return newCell;
}

struct TapeCell* createBlankCell(struct TapeCell* tempCell) {
    struct TapeCell* newCell = (struct TapeCell*) malloc(sizeof (struct TapeCell));
    newCell->data = 'B';
    newCell->prev = tempCell;
    newCell->next = NULL;
    return newCell;

}

void addNext(char charValue) {
    //Create a temporary variable
    struct TapeCell* temp = head;
    struct TapeCell* newCell = createNewCell(charValue);
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = newCell;
    newCell->prev = temp;
}

void initializeTable(char* input) {
    //Go through every line on the file and add it to the table
    //Separate the line by ->

    //Copied the instructions
    int currentState = input[1] - 48;  //48 is the value of 0 so get the int by subtracting it by 48
    char readValue = input[3];
    char writeValue = input[8];
    char moveDirection = input[10];
    int newState = input[12];

    instructionTable[currentState][readValue].currentState = currentState;
    instructionTable[currentState][readValue].readValue = readValue;
    instructionTable[currentState][readValue].moveDirection = moveDirection;
    instructionTable[currentState][readValue].writeValue = writeValue;
    instructionTable[currentState][readValue].newState = newState;
}

void finalTape() {
    struct TapeCell* temp = head;
    printf("Final Tape: ");
    while (temp->next != NULL) {
        printf("%c", temp->data);
        temp = temp->next;
    }
}