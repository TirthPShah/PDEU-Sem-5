#include <stdio.h>
#include <string.h>

#define true 1
#define false 0

char input[100];
const char *lookahead;
char output[200];
char *outputPtr;

void removeLeftRecursion() {

    if (*lookahead == '\0') {
        return;
    }

    if (*lookahead == ';') {
        lookahead++;
    }

    char currNT = *lookahead;  // The current non-terminal
    *outputPtr = currNT;
    outputPtr++;

    lookahead++; // Move past the non-terminal

    // Skip any spaces or tabs
    while (*lookahead == ' ' || *lookahead == '\t') {
        lookahead++;
    }

    *outputPtr = ' ';
    outputPtr++;

    if (*lookahead == '-' && *(lookahead + 1) == '>') {
        lookahead += 2;
    }

    *outputPtr = '-';
    outputPtr++;
    *outputPtr = '>';
    outputPtr++;

    // Skip any spaces or tabs
    while (*lookahead == ' ' || *lookahead == '\t') {
        lookahead++;
    }

    *outputPtr = ' ';
    outputPtr++;

    // If the rule does not have left recursion, copy it as is
    if (*lookahead != currNT) {
        
        while (*lookahead != ';' && *lookahead != '\0' && *lookahead != '|' && *lookahead != '\n') {
            *outputPtr = *lookahead;
            outputPtr++;
            lookahead++;
        }

        while(*lookahead == '|') {
            
        }




    } 
    
    else {
        printf("Left recursion detected for %c\n", currNT);
        return;
        // Add your logic to handle left recursion here
    }

    if (*lookahead == '|') {
        lookahead++; // Move past the '|'
    }
}

int main() {

    printf("Enter the input string: ");
    scanf(" %[^\n]", input);  // Read input with spaces
    lookahead = input;
    outputPtr = output;

    while (*lookahead != '\0') {
        removeLeftRecursion();
    }

    *outputPtr = '\0';  // Null-terminate the output string

    printf("The final grammar is: \n%s\n", output);

    return 0;
}
