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
     char readValue;
     char writeValue;
     char moveDirection; // 'L' for left, 'R' for right
     int newState;
};

//Global variables
struct TapeCell* head = NULL;

//Functions
struct TapeCell* createNewCell(char charValue);
void addNext(char charValue);
void initializeTable(char* input, struct Instruction** instructionTable);


int main() {
    //Initialize the head
    head = createNewCell('A');

    //Read for file name
    char fileName[20];
    printf("Input the name of the file: ");
    scanf("%s", fileName);

    //Read the file and add it into an array
    FILE *fp;
    fp = fopen(fileName, "r");
    char *line;
    line = malloc(sizeof (char * ) * 100);      //idk the size of the file
    (fgets(line, sizeof(line), fp) != NULL);      // f(gets): store, size, inputFile

//    Create the tape
    for (int i = 0; i < strlen(line); i++) {
        printf("%c", line[i]);
        addNext(line[i]);
    }
    for (int i = 0; i < 9; i++) {
        printf("%c", head[i].data);
    }

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
    struct Instruction** instructionTable;
    do
    {
        fgets(buffer, 20, fp); //add the text to, max line for array, file
        if (feof(fp)) {
            keepReading = false;
        }
        else if (currentLine == 1) {
            numOfStates = atoi(buffer); //cpy buffer to
        }
        else if (currentLine == 2) {
            startState = atoi(buffer);
        }
        else if (currentLine == 3) {
            endState = atoi(buffer);
        }
        else if (currentLine > 3) {
            char * input = buffer;
            printf("%s", input);
            initializeTable(input, instructionTable);
        }
        currentLine++;
    } while (keepReading);

    printf("%d %d %d ",numOfStates, startState, endState);
    fclose(fp);

    //Create the 2d array of instructions

    //End of program
    free(line);
    return 0;

}


struct TapeCell* createNewCell(char charValue) {
    struct TapeCell* newCell = (struct TapeCell*) malloc(sizeof (struct TapeCell));
    newCell->data = charValue;
    newCell->prev = NULL;
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


void initializeTable(char* input, struct Instruction** instructionTable) {
    //Go through every line on the file and add it to the table
    //Separate the line by ->

    //Copied the instructions
    char x = input[1];
    char y = input[3];
    char moveDirection = input[10];
    int currentState = input[8];
    int newState = input[12];

    instructionTable[x][y].currentState = currentState;
    instructionTable[x][y].moveDirection = moveDirection;
    instructionTable[x][y].newState = newState;


    printf("x:%d - y:%d - cS:%d - nS:%d\n", x, y, currentState, newState);

}

