#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_EXPRESSIONS 100
#define MAX_LENGTH 100

typedef struct {
    char left[10];
    char right[MAX_LENGTH];
} Expression;

Expression expressions[MAX_EXPRESSIONS];
int expr_count = 0;

int is_number(const char *str) {
    for (int i = 0; str[i] != '\0'; i++) {
        if (!isdigit(str[i])) return 0;
    }
    return 1;
}

void constant_folding(char *expr) {
    char *token, *saveptr;
    char temp[MAX_LENGTH] = "";
    int result = 0;
    int first = 1;

    token = strtok_r(expr, "+", &saveptr);
    while (token != NULL) {
        while (*token == ' ') token++;  // Trim leading spaces
        char *end = token + strlen(token) - 1;
        while (end > token && *end == ' ') end--;  // Trim trailing spaces
        *(end + 1) = '\0';

        if (is_number(token)) {
            result += atoi(token);
        } else {
            if (!first) strcat(temp, "+ ");
            strcat(temp, token);
            strcat(temp, " ");
            first = 0;
        }
        token = strtok_r(NULL, "+", &saveptr);
    }

    if (result > 0) {
        char res_str[20];
        sprintf(res_str, "%d + ", result);
        strcpy(expr, res_str);
        strcat(expr, temp);
    } else {
        strcpy(expr, temp);
    }

    // Remove trailing space
    int len = strlen(expr);
    if (len > 0 && expr[len-1] == ' ') {
        expr[len-1] = '\0';
    }
}

int optimize_expressions() {
    int changed = 0;
    
    // Perform constant folding
    for (int i = 0; i < expr_count; i++) {
        char old_expr[MAX_LENGTH];
        strcpy(old_expr, expressions[i].right);
        constant_folding(expressions[i].right);
        if (strcmp(old_expr, expressions[i].right) != 0) {
            changed = 1;
        }
    }
    
    // Perform common subexpression elimination
    for (int i = 0; i < expr_count; i++) {
        for (int j = 0; j < i; j++) {
            char *subexpr = strstr(expressions[i].right, expressions[j].right);
            if (subexpr) {
                char new_expr[MAX_LENGTH];
                int prefix_len = subexpr - expressions[i].right;
                strncpy(new_expr, expressions[i].right, prefix_len);
                new_expr[prefix_len] = '\0';
                strcat(new_expr, expressions[j].left);
                strcat(new_expr, subexpr + strlen(expressions[j].right));
                
                if (strcmp(new_expr, expressions[i].right) != 0) {
                    strcpy(expressions[i].right, new_expr);
                    changed = 1;
                }
            }
        }
    }
    
    return changed;
}

int main() {
    char line[MAX_LENGTH];
    
    printf("Enter expressions (one per line, empty line to finish):\n");
    
    while (fgets(line, sizeof(line), stdin) && line[0] != '\n') {
        line[strcspn(line, "\n")] = 0;  // Remove newline
        
        char *equals = strchr(line, '=');
        if (equals == NULL) {
            printf("Invalid expression: %s\n", line);
            continue;
        }
        
        *equals = '\0';
        strcpy(expressions[expr_count].left, line);
        strcpy(expressions[expr_count].right, equals + 1);
        
        // Trim spaces
        char *end = expressions[expr_count].left + strlen(expressions[expr_count].left) - 1;
        while (end > expressions[expr_count].left && isspace((unsigned char)*end)) end--;
        end[1] = '\0';
        
        char *start = expressions[expr_count].right;
        while (*start && isspace((unsigned char)*start)) start++;
        strcpy(expressions[expr_count].right, start);
        
        expr_count++;
    }
    
    int iteration = 0;
    while (1) {
        int changed = optimize_expressions();
        if (!changed) break;
        iteration++;
    }
    
    printf("\nOptimized expressions after %d iterations:\n", iteration);
    for (int i = 0; i < expr_count; i++) {
        printf("%s = %s\n", expressions[i].left, expressions[i].right);
    }
    
    return 0;
}