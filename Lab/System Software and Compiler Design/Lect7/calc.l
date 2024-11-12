%{
#include <stdlib.h>
#include <stdio.h>
#include "y.tab.h" 

extern int yylval; 
void yyerror(const char *);
%}

%%

[a-z] { 
    yylval = *yytext - 'a';
    return VARIABLE;
}

[0-9]+ { 
    yylval = atoi(yytext);
    return INTEGER;
}

[-+()=*/] { 
    return *yytext;
}

\n      { return '\n'; } 
[ \t]   { /* Ignore whitespace */ }  
.       { yyerror("Unexpected character."); }

%%

int yywrap(void) {
    return 1;
}
