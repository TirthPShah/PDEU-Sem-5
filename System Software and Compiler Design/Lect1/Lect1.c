#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_KEYWORDS 32
#define MAX_OPERATORS 12

const char *keywords[MAX_KEYWORDS] = {
    "auto", "break", "case", "char", "const", "continue", "default", "do", "double",
    "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", "register",
    "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef",
    "union", "unsigned", "void", "volatile", "while"
};

const char *operators[MAX_OPERATORS] = {
    "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">="
};

int isKeyword(const char *str) {
    for (int i = 0; i < MAX_KEYWORDS; i++) {
        if (strcmp(str, keywords[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

int isOperator(const char *str) {
    for (int i = 0; i < MAX_OPERATORS; i++) {
        if (strcmp(str, operators[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

int isIdentifier(const char *str) {
    if (isalpha(str[0]) || str[0] == '_') {
        for (int i = 1; str[i] != '\0'; i++) {
            if (!isalnum(str[i]) && str[i] != '_') {
                return 0;
            }
        }
        return 1;
    }
    return 0;
}

void tokenizeFile(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Unable to open file");
        exit(EXIT_FAILURE);
    }

    char ch, buffer[256];
    int i = 0;
    int keywordCount = 0, operatorCount = 0, identifierCount = 0;

    while ((ch = fgetc(file)) != EOF) {
        if (isspace(ch) || ispunct(ch)) {
            if (i > 0) {
                buffer[i] = '\0';
                if (isKeyword(buffer)) {
                    keywordCount++;
                } else if (isOperator(buffer)) {
                    operatorCount++;
                } else if (isIdentifier(buffer)) {
                    identifierCount++;
                }
                i = 0;
            }
            if (ispunct(ch) && ch != '_') {
                buffer[0] = ch;
                buffer[1] = '\0';
                if (isOperator(buffer)) {
                    operatorCount++;
                }
            }
        } else {
            buffer[i++] = ch;
        }
    }

    fclose(file);

    printf("Keywords: %d\n", keywordCount);
    printf("Identifiers: %d\n", identifierCount);
    printf("Operators: %d\n", operatorCount);
}

int main() {
    const char *filename = "sample.c";
    tokenizeFile(filename);
    return 0;
}
