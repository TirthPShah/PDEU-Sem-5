import java.util.*;

public class FollowSetCalculator {
    private static final char EPSILON = '@';
    private static final char END_MARKER = '$';
    private static final Map<Character, List<String>> productions = new HashMap<>();
    private static final Map<Character, Set<Character>> firstSets = new HashMap<>();
    private static final Map<Character, Set<Character>> followSets = new HashMap<>();

    public static void main(String[] args) {
        initializeProductions();
        initializeFirstSets();
        initializeFollowSets();

        calculateFirstSets();
        calculateFollowSets();

        printFollowSets();
    }

    private static void initializeProductions() {
        productions.put('A', Arrays.asList("@", "+TA"));
        productions.put('B', Arrays.asList("@", "*FB"));
        productions.put('E', Collections.singletonList("TA"));
        productions.put('F', Arrays.asList("i", "(E)"));
        productions.put('T', Collections.singletonList("FB"));
    }

    private static void initializeFirstSets() {
        // Initialize first sets for all non-terminals
        for (char nonTerminal : productions.keySet()) {
            firstSets.put(nonTerminal, new HashSet<>());
        }
    }

    private static void initializeFollowSets() {
        // Initialize follow sets for all non-terminals
        for (char nonTerminal : productions.keySet()) {
            followSets.put(nonTerminal, new HashSet<>());
        }
        // Add end marker '$' to the follow set of the start symbol
        followSets.get('E').add(END_MARKER);
    }

    private static void calculateFirstSets() {
        boolean changed;
        do {
            changed = false;
            for (Map.Entry<Character, List<String>> entry : productions.entrySet()) {
                char nonTerminal = entry.getKey();
                for (String production : entry.getValue()) {
                    for (int i = 0; i < production.length(); i++) {
                        char symbol = production.charAt(i);
                        if (!isNonTerminal(symbol)) {
                            changed |= firstSets.get(nonTerminal).add(symbol);
                            break;
                        } else {
                            Set<Character> firstSet = firstSets.get(symbol);
                            changed |= firstSets.get(nonTerminal).addAll(firstSet);
                            if (!firstSet.contains(EPSILON)) break;
                        }
                    }
                }
            }
        } while (changed);
    }

    private static void calculateFollowSets() {
        boolean changed;
        do {
            changed = false;
            for (Map.Entry<Character, List<String>> entry : productions.entrySet()) {
                char nonTerminal = entry.getKey();
                for (String production : entry.getValue()) {
                    for (int i = 0; i < production.length(); i++) {
                        char symbol = production.charAt(i);
                        if (isNonTerminal(symbol)) {
                            if (i + 1 < production.length()) {
                                char nextSymbol = production.charAt(i + 1);
                                if (isNonTerminal(nextSymbol)) {
                                    Set<Character> firstSet = firstSets.get(nextSymbol);
                                    for (char first : firstSet) {
                                        if (first != EPSILON) {
                                            changed |= followSets.get(symbol).add(first);
                                        }
                                    }
                                    if (firstSet.contains(EPSILON)) {
                                        changed |= followSets.get(symbol).addAll(followSets.get(nonTerminal));
                                    }
                                } else {
                                    changed |= followSets.get(symbol).add(nextSymbol);
                                }
                            } else {
                                changed |= followSets.get(symbol).addAll(followSets.get(nonTerminal));
                            }
                        }
                    }
                }
            }
        } while (changed);
    }

    private static boolean isNonTerminal(char symbol) {
        return productions.containsKey(symbol);
    }

    private static void printFollowSets() {
        for (Map.Entry<Character, Set<Character>> entry : followSets.entrySet()) {
            System.out.println("FOLLOW(" + entry.getKey() + ") = " + entry.getValue());
        }
    }
}
