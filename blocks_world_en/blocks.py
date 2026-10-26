"""Blocks world, basic variant (moves 1 and 2).

Usage:
    python3 blocks.py examples/example.txt
"""

import sys
import time

TABLE = 0


class State:
    """A configuration of N blocks.

    support[k-1] is the block on which block k rests (0 means the table),
    exactly as in the input file.
    """

    def __init__(self, support):
        self.support = tuple(support)
        self.n = len(support)

    def is_clear(self, k):
        """A block is clear if nothing rests on it, i.e. its number does not appear in support."""
        return k not in self.support

    def moves(self):
        """Return all legal moves as (block, destination) pairs."""
        result = []
        for k in range(1, self.n + 1):
            if not self.is_clear(k):
                continue
            if self.support[k - 1] != TABLE:
                result.append((k, TABLE))  # move 1: from a block onto the table
            else:
                for d in range(1, self.n + 1):  # move 2: from the table onto a clear block
                    if d != k and self.is_clear(d):
                        result.append((k, d))
        return result

    def apply(self, move):
        """Return a new state with the move applied; the current state is left unchanged."""
        k, d = move
        new_support = list(self.support)
        new_support[k - 1] = d
        return State(new_support)

    def is_in_place(self, k, goal):
        """True if block k rests where it does in the goal and everything below it does as well."""
        if self.support[k - 1] != goal.support[k - 1]:
            return False
        if self.support[k - 1] == TABLE:
            return True
        return self.is_in_place(self.support[k - 1], goal)

    def __eq__(self, other):
        return self.support == other.support

    def __hash__(self):
        return hash(self.support)

    def __str__(self):
        """Towers listed bottom to top, e.g. [1 2 4] [3 5]."""
        towers = []
        for k in range(1, self.n + 1):
            if self.support[k - 1] == TABLE:
                tower = [k]
                while tower[-1] in self.support:
                    tower.append(self.support.index(tower[-1]) + 1)
                towers.append("[" + " ".join(str(x) for x in tower) + "]")
        return " ".join(towers)


def state_error(support):
    """Return None if the configuration is valid, otherwise a description of the problem."""
    n = len(support)
    for k in range(1, n + 1):
        s = support[k - 1]
        if s == k:
            return f"block {k} rests on itself"
        if s < 0 or s > n:
            return f"block {k} rests on block {s}, which does not exist"
        if s != TABLE and support.count(s) > 1:
            return f"more than one block rests on block {s}"
    for k in range(1, n + 1):
        # In a valid configuration the table is reached in at most n steps down;
        # otherwise the blocks form a cycle.
        x = k
        for _ in range(n):
            if x != TABLE:
                x = support[x - 1]
        if x != TABLE:
            return f"cycle detected: the table cannot be reached from block {k}"
    return None


def read_problem(path):
    """Read the initial and goal configurations from a file. Blank lines and lines starting with # are skipped."""
    lines = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#"):
            lines.append(line)
    if len(lines) != 2:
        raise ValueError("the file must contain exactly 2 configurations")

    start = [int(x) for x in lines[0].split()]
    goal = [int(x) for x in lines[1].split()]
    if len(start) != len(goal):
        raise ValueError("the configurations have a different number of blocks")
    if state_error(start):
        raise ValueError("initial configuration: " + state_error(start))
    if state_error(goal):
        raise ValueError("goal configuration: " + state_error(goal))
    return State(start), State(goal)


def ordered_moves(state, goal):
    """Legal moves sorted by priority:
    0 - the block goes straight to its goal position (the table or a block already in place),
    1 - a misplaced block is moved to the table,
    2 - all remaining moves.
    """
    def priority(move):
        k, d = move
        if d == goal.support[k - 1] and (d == TABLE or state.is_in_place(d, goal)):
            return 0
        if d == TABLE and not state.is_in_place(k, goal):
            return 1
        return 2

    return sorted(state.moves(), key=priority)


class LimitExceeded(Exception):
    pass


def dfs(start, goal, max_nodes=1_000_000, max_time=60):
    """Depth-first search with backtracking.

    Returns (moves, number of expanded nodes, time in seconds); moves is None if no solution was found.
    """
    t0 = time.time()
    visited = {start}
    path = []
    expanded = 0

    def search(state):
        nonlocal expanded
        if state == goal:
            return True
        if expanded >= max_nodes or time.time() - t0 > max_time:
            raise LimitExceeded()
        expanded += 1
        for move in ordered_moves(state, goal):
            successor = state.apply(move)
            if successor in visited:
                continue
            visited.add(successor)
            path.append(move)
            if search(successor):
                return True
            path.pop()  # dead end: undo the move (backtracking)
        return False

    try:
        found = search(start)
    except LimitExceeded:
        print("Node or time limit exceeded")
        found = False
    return (path if found else None), expanded, time.time() - t0


def verify(start, goal, moves):
    """Return "OK" or a description of the first invalid move."""
    state = start
    for i, (k, d) in enumerate(moves, 1):
        if k < 1 or k > state.n or d < 0 or d > state.n:
            return f"error in move {i}: no such block"
        if k == d:
            return f"error in move {i}: a block cannot be placed on itself"
        if not state.is_clear(k):
            return f"error in move {i}: block {k} is not clear"
        if d == TABLE and state.support[k - 1] == TABLE:
            return f"error in move {i}: block {k} is already on the table"
        if d != TABLE and not state.is_clear(d):
            return f"error in move {i}: block {d} is not clear"
        if d != TABLE and state.support[k - 1] != TABLE:
            return f"error in move {i}: a block can only be placed on another block from the table"
        state = state.apply((k, d))
    if state != goal:
        return "error: the final configuration differs from the goal"
    return "OK"


def format_moves(moves):
    return " ".join(f"({k}, {d})" for k, d in moves)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 blocks.py file.txt")
        sys.exit(1)
    try:
        start, goal = read_problem(sys.argv[1])
    except (ValueError, OSError) as e:
        print("Invalid input:", e)
        sys.exit(1)

    print("Start:", start)
    print("Goal: ", goal)
    moves, expanded, elapsed = dfs(start, goal)
    print(f"Expanded nodes: {expanded}, time: {elapsed:.4f} s")
    if moves is None:
        print("No solution found")
        sys.exit(1)
    print("Number of moves:", len(moves))
    print("Moves:", format_moves(moves))
    print("Verification:", verify(start, goal, moves))
