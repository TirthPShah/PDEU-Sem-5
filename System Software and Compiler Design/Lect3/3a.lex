/*
Lex file to remove comments from a C program
*/

%{
#include<stdio.h>
FILE *output;
%}

%%
"//"[^\n]* 
"/*"(.|\n|\t)*"*/"
[ \n\t] {printf("");}
.|\n|\t {fprintf(output, "%s", yytext);}
%%

int yywrap() {
    return 1;
}

int main(int argc, char **argv)
{
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            perror(argv[1]);
            return 1;
        }
        yyin = file;
    }

    output = fopen("./input.c", "w");
    if (!output) {
        perror("input.c");
        return 1;
    }
    yyout = output;

    yylex();

    fclose(output);
    return 0;
}