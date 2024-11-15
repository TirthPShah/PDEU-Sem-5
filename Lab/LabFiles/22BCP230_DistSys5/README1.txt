# Bully Election Algorithm Simulation

This project simulates the Bully Election Algorithm in a distributed system where processes communicate and manage leader election. The simulation includes process failure and recovery events to demonstrate how the Bully Algorithm handles these cases.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Setup and Execution](#setup-and-execution)
- [Architecture](#architecture)
- [Simulation Flow](#simulation-flow)
- [Sample Output](#sample-output)
- [Project Files](#project-files)

## Introduction

The Bully Election Algorithm is a method used in distributed systems to elect a leader or coordinator among processes. When a failure is detected in the current leader, an election is initiated to select the highest PID (Process ID) as the new leader. The project demonstrates this algorithm by simulating failures, recoveries, and periodic election checks in a multi-process environment.

## Features

- Simulates a distributed system of `N` processes with unique PIDs.
- Implements the Bully Election Algorithm for leader election.
- Simulates random process failures and recoveries.
- Initiates a new election if the current leader fails.
- Elects a new leader when a recovered process has a higher PID than the current leader.

## Requirements

- Java Development Kit (JDK) 8 or later.
- A Java-compatible IDE or command-line tools.

## Setup and Execution

1. **Clone or Download the Repository:** Download the source files to your local machine.

2. **Compile the Java File:**
    ```bash
    javac BullyElection.java
    ```

3. **Run the Simulation:**
    ```bash
    java BullyElection
    ```

4. **Observation:** The simulation will output process events (such as failures, activations, and elections) to the console.

## Architecture

- **Processes and PIDs:** Each process is assigned a unique PID, and its status is maintained in an array (`pStatus`), where `1` indicates an alive process and `0` indicates a dead process.
- **Leader (Coordinator):** The current coordinator is the highest alive PID.
- **Thread Pool:** The simulation uses a fixed thread pool to manage three concurrent tasks:
    - `simulateCrashes`: Randomly selects processes to simulate failure.
    - `simulateActivations`: Randomly activates dead processes, simulating recovery.
    - `periodicElections`: Periodically triggers the election to check if the coordinator is still active.

## Simulation Flow

1. **Initialization:** The program starts by creating a random number of processes (between 5 and 15) and setting their statuses randomly (alive or dead).
2. **Process Failure:** The `simulateCrashes` function randomly crashes processes and initiates an election when a failure occurs.
3. **Process Recovery:** The `simulateActivations` function randomly activates dead processes, simulating recovery, and initiates an election to see if the new process should become the leader.
4. **Periodic Elections:** The `periodicElections` function initiates an election at regular intervals to verify if the current leader is still valid.
5. **Bully Election Algorithm:** When an election is triggered, each process with a higher PID than the initiator is queried. The highest alive PID becomes the new leader.

## Sample Output

```plaintext
Processes: 1 2 3 4 5 6 7 
Alive:     1 1 1 1 0 1 0 
Coordinator: Process 6
Process 5 activated.
Message sent to Process 1
Message sent to Process 2
Message sent to Process 3
Message sent to Process 4
Message sent to Process 5
New Coordinator: Process 6
Process 6 crashed.
No alive processes found!
Process 2 crashed.
New Coordinator: Process 5
