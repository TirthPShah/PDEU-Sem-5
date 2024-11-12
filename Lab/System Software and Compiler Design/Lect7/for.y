%token FOR LPAREN RPAREN LBRACE RBRACE SEMICOLON IDENTIFIER NUMBER ASSIGN PLUS PLUS MINUS MINUS LT GT LE GE EQ NE
%left '='

%{

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);  // Match definition
int yylex(void);

int sym[70];  // Symbol table for variables

%}

%%

program:
    program statement
    |
    ;

statement:
    for_loop
    ;

for_loop:
    FOR LPAREN init SEMICOLON condition SEMICOLON increment RPAREN LBRACE program RBRACE {
        printf("Initializing for-loop with variable at index %d, value %d\n", $3, sym[$3]);
        // Run the loop with proper condition and increment
        for (; $5; sym[$3] += $7) {  // Update loop variable
            printf("Running for-loop iteration with i = %d\n", sym[$3]);
            yyparse();  // Process statements inside the loop body
        }
    }
    ;

init:
    IDENTIFIER ASSIGN NUMBER {
        sym[$1] = $3;  // Initialize variable in symbol table
        $$ = $1;  // Pass the identifier index (for loop variable)
    }
    ;

condition:
    IDENTIFIER LT NUMBER { 
        printf("Condition: %d < %d\n", sym[$1], $3);  // Debug output
        $$ = sym[$1] < $3;  // Evaluate condition
    }
    | IDENTIFIER GT NUMBER { 
        printf("Condition: %d > %d\n", sym[$1], $3);
        $$ = sym[$1] > $3;
    }
    | IDENTIFIER LE NUMBER { 
        printf("Condition: %d <= %d\n", sym[$1], $3);
        $$ = sym[$1] <= $3;
    }
    | IDENTIFIER GE NUMBER { 
        printf("Condition: %d >= %d\n", sym[$1], $3);
        $$ = sym[$1] >= $3;
    }
    | IDENTIFIER EQ NUMBER { 
        printf("Condition: %d == %d\n", sym[$1], $3);
        $$ = sym[$1] == $3;
    }
    | IDENTIFIER NE NUMBER { 
        printf("Condition: %d != %d\n", sym[$1], $3);
        $$ = sym[$1] != $3;
    }
    ;

increment:
    IDENTIFIER PLUS PLUS {
        printf("Incrementing %d\n", sym[$1]);
        $$ = 1;  // Return increment value
    }
    | IDENTIFIER MINUS MINUS {
        printf("Decrementing %d\n", sym[$1]);
        $$ = -1;  // Return decrement value
    }
    ;

%%

// Error handling
void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    printf("Enter a for loop (e.g., for (i = 0; i < 10; i++) { ... }):\n");
    yyparse();
    return 0;
}
