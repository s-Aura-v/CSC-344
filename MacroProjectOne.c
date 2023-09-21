//
// Created by Saurav Lamichhane on 9/10/23.
//
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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


int main() {
    //Initialize the head
    head = createNewCell('A');
    


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

void addNext(char charValue) {
    //Create a temporary variable so we don't edit the main head
    struct TapeCell* temp = head;
    struct TapeCell* newCell = createNewCell(charValue);
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = newCell;
    newCell->prev = temp;
}


