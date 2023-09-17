//
// Created by Saurav Lamichhane on 9/10/23.
//
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Tape {
    char *initial;
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

int main() {
    //Read the input file
    FILE *fp;
    fp = fopen("input_test_1.txt", "r"); //r = file is created for reading



    
    fclose(fp);
    return 0;
}