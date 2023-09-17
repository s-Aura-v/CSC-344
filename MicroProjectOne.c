    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <stdbool.h>

    struct books {
        float price;
        char name[20];
    };

    int main() {

        //Ask the user for input
        int shelvesAmt;
        int slotsAmt;
        printf("Input the number of shelves and the number of slots in each shelf: ");
        scanf("%d %d", &shelvesAmt, &slotsAmt); 

        struct books ** pointerToBookShelf;
        
        bool validBookShelf = false;
        while (validBookShelf == false)
        if (shelvesAmt < 0 || slotsAmt < 0) {
            printf("Please input valid numbers: \n");
            printf("Input the number of shelves and the number of slots in each shelf: ");
            scanf("%d %d", &shelvesAmt, &slotsAmt); 
        } else {
            pointerToBookShelf = malloc(shelvesAmt * sizeof(struct books *));
            for (int i = 0; i < shelvesAmt; i++) {
                pointerToBookShelf[i] = malloc(slotsAmt * sizeof(struct books *));
            }
            validBookShelf = true;
        }
        
        char bookName[20];
        double price;
        int shelf;
        int slot;
        while (1) {
            printf("Please input where you would like to place the books by listing the <name>, <price>, <shelf>, <slot>: \nEnter -1 -1 -1 -1 to exit! ");
            scanf("%s %lf %d %d", bookName, &price, &shelf, &slot);

            //Place books in the bookshelf
            if (atoi(bookName) == -1 && price == -1 && shelf == -1 && slot == -1) {
                printf("Thank you for placing the books in the shelf!!\n");
                break;
            } else if (shelf >= shelvesAmt || slot >= slotsAmt || slot < -1 || shelf < -1) {
                printf("Enter a valid shelf position! \n ");
            } else {
            strcpy(pointerToBookShelf[shelf][slot].name, bookName);
            pointerToBookShelf[shelf][slot].price = price;
            }
        }

        //After they're done placing items, read them:

        while (1) {
            printf("Which book would you like to view? <shelf> <slot>: \nEnter -1 -1 to exit! ");
            scanf("%d %d", &shelf, &slot);

            if (shelf == -1 && slot == -1) {
                printf("Thank you for visting the library!\n");
                break;
            } else if (shelf >= shelvesAmt && slot >= slotsAmt) {
                printf("Please enter a valid shelf position: \n");
            } else if (strcmp(pointerToBookShelf[shelf][slot].name,"") == 0)  {
                printf("Invalid! No books added at this position!");
            } else { 
                printf("Book name: %s\nPrice: %f\n", pointerToBookShelf[shelf][slot].name, pointerToBookShelf[shelf][slot].price);
            }
        }

        //free memory
        for (int i = 0; i < shelvesAmt; i++) {
            free(pointerToBookShelf[i]);
        }
        free(pointerToBookShelf);
        return 0;
    }
