#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define KEYWORDS 32
#define OPERATORS 12

const char *keywords[] = {
    "auto", "break", "case", "char", "const", "continue", "default", "do", "double",
    "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", "register",
    "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef",
    "union", "unsigned", "void", "volatile", "while"
};

const char *operators[] = {
    "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">="
};

const char *preProcessors[] = {
    "#include", "#define", "#undef", "#if", "#ifdef", "#ifndef", "#else", "#elif", "#endif", "#error", "#pragma"
};

int isWhiteSpace(char ch) {

    if(ch == ' ') {
        return 1;
    } else if(ch == '\t') {
        return 2;
    } else if(ch == '\n') {
        return 3;
    } else if(ch == '\r') {
        return 4;
    }

    return 0;
}

int isAlpha(char ch) {
    return (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z');
}

int isDigit(char ch) {
    return ch >= '0' && ch <= '9';
}

int isPunctuator(char ch) {
    return ch == ',' || ch == ';' || ch == '(' || ch == ')' || ch == '{' || ch == '}';
}

int isHeaderFile(const char *str) {
    if(str[0] == '<' && str[strlen(str)-1] == '>' && str[strlen(str)-2] == "h" && str[strlen(str)-3] == '.'){
        return 1;
    }
}

int isKeyword(const char *str) {
    for (int i = 0; i < KEYWORDS; i++) {
        if (strcmp(str, keywords[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

int isPreProcessor(const char *str) {
    for (int i = 0; i < 11; i++) {
        if (strcmp(str, preProcessors[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

int isOperator(const char *str) {
    for (int i = 0; i < OPERATORS; i++) {
        if (strcmp(str, operators[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

int isIdentifer(const char *str) {
    if(isAlpha(str[0]) || str[0] == '_') {
        for(int i = 1; i < strlen(str); i++) {
            if(!isAlpha(str[i]) && !isDigit(str[i]) && str[i] != '_') {
                return 0;
            }
        }
    }
    return 1;
}

void printBuffer(char* buffer, int i) {
    for(int j = 0; j < i; j++) {
        printf("%c", buffer[j]);
    }
    printf("\n");
}


void findInFile(const char* fileName) {
    FILE *file = fopen(fileName, "r");
    if(!file) {
        printf("\n\nUnable to open file\n\n");
        exit(EXIT_FAILURE);
    }

    char* buffer = (char*)malloc(256 * sizeof(char));
    int i = 0;
    int keywordCount = 0, operatorCount = 0, identifierCount = 0;

    char ch = fgetc(file);

    while(ch != EOF) {
        
        if(isWhiteSpace(ch) || isPunctuator(ch)) {

            int typeOfWS = isWhiteSpace(ch);

            if(typeOfWS) {
                switch (typeOfWS) {
                    case 1:
                        printf("Space\n");
                        break;
                    case 2:
                        printf("Tab\n");
                        break;
                    case 3:
                        printf("New Line\n");
                        break;
                    case 4:
                        printf("Carriage Return\n");
                        break;
                    default:
                        break;
                }
            }

            if(isPunctuator(ch)) {
                printf("Punctuator: %c\n", ch);
            }

            if(i > 0) {
                buffer[i] = '\0';

                if(isHeaderFile(buffer)) {
                    printf("Header File: %s\n", buffer);
                }
                else if(isPreProcessor(buffer)) {
                    printf("PreProcessor: %s\n", buffer);
                }
                else if(isKeyword(buffer)) {
                    keywordCount++;
                    printf("Keyword: %s\n", buffer);
                } else if(isOperator(buffer)) {
                    operatorCount++;
                    printf("Operator: %s\n", buffer);
                } else if(isIdentifer(buffer)) {
                    identifierCount++;
                    printf("Identifier: %s\n", buffer);
                }
                i = 0;
            }
            if(isPunctuator(ch) && ch != '_') {
                buffer[0] = ch;
                buffer[1] = '\0';
                if(isOperator(buffer)) {
                    operatorCount++;
                    printf("Operator: %s\n", buffer);
                }
            }
        } else {
            buffer[i++] = ch;
        }

        ch = fgetc(file);
    }

     if(i > 0) {
            buffer[i] = '\0';

            if(isHeaderFile(buffer)) {
                printf("Header File: %s\n", buffer);
            }
            else if(isPreProcessor(buffer)) {
                printf("PreProcessor: %s\n", buffer);
            }
            else if(isKeyword(buffer)) {
                keywordCount++;
                printf("Keyword: %s\n", buffer);
            } else if(isOperator(buffer)) {
                operatorCount++;
                printf("Operator: %s\n", buffer);
            } else if(isIdentifer(buffer)) {
                identifierCount++;
                printf("Identifier: %s\n", buffer);
            }
        }

        

    printf("\n\nKeywords: %d\nOperators: %d\nIdentifiers: %d\n\n", keywordCount, operatorCount, identifierCount);
    printf("\n\nTotal Tokens: %d\n\n", operatorCount+identifierCount+keywordCount);
}

int main() {
    findInFile("sample.c");
    return 0;
}