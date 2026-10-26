[README.md](https://github.com/user-attachments/files/33977278/README.md)
# Blocks World

A solver for the blocks world problem (basic variant). Given an initial and a goal arrangement
of numbered blocks, the program finds a sequence of moves that transforms one into the other
using depth-first search with backtracking, and then verifies the result.

## Problem

N blocks numbered 1 to N lie on a table, either directly on the table or on another block.
At most one block can rest directly on another block, but towers can be of any height.
A block is clear if nothing rests on it.

Allowed moves (one block per move):

1. move a clear block that rests on another block onto the table,
2. move a clear block that rests on the table onto another clear block.

Moving a block directly from one block onto another is not allowed in this variant.

## Requirements

Python 3.10 or newer. No external packages are needed.

## Usage

Solve a single problem:

```bash
python3 blocks.py examples/example.txt
```

Run the experiments (65 random problems, results written to `results.md`):

```bash
python3 experiments.py
```

Run the tests:

```bash
python3 -m unittest discover -s tests -v
```

All commands should be run from this folder.

## Input format

The input file contains two lines: the initial arrangement and the goal arrangement.
Blank lines and lines starting with `#` are ignored.

Each arrangement is a list of N integers separated by spaces. The i-th number is the block
on which block i rests, and `0` denotes the table.

```
# start: [1 2 4] [3 5]
0 1 0 2 3
# goal: a single tower [5 4 3 2 1] (5 at the bottom)
2 3 4 5 0
```

Towers are written bottom to top, so `[1 2 4]` means block 1 on the table, 2 on 1 and 4 on 2.

A move is written as a pair `(block, destination)`, where destination `0` is the table.
For example, `(4, 0)` means "put block 4 on the table" and `(4, 5)` means "put block 4 on block 5".

## Example output

```
$ python3 blocks.py examples/example.txt
Start: [1 2 4] [3 5]
Goal:  [5 4 3 2 1]
Expanded nodes: 7, time: 0.0000 s
Number of moves: 7
Moves: (5, 0) (4, 0) (4, 5) (3, 4) (2, 0) (2, 3) (1, 2)
Verification: OK
```

Invalid input is rejected with a message:

```
$ python3 blocks.py examples/invalid_cycle.txt
Invalid input: initial configuration: cycle detected: the table cannot be reached from block 1
```

## How it works

**Validation.** An arrangement is rejected if a block rests on itself, rests on a block that
does not exist, shares its support with another block, or is part of a cycle.

**Search.** The program uses recursive depth-first search. Visited states are kept in a set,
so no state is expanded twice. If a move leads to a dead end, it is undone and the next move
is tried. The search stops after 1,000,000 expanded nodes or 60 seconds.

**Move ordering.** A block is *in place* if it rests where it does in the goal and everything
below it is in place too. Moves are tried in this order:

1. moves that put a block directly in its goal position,
2. moves that put a misplaced block on the table,
3. all other moves.

In practice this dismantles misplaced towers and rebuilds them from the bottom up.
Each block is moved at most twice, so a solution has at most 2N moves. The solution is not
guaranteed to be the shortest one.

**Verification.** The `verify` function replays the moves from the initial state, checks every
move against the rules and compares the final state with the goal. It reports the number of the
first invalid move and the reason, for example `error in move 2: block 1 is not clear`.

## Project structure

```
blocks_world_en/
    blocks.py           main program: State class, input parsing, DFS, verification
    experiments.py      random problems for N = 3..15, writes results.md
    results.md          experiment results
    REPORT.md           project report
    examples/           example from the assignment and invalid inputs
    tests/
        test_blocks.py  automated tests
```

## Results

All 65 random problems (seed 2026, five for each N from 3 to 15) were solved and passed
verification, each in under 1 ms. See `results.md` for the full table and `REPORT.md` for the
discussion.
