#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <algorithm> // for std::find

using namespace std;

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

    return 0;
}