# Distributed Systems Lab: Token Ring and Ricart-Agrawala Algorithms

## Overview
This project demonstrates two distributed mutual exclusion algorithms:
- **Token Ring Algorithm**: A circular structure where each node passes a token to control access to the critical section.
- **Ricart-Agrawala Algorithm**: A timestamp-based mutual exclusion mechanism where processes communicate to determine critical section access.

## Files
- `TokenRing.java`: Implements the Token Ring mutual exclusion algorithm.
- `CriticalSectionSimulator.java`: Implements the Ricart-Agrawala algorithm.
- `TokenRingManager` and `TokenRingNode`: Classes managing token handling and node operations in Token Ring.
- `Process` and `SharedData`: Classes to simulate request and response handling in Ricart-Agrawala.

## Requirements
- Java 8 or higher
- IDE or terminal with command-line Java compilation support

## Running the Code
1. Compile the Java files:
   ```bash
   javac TokenRing.java CriticalSectionSimulator.java

java TokenRing
java CriticalSectionSimulator