/* Count no. of vowels
*/
%{
    int vowels = 0;
%}

%%
[aeiouAEIOU] {vowels++;}
.;
%%

int main() {
    yylex();
    printf("Total vowels: %d\n", vowels);
    return 0;
}