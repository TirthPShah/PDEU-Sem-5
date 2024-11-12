#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <stack>
#include <algorithm> // for std::find

using namespace std;

// Function to generate the precedence table based on operator priority
void generateTable(vector<char>& priorityList, map<char, map<char, char>>& precedenceTable) {
    for (char c : priorityList) {
        for (char d : priorityList) {
            int posOfC = find(priorityList.begin(), priorityList.end(), c) - priorityList.begin();
            int posOfD = find(priorityList.begin(), priorityList.end(), d) - priorityList.begin();

            if (posOfC < posOfD) {
                precedenceTable[c][d] = '<';
            } else if (posOfC > posOfD) {
                precedenceTable[c][d] = '>';
            } else {
                if (c == '$' || c == 'i') {
                    precedenceTable[c][d] = '-';
                } else {
                    precedenceTable[c][d] = '>';
                }
            }
        }
    }
}

// Function to display the stack contents
void displayStack(stack<char> s) {
    vector<char> temp;
    while (!s.empty()) {
        temp.push_back(s.top());
        s.pop();
    }
    reverse(temp.begin(), temp.end());
    for (char c : temp) {
        cout << c;
    }
}

// Function to simulate the operator precedence parsing
void operatorPrecedenceParsing(const string& input, const map<char, map<char, char>>& precedenceTable) {
    stack<char> parseStack;
    parseStack.push('$');  // Initialize stack with '$' representing bottom of stack

    size_t index = 0;
    char lookahead = input[index];

    cout << "Parsing steps:\n";
    cout << "Stack\tInput\tAction\n";

    while (!parseStack.empty() && lookahead != '\0') {
        // Display current stack contents
        displayStack(parseStack);
        cout << "\t" << input.substr(index) << "\t";

        char topOfStack = parseStack.top();
        if (topOfStack == '$' && lookahead == '$') {
            cout << "Accept\n";
            break;
        }

        // Fetch precedence between top of stack and lookahead symbol
        char precedence = precedenceTable.at(topOfStack).at(lookahead);

        if (precedence == '<' || precedence == '-') {
            // Shift operation
            parseStack.push(lookahead);
            cout << "Shift\n";
            lookahead = input[++index];
        } else if (precedence == '>') {
            // Reduce operation (for simplicity, we reduce on encountering any operator precedence conflict)
            parseStack.pop();
            cout << "Reduce\n";
        } else {
            cout << "Error\n";
            break;
        }
    }

    if (lookahead == '$' && parseStack.top() == '$') {
        cout << "String parsed successfully.\n";
    } else {
        cout << "Parsing failed.\n";
    }
}

int main() {
    vector<char> priorityList = {'$', '+', '*', 'i'};
    map<char, map<char, char>> precedenceTable;
    generateTable(priorityList, precedenceTable);

    cout << "Operator Precedence Table\n";

    // Print header
    cout << "  ";
    for (char c : priorityList) {
        cout << c << " ";
    }
    cout << "\n";

    // Print table
    for (char c : priorityList) {
        cout << c << " ";
        for (char d : priorityList) {
            cout << precedenceTable[c][d] << " ";
        }
        cout << "\n";
    }

    // Input string for parsing
    string input;
    cout << "Enter input string (e.g., i+i*i$): ";
    cin >> input;

    // Ensure input ends with '$' to mark the end of input
    if (input.back() != '$') {
        input += '$';
    }

    // Simulate the operator precedence parsing
    operatorPrecedenceParsing(input, precedenceTable);

    return 0;
}
