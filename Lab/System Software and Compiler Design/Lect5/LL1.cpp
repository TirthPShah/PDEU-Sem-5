#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <string>
using namespace std;

// Production rule
class Rule {
public:
    char lhs;
    string rhs;
    Rule(char lhs, string rhs) {
        this->lhs = lhs;
        this->rhs = rhs;
    }
};

// First Set Function for a single rule
void computeFirstSetForRule(Rule rule, map<char, set<char> >& first, map<char, vector<string> >& productions) {
    string rhs = rule.rhs;

    if (rhs[0] == '@') {  // epsilon
        first[rule.lhs].insert('@');
    } else if (islower(rhs[0]) || rhs[0] == '+' || rhs[0] == '*' || rhs[0] == '(' || rhs[0] == ')') {
        first[rule.lhs].insert(rhs[0]);  // terminal symbol
    } else {
        for (char symbol : rhs) {
            if (islower(symbol) || symbol == '+' || symbol == '*' || symbol == '(' || symbol == ')') {
                first[rule.lhs].insert(symbol);  // terminal symbol
                break;
            } else {
                for (char c : first[symbol]) {
                    if (c != '@') {
                        first[rule.lhs].insert(c);
                    }
                }
            }
        }
    }
}

// Recursive function to calculate the First set for non-terminals
void calculateFirstSet(char nonTerminal, map<char, set<char> >& first, map<char, vector<string> >& productions) {

    for (string rhs : productions[nonTerminal]) {
        if (rhs[0] == '@') {
            first[nonTerminal].insert('@');
        } else {
            for (char symbol : rhs) {
                if (islower(symbol) || symbol == '+' || symbol == '*' || symbol == '(' || symbol == ')') {
                    first[nonTerminal].insert(symbol);
                    break;
                } else {
                    if (first[symbol].empty()) {
                        calculateFirstSet(symbol, first, productions);
                    }
                    for (char c : first[symbol]) {
                        if (c != '@') {
                            first[nonTerminal].insert(c);
                        }
                    }
                }
            }
        }
    }
}

void calculateFollowSet(char nonTerminal, map<char, set<char> >& follow, map<char, vector<string> >& productions) {
    if (nonTerminal == 'E') {
        follow[nonTerminal].insert('$');
    }

    for (auto& entry : productions) {
        for (string rhs : entry.second) {
            for (int i = 0; i < rhs.length(); i++) {
                if()

}

// Generate First Set for each non-terminal
map<char, set<char> > getFirstSet(vector<Rule> rules) {
    map<char, set<char> > first;
    map<char, vector<string> > productions;

    // Organize productions by non-terminal
    for (Rule rule : rules) {
        productions[rule.lhs].push_back(rule.rhs);
    }

    // Calculate First set for each non-terminal
    for (auto& entry : productions) {
        calculateFirstSet(entry.first, first, productions);
    }

    return first;
}

// Print First Set for each non-terminal
void printFirstSet(map<char, set<char> > first) {
    cout << "\nFirst Set For Each Non-terminal:\n" << endl;
    for (auto it : first) {
        cout << "First(" << it.first << ") = { ";
        for (char c : it.second) {
            cout << c << " ";
        }
        cout << "}" << endl;
    }
}

// Generate Follow Set for each non-terminal
map<char, set<char> > getFollowSet(vector<Rule> rules) {
    map<char, set<char> > follow;
    map<char, vector<string> > productions;

    // Organize productions by non-terminal
    for (Rule rule : rules) {
        productions[rule.lhs].push_back(rule.rhs);
    }

    // Calculate Follow set for each non-terminal
    for (auto& entry : productions) {
        calculateFollowSet(entry.first, follow, productions);
    }

    return follow;
}


// Print Follow Set for each non-terminal
void printFollowSet(map<char, set<char> > follow) {
    cout << "\nFollow Set For Each Non-terminal:\n" << endl;
    for (auto it : follow) {
        cout << "Follow(" << it.first << ") = { ";
        for (char c : it.second) {
            cout << c << " ";
        }
        cout << "}" << endl;
    }
}

int main() {
    // Grammar initialization
    vector<Rule> rules;
    rules.push_back(Rule('F', "i"));
    rules.push_back(Rule('F', "(E)"));
    rules.push_back(Rule('B', "@"));  // epsilon
    rules.push_back(Rule('B', "*FB"));
    rules.push_back(Rule('T', "FB"));
    rules.push_back(Rule('A', "@"));  // epsilon
    rules.push_back(Rule('A', "+TA"));
    rules.push_back(Rule('E', "TA"));

    // Print Grammar
    cout << "Grammar:\n" << endl;
    for (Rule rule : rules) {
        cout << rule.lhs << " -> " << rule.rhs << endl;
    }

    // Calculate First Set
    map<char, set<char> > first = getFirstSet(rules);

    // Print First Set for each non-terminal
    printFirstSet(first);



    return 0;
}
