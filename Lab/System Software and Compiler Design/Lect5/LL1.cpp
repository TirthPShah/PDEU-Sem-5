#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <set>

using namespace std;

class FollowSetCalc {
public:
    char startSymbol = 'E';
    map<char, vector<string>> productions;
    map<char, set<char>> firstSet;
    map<char, set<char>> followSet;
    map<char, map<char, string>> parsingTable;
    map<char, vector<pair<char, string>>> nonTerminalInfo; // New data structure
    set<char> terminals = {'+', '*', '(', ')', 'i', '$'};
    set<char> nonTerminals = {'A', 'B', 'E', 'F', 'T'};

    char epsilon = '#';
    char endMarker = '$';

    void initializeProductions() {
        productions['A'] = {"#", "+TA"};
        productions['B'] = {"#", "*FB"};
        productions['E'] = {"TA"};
        productions['F'] = {"i", "(E)"};
        productions['T'] = {"FB"};
    }

    void initFirstSet() {
        for (const auto& entry : productions) {
            firstSet[entry.first] = {};
        }
    }

    void initFollowSet() {
        for (const auto& entry : productions) {
            followSet[entry.first] = {};
        }
        followSet[startSymbol].insert(endMarker);
    }

    bool add(map<char, set<char>>& setMap, char key, char value) {
        if(setMap[key].count(value) == 0) {
            setMap[key].insert(value);
            return true;
        }
        return false;
    }

    bool addAll(map<char, set<char>>& setMap, char key, const set<char>& values) {
        auto& targetSet = setMap[key];
        auto beforeSize = targetSet.size();

        targetSet.insert(values.begin(), values.end());

        return targetSet.size() > beforeSize;
    }

    void calcFirstSet() {
        bool changed;

        do {
            changed = false;
            for(const auto& entry : productions) {
                char nonTerminal = entry.first;
                for(const string& rhs : entry.second) {
                    for(char symbol : rhs) {
                        if(!isupper(symbol)) {
                            changed |= add(firstSet, nonTerminal, symbol);
                            nonTerminalInfo[nonTerminal].emplace_back(symbol, rhs);
                            break;
                        }
                        else {
                            set<char> firstOfSymbol = firstSet[symbol];
                            changed |= addAll(firstSet, nonTerminal, firstOfSymbol);
                            if (firstOfSymbol.count(epsilon) == 0) {
                                break;
                            }
                        }
                    }
                }
            }
        } while(changed);
    }

    void calcFollowSet() {
        bool changed;

        do {
            changed = false;
            for(const auto& entry : productions) {
                char nonTerminal = entry.first;
                for(const string& rhs : entry.second) {
                    for(size_t i = 0; i < rhs.size(); ++i) {
                        if(isupper(rhs[i])) {
                            if(i + 1 < rhs.size()) {
                                char nextSymbol = rhs[i + 1];
                                if(isupper(nextSymbol)) {
                                    set<char> firstOfNext = firstSet[nextSymbol];
                                    for(char c : firstOfNext) {
                                        if(c != epsilon) {
                                            changed |= add(followSet, rhs[i], c);
                                        }
                                    }
                                    if(firstOfNext.count(epsilon)) {
                                        changed |= addAll(followSet, rhs[i], followSet[nonTerminal]);
                                    }
                                } else {
                                    changed |= add(followSet, rhs[i], nextSymbol);
                                }
                            } else {
                                changed |= addAll(followSet, rhs[i], followSet[nonTerminal]);
                            }
                        }
                    }
                }
            }
        } while(changed);
    }

    void printNonTerminalInfo() {
        cout << "\nNon-terminal Info:\n";
        for (const auto& entry : nonTerminalInfo) {
            cout << "Non-terminal: " << entry.first << endl;
            for (const auto& [firstElement, production] : entry.second) {
                cout << "First element: " << firstElement << ", Production: " << production << endl;
            }
        }
    }

    void makeParseTable() {
    // Initialize parsing table with "error"

    for (char nt : nonTerminals) {
        for (char t : terminals) {
            parsingTable[nt][t] = "error";
        }
    }

    // Fill parsing table based on nonTerminalInfo
    for (const auto& ntEntry : nonTerminalInfo) {

        char nonTerminal = ntEntry.first;
        for (const auto& [firstElement, production] : ntEntry.second) {

            cout << "Non-terminal: " << nonTerminal << ", First element: " << firstElement << ", Production: " << production << endl;

            if (firstElement != epsilon) {
                parsingTable[nonTerminal][firstElement] = production;
            }


        }

    }
}


void printParsingTable() {
    cout << "\nParsing Table:\n";
    // Print header row
    cout << "    ";
    for (char t : terminals) {
        cout << t << "   ";
    }
    cout << endl;

    // Print table rows
    for (const auto& row : parsingTable) {
        char nonTerminal = row.first;
        cout << nonTerminal << " ";
        for (char t : terminals) {
            cout << row.second.at(t) << "   ";
        }
        cout << endl;
    }
}


    void displayFirstSet() {
        cout << "\nFirst Sets:\n";
        for (const auto& entry : firstSet) {
            cout << "FIRST(" << entry.first << ") = { ";
            for (char c : entry.second) {
                cout << c << " ";
            }
            cout << "}\n";
        }
    }

    void displayFollowSet() {
        cout << "\nFollow Sets:\n";
        for (const auto& entry : followSet) {
            cout << "FOLLOW(" << entry.first << ") = { ";
            for (char c : entry.second) {
                cout << c << " ";
            }
            cout << "}\n";
        }
    }
};

int main() {
    FollowSetCalc calc;
    calc.initializeProductions();
    calc.initFirstSet();
    calc.initFollowSet();

    calc.calcFirstSet();
    calc.calcFollowSet();

    calc.makeParseTable();
    calc.displayFirstSet();
    calc.displayFollowSet();
    calc.printParsingTable();

    return 0;
}
