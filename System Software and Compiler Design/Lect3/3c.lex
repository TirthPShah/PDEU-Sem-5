/*
Lex file to remove HTML Tags and SQL commands from a file
*/

%{
#include<stdio.h>
%}

%%
"<"[^>]*">"[^</]*"</"[^>]*">" {printf("HTML Tag: %s", yytext);}
"SELECT"|"INSERT"|"UPDATE"|"DELETE"|"FROM"[^\n]* {printf("SQL Comm: %s", yytext);}
. {printf("%s", yytext);}
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

    yylex();
    return 0;
}