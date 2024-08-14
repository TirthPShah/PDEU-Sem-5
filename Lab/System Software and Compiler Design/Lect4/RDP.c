#include <stdio.h>
#include <string.h>

#define SUCCESS 1
#define FAILED 0

// Function prototypes
int E(), Edash(), T(), Tdash(), F();

const char *cursor;
char string[64];

int main() {
	puts("Enter the string");
	scanf("%s", string); // Read input from the user
	cursor = string;
	puts("");


	// Call the starting non-terminal E
	if (E() && *cursor == '\0') { // If parsing is successful and the cursor has reached the end
		puts("String is successfully parsed");
		return 0;
	} 
	else {
		puts("Error in parsing String");
		return 1;
	}
}

// Grammar rule: E -> T E'
int E() {
	if (T()) { // Call non-terminal T
		if (Edash()) // Call non-terminal E'
			return SUCCESS;
		else
			return FAILED;
	} 
	else
		return FAILED;
}

// Grammar rule: E' -> + T E' | $
int Edash() {
	if (*cursor == '+') {
		cursor++;
		if (T()) { // Call non-terminal T
			if (Edash()) // Call non-terminal E'
				return SUCCESS;
			else
				return FAILED;
		} 
		else
			return FAILED;
	}
	else {
		return SUCCESS;
	}
}

// Grammar rule: T -> F T'
int T() {
	if (F()) { // Call non-terminal F
		if (Tdash()) // Call non-terminal T'
			return SUCCESS;
		else
			return FAILED;
	} 
	else
		return FAILED;
}

// Grammar rule: T' -> * F T' | $
int Tdash() {
	if (*cursor == '*') {
		cursor++;
		if (F()) { // Call non-terminal F
			if (Tdash()) // Call non-terminal T'
				return SUCCESS;
			else
				return FAILED;
		} 
		else
			return FAILED;
	} 
	else {

		return SUCCESS;
	}
}

// Grammar rule: F -> ( E ) | i
int F() {
	if (*cursor == '(') {

		cursor++;
		if (E()) { // Call non-terminal E
			if (*cursor == ')') {
				cursor++;
				return SUCCESS;
			} 
			else
				return FAILED;
		} 
		else
			return FAILED;
	} 
	else if (*cursor == 'i') {

		cursor++;
		return SUCCESS;
	} 
	else
		return FAILED;
}
