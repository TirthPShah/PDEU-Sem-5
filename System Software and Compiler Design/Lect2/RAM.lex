%{
    /*
        turn occurence of ram to RAM and sita to SITA
    */
%}

%%
"ram" { printf("RAM"); }
"sita" { printf("SITA"); }
. {printf("%s", yytext);}
%%

int yywrap() {
    return 1;
}

int main() {
    yylex();
    return 0;
}