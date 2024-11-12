%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>  // For strdup()

void yyerror(const char *s);  // Error handling
int yylex(void);

int sym[26];  // Symbol table for variables 'a' to 'z'
%}

/* Define YYSTYPE union to handle both int and string */
%union {
    int val;    // For numbers and identifiers
    char *str;  // For string literals
}

/* Declare token types and associate them with types from the %union */
%token <val> IF ELSE WHILE FOR PRINTF NUMBER IDENTIFIER
%token <str> STRING
%token LPAREN RPAREN LBRACE RBRACE SEMICOLON

/* Associate types with non-terminals */
%type <val> stmt stmt_list expr

/* Declare precedence to resolve ambiguity */
%right '='
%left '+' '-'
%left '*' '/'

%%

stmt:
      IF LPAREN expr RPAREN LBRACE stmt_list RBRACE {
        printf("Evaluating if statement with condition %d\n", $3);
        if ($3) {
            printf("Condition is true, executing if block\n");
        } else {
            printf("Condition is false, skipping if block\n");
        }
      }
    | IF LPAREN expr RPAREN LBRACE stmt_list RBRACE ELSE LBRACE stmt_list RBRACE {
        printf("Evaluating if-else statement with condition %d\n", $3);
        if ($3) {
            printf("Condition is true, executing if block\n");
        } else {
            printf("Condition is false, executing else block\n");
        }
      }
    | PRINTF LPAREN STRING RPAREN SEMICOLON {
        printf("Executing printf: %s\n", $3);
        free($3);
      }
    | IDENTIFIER '=' expr SEMICOLON {
        sym[$1] = $3;
        printf("Assigned %d to variable %c\n", $3, $1 + 'a');
      }
    | expr SEMICOLON {
        printf("Evaluated expression result: %d\n", $1);
      }
    | SEMICOLON { printf("Empty statement\n"); }
    ;

stmt_list:
      stmt
    | stmt_list stmt
    ;

expr:
      expr '+' expr { $$ = $1 + $3; }
    | expr '-' expr { $$ = $1 - $3; }
    | expr '*' expr { $$ = $1 * $3; }
    | expr '/' expr { 
        if ($3 == 0) yyerror("division by zero");
        else $$ = $1 / $3; 
      }
    | NUMBER { $$ = $1; }
    | IDENTIFIER { $$ = sym[$1]; }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    printf("Enter your C-like statements:\n");
    return yyparse();
} 