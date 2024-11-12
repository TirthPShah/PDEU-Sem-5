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

char input[400];

// Function to give tuple from input instruction
char* getTuple(char *instruction) {
    char *tuple = (char *)malloc(20);
    char buffer[10];
    int i = 0, j = 0;

    // Skip initial spaces if any
    while (instruction[i] == ' ') i++;

    // Extract mnemonic or keyword
    while (instruction[i] != ' ' && instruction[i] != '\0' && j < sizeof(buffer) - 1) {
        buffer[j++] = instruction[i++];
    }
    buffer[j] = '\0';

    // Initialize tuple format
    strcpy(tuple, "(");

    // Search for mnemonic in the MOTable
    for (int k = 0; k < sizeof(moTable) / sizeof(moTable[0]); k++) {
        if (strcmp(moTable[k].mnemonic, buffer) == 0) {
            strcat(tuple, moTable[k].class);
            strcat(tuple, ",");
            strcat(tuple, moTable[k].opcode);
            strcat(tuple, ")");
            return tuple;
        }
    }

    // If mnemonic not found
    strcpy(tuple, "(NA,NA)");
    return tuple;
}

int main() {
    // Read input from input.asm
    FILE *file = fopen("input.asm", "r");
    if (!file) {
        printf("Error opening file.\n");
        return 1;
    }
    
    char line[100];

    // Read each line, get the tuple, and print it
    while (fgets(line, sizeof(line), file)) {
        // Remove the newline character at the end if it exists
        size_t len = strlen(line);
        if (len > 0 && line[len - 1] == '\n') {
            line[len - 1] = '\0';
        }
        
        char *tuple = getTuple(line);
        printf("%-20s %s\n", line, tuple);  // Print line without the trailing newline and the tuple
        free(tuple);
    }


    fclose(file);
    return 0;
}
