#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <iomanip>
#include <algorithm>

// Global variables
std::map<std::string, int> symbolTable;
std::map<std::string, int> literalTable;
std::vector<int> poolTable;
int locationCounter = 0;
int literalPoolStart = 0;
int startOffset = 0;

// Define assembly directives and instructions
std::vector<std::string> assemblerDirectives = {"START", "END", "LTORG"};
std::vector<std::string> imperativeStatements = {"STOP", "ADD", "SUB", "MUL", "MOVER", "MOVEM", "BC", "DIV", "READ", "PRINT"};
std::vector<std::string> declarativeStatements = {"DC", "DS"};

// Opcode lookup table using pair of strings
std::map<std::string, std::pair<std::string, std::string>> opcodeTable = {
    {"STOP", {"IS", "00"}}, {"ADD", {"IS", "01"}}, {"SUB", {"IS", "02"}},
    {"MOVER", {"IS", "04"}}, {"MOVEM", {"IS", "05"}}, {"BC", {"IS", "07"}},
    {"DIV", {"IS", "08"}}, {"READ", {"IS", "09"}}, {"PRINT", {"IS", "10"}},
    {"START", {"AD", "01"}}, {"END", {"AD", "02"}}, {"LTORG", {"AD", "05"}},
    {"DS", {"DL", "01"}}, {"DC", {"DL", "02"}},
    {"AREG", {"RG", "1"}}, {"BREG", {"RG", "2"}}, {"CREG", {"RG", "3"}}
};

// Instruction class
class Instruction {
public:
    std::string instType;
    std::string label;
    std::string opcode;
    std::string operand1;
    std::string operand2;
    int location;
    std::string opcodeBinary;
    std::string regOperand;
    std::string memOperand;

    Instruction(std::string type, std::string lbl, std::string op, std::string op1, std::string op2, 
               int loc, std::string opBin = "", std::string regOp = "", std::string memOp = "") {
        instType = type;
        label = lbl;
        opcode = op;
        operand1 = op1;
        operand2 = op2;
        location = loc;
        opcodeBinary = opBin;
        regOperand = regOp;
        memOperand = memOp;
    }
};

std::vector<Instruction> instructionList;

// Helper functions
bool isNumber(const std::string& str) {
    return !str.empty() && std::all_of(str.begin(), str.end(), ::isdigit);
}

std::vector<std::string> splitString(const std::string& str) {
    std::vector<std::string> tokens;
    std::stringstream ss(str);
    std::string token;
    while (ss >> token) {
        tokens.push_back(token);
    }
    return tokens;
}

bool contains(const std::vector<std::string>& vec, const std::string& elem) {
    return std::find(vec.begin(), vec.end(), elem) != vec.end();
}

std::string removeComma(const std::string& str) {
    std::string result = str;
    result.erase(std::remove(result.begin(), result.end(), ','), result.end());
    return result;
}

void processAssemblyLine(const std::string& line) {
    std::vector<std::string> parts = splitString(line);
    if (parts.empty()) return;

    // Handle assembler directives
    std::string first = parts[0];
    if (contains(assemblerDirectives, first)) {
        std::string opcodeBinary = opcodeTable[first].second;
        
        if (first == "START") {
            startOffset = std::stoi(parts[1]);
            instructionList.emplace_back("AD", "", first, "", parts[1], locationCounter, opcodeBinary);
        }
        else if (first == "LTORG" || first == "END") {
            poolTable.push_back(literalPoolStart);
            int numUnassignedLiterals = 0;
            
            for (const auto& literal : literalTable) {
                if (literal.second == -1) {
                    literalTable[literal.first] = startOffset + locationCounter;
                    locationCounter++;
                    numUnassignedLiterals++;
                }
            }
            
            literalPoolStart += numUnassignedLiterals;
            instructionList.emplace_back("AD", "", first, "", "", 
                startOffset + locationCounter - numUnassignedLiterals, opcodeBinary);
        }
        return;
    }

    // Check if first word is a label
    std::string label = "";
    int opcodeIndex = 0;
    if (!contains(imperativeStatements, first) && !contains(assemblerDirectives, first)) {
        label = first;
        opcodeIndex = 1;
    }

    // Determine opcode and operands
    if (parts.size() <= opcodeIndex) return;
    std::string opcode = parts[opcodeIndex];
    std::string operand1 = (parts.size() > opcodeIndex + 1) ? removeComma(parts[opcodeIndex + 1]) : "";
    std::string operand2 = (parts.size() > opcodeIndex + 2) ? parts[opcodeIndex + 2] : "";

    // Process Declarative Statements
    if (contains(declarativeStatements, opcode)) {
        std::string opcodeBinary = opcodeTable[opcode].second;
        
        if (opcode == "DS") {
            if (isNumber(operand1)) {
                symbolTable[label] = startOffset + locationCounter;
                locationCounter += std::stoi(operand1);
            }
            else {
                std::cout << "Error: Missing or invalid operand for DS statement at label '" << label << "'\n";
                return;
            }
        }
        else if (opcode == "DC") {
            if (isNumber(operand1)) {
                symbolTable[label] = startOffset + locationCounter;
                locationCounter += 1;
            }
            else {
                std::cout << "Error: Missing or invalid operand for DC statement at label '" << label << "'\n";
                return;
            }
        }

        std::string memOperand = std::to_string(symbolTable[label]);
        while (memOperand.length() < 3) memOperand = "0" + memOperand;
        
        instructionList.emplace_back("DL", label, opcode, "", operand1, 
            startOffset + locationCounter - 1, opcodeBinary, "", memOperand);
        return;
    }

    // Process Imperative Statements
    if (contains(imperativeStatements, opcode)) {
        std::string opcodeBinary = opcodeTable[opcode].second;
        std::string regOperand = "";
        if (opcodeTable.find(operand1) != opcodeTable.end()) {
            regOperand = opcodeTable[operand1].second;
        }

        std::string memOperand = " ";
        if (!operand2.empty() && operand2[0] == '=') {
            if (literalTable.find(operand2) == literalTable.end()) {
                literalTable[operand2] = -1;
            }
            if (literalTable[operand2] != -1) {
                int addr = literalTable[operand2];
                memOperand = std::to_string(addr);
                while (memOperand.length() < 3) memOperand = "0" + memOperand;
            }
        }
        else if (symbolTable.find(operand2) != symbolTable.end()) {
            int addr = symbolTable[operand2];
            memOperand = std::to_string(addr);
            while (memOperand.length() < 3) memOperand = "0" + memOperand;
        }

        instructionList.emplace_back("IS", label, opcode, operand1, operand2,
            startOffset + locationCounter, opcodeBinary, regOperand, memOperand);
        locationCounter++;
    }
}

void printTables() {
    // Print Instruction Table
    std::cout << "\nInstruction Table\n";
    std::cout << std::setw(5) << "Type" << std::setw(8) << "Label" << std::setw(10) << "Opcode"
              << std::setw(15) << "Operand1" << std::setw(15) << "Operand2" << std::setw(10) << "Location"
              << std::setw(12) << "Opcode(2)" << std::setw(8) << "Reg(1)" << std::setw(8) << "Mem(3)"
              << std::setw(25) << "Intermediate Code\n";
    std::cout << std::string(120, '-') << "\n";

    for (const auto& inst : instructionList) {
        std::string intermediateCode;
        if (inst.instType == "IS") {
            intermediateCode = "(" + inst.instType + ", " + inst.opcodeBinary + ")";
            if (!inst.regOperand.empty()) {
                intermediateCode += " (RG, " + inst.regOperand + ")";
            }
            if (!inst.operand2.empty() && inst.operand2[0] == '=') {
                int literalIndex = 0;
                for (const auto& lit : literalTable) {
                    if (lit.first == inst.operand2) break;
                    literalIndex++;
                }
                intermediateCode += " (L, " + std::to_string(literalIndex) + ")";
            }
            else if (symbolTable.find(inst.operand2) != symbolTable.end()) {
                int symbolIndex = 0;
                for (const auto& sym : symbolTable) {
                    if (sym.first == inst.operand2) break;
                    symbolIndex++;
                }
                intermediateCode += " (S, " + std::to_string(symbolIndex) + ")";
            }
        }
        else if (inst.instType == "AD") {
            intermediateCode = "(AD, " + inst.opcodeBinary + ")";
        }
        else if (inst.instType == "DL") {
            int symbolIndex = 0;
            for (const auto& sym : symbolTable) {
                if (sym.first == inst.label) break;
                symbolIndex++;
            }
            intermediateCode = "(" + inst.instType + ", " + inst.opcodeBinary + ") (S, " + 
                             std::to_string(symbolIndex) + ") (C, " + inst.operand2 + ")";
        }

        std::cout << std::setw(5) << inst.instType << std::setw(8) << inst.label
                  << std::setw(10) << inst.opcode << std::setw(15) << inst.operand1
                  << std::setw(15) << inst.operand2 << std::setw(10) << inst.location
                  << std::setw(12) << inst.opcodeBinary << std::setw(8) << inst.regOperand
                  << std::setw(8) << inst.memOperand << std::setw(25) << intermediateCode << "\n";
    }

    // Print Symbol Table
    std::cout << "\nSymbol Table:\n";
    std::cout << std::setw(10) << "Symbol" << std::setw(10) << "Location\n";
    std::cout << std::string(20, '-') << "\n";
    for (const auto& symbol : symbolTable) {
        std::cout << std::setw(10) << symbol.first << std::setw(10) << symbol.second << "\n";
    }

    // Print Literal Table
    std::cout << "\nLiteral Table:\n";
    std::cout << std::setw(10) << "Sr.no" << std::setw(10) << "Literal" << std::setw(10) << "Location\n";
    std::cout << std::string(30, '-') << "\n";
    int idx = 1;
    for (const auto& literal : literalTable) {
        std::cout << std::setw(10) << idx++ << std::setw(10) << literal.first 
                  << std::setw(10) << literal.second << "\n";
    }

    // Print Pool Table
    std::cout << "\nPool Table:\n";
    std::cout << std::setw(10) << "Sr.no" << std::setw(10) << "Literal Pointer\n";
    std::cout << std::string(20, '-') << "\n";
    for (size_t i = 0; i < poolTable.size(); i++) {
        std::cout << std::setw(10) << i << std::setw(10) << poolTable[i] << "\n";
    }
}

int main() {
    std::string fileName = "input.asm";
    std::ifstream file(fileName);
    
    if (!file.is_open()) {
        std::cout << "Error opening file: " << fileName << "\n";
        return 1;
    }

    std::string line;
    while (std::getline(file, line)) {
        if (!line.empty()) {
            processAssemblyLine(line);
        }
    }

    file.close();
    printTables();
    return 0;
}