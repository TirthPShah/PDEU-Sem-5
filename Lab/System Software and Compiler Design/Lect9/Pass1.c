#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct MOTableEntry {
    char mnemonic[10];
    char class[3];
    char opcode[3];
    int length;
};

struct MOTableEntry moTable[] = {
    {"STOP", "IS", "00", 1},
    {"ADD", "IS", "01", 1},
    {"SUB", "IS", "02", 1},
    {"MULTI", "IS", "03", 1},
    {"MOVER", "IS", "04", 1},
    {"MOVEM", "IS", "05", 1},
    {"COMP", "IS", "06", 1},
    {"BC", "IS", "07", 1},
    {"DIV", "IS", "08", 1},
    {"READ", "IS", "09", 1},
    {"PRINT", "IS", "10", 1},
    {"START", "AD", "01", 1},
    {"END", "AD", "02", 1},
    {"ORIGIN", "AD", "03", 1},
    {"EQU", "AD", "04", 1},
    {"LTORG", "AD", "05", 1},
    {"DS", "DL", "01", 1},
    {"DC", "DL", "02", 1},
    {"AREG", "RG", "01", 1},
    {"BREG", "RG", "02", 1},
    {"CREG", "RG", "03", 1},
    {"EQ", "CC", "01", 1},
    {"LT", "CC", "02", 1},
    {"GT", "CC", "03", 1},
    {"LE", "CC", "04", 1},
    {"GE", "CC", "05", 1},
    {"NE", "CC", "06", 1}
};

// Function to give tuple from input instruction
char* getTuple(char *instruction) {
    char *tuple = (char *)malloc(100);  // Allocate more space for multiple tuples
    tuple[0] = '\0';  // Initialize as an empty string
    
    char buffer[10];
    char *token = strtok(instruction, " ,");  // Split by spaces and commas
    int isFirstToken = 1;  // Track if we're on the mnemonic

    while (token != NULL) {
        strcpy(buffer, token);

        // Look up the token in the MOTable
        int found = 0;
        for (int k = 0; k < sizeof(moTable) / sizeof(moTable[0]); k++) {
            if (strcmp(moTable[k].mnemonic, buffer) == 0) {
                // Append tuple for the mnemonic or register
                strcat(tuple, "(");
                strcat(tuple, moTable[k].class);
                strcat(tuple, ",");
                strcat(tuple, moTable[k].opcode);
                strcat(tuple, ") ");
                found = 1;
                break;
            }
        }
        
        if (!found) {
            if (buffer[0] == '=') {  // Handle literals (e.g., ='5')
                strcat(tuple, "(LIT,");
                strcat(tuple, buffer + 2);  // Skip "='"
                tuple[strlen(tuple) - 1] = ')';  // Replace the trailing quote with a parenthesis
                strcat(tuple, " ");
            } else {
                strcat(tuple, "(SYM,");
                strcat(tuple, buffer);
                strcat(tuple, ") ");
            }
        }

        // Move to the next token
        token = strtok(NULL, " ,");
    }

    // Remove the trailing space
    size_t len = strlen(tuple);
    if (len > 0 && tuple[len - 1] == ' ') {
        tuple[len - 1] = '\0';
    }

    return tuple;
}

int main() {
    // Open input.asm file for reading
    FILE *file = fopen("input.asm", "r");
    if (file == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    char line[100];
    while (fgets(line, sizeof(line), file)) {
        // Remove newline character from the line
        line[strcspn(line, "\n")] = '\0';

        // Get tuple for the line
        char *tuple = getTuple(line);
        
        // Print the original line with the tuple
        printf("%-30s %s\n", line, tuple);

        free(tuple);  // Free the allocated tuple memory
    }

    // Close the file
    fclose(file);

    return 0;
}
