%{
#include "y.tab.h"  // Include the Yacc header for token definitions
#include <stdio.h>
#include <stdlib.h>
#include <string.h>  // For strdup()

extern YYSTYPE yylval;
%}

%%
"if"        { return IF; }
"else"      { return ELSE; }
"while"     { return WHILE; }
"for"       { return FOR; }
"printf"    { return PRINTF; }
"("         { return LPAREN; }
")"         { return RPAREN; }
"{"         { return LBRACE; }
"}"         { return RBRACE; }
";"         { return SEMICOLON; }
"+"         { return '+'; }
"-"         { return '-'; }
"*"         { return '*'; }
"/"         { return '/'; }
"="         { return '='; }
[0-9]+      { yylval.val = atoi(yytext); return NUMBER; }
[a-z]       { yylval.val = yytext[0] - 'a'; return IDENTIFIER; }
\"[^\"]*\"  { yylval.str = strdup(yytext); return STRING; }
[ \t\n]+    { /* Ignore whitespace */ }
.           { return yytext[0]; }  // Return any single character
%%

int yywrap() {
    return 1;
}