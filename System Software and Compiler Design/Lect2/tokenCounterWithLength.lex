%{
    int token = 0;
    int other = 0;
%}

%%

"auto"|"break"|"case"|"char"|"const"|"continue"|"default"|"do"|"double"|"else"|"enum"|"extern"|"float"|"for"|"goto"|"if"|"int"|"long"|"register"|"return"|"short"|"signed"|"sizeof"|"static"|"struct"|"switch"|"typedef"|"union"|"unsigned"|"void"|"volatile"|"while" {token++; printf("Keyword: %s length(%zu)\n", yytext, yyleng);}
"+"|"-"|"*"|"/"|"%"|"="|"=="|"!="|"<"|">"|"<="|">=" {token++; printf("Operator: %s length(%zu)\n", yytext, yyleng);}
[a-zA-Z_][a-zA-Z0-9_]* {token++; printf("Identifier: %s length(%zu)\n", yytext, yyleng);}
[0-9]+ {token++; printf("Number: %s length(%zu)\n", yytext, yyleng);}
"("|")"|"{"|"}"|"["|"]"|";"|","|"."|":" {token++; printf("Separator: %s length(%zu)\n", yytext, yyleng);}
[ \t\n] {token++; printf("Whitespace: %s length(%zu)\n", yytext, yyleng);}
"#include"|"#define"|"#undef"|"#if"|"#ifdef"|"#ifndef"|"#else"|"#elif"|"#endif"|"#error"|"#pragma" {token++; printf("Preprocessor: %s length(%zu)\n", yytext, yyleng);}
. {other++; printf("Other: %s length(%zu)\n", yytext, yyleng);}



%%

int yywrap() {
    return 1;
}

int main() {
    yylex();
    printf("Total tokens: %d\n", token);
    printf("Total other characters: %d\n", other);
    return 0;
}
