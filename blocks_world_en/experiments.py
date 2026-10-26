"""Task 4: five random problems for each N from 3 to 15; results are written to results.md.

Usage:
    python3 experiments.py
"""

import random

from blocks import TABLE, State, dfs, format_moves, verify

SEED = 2026


def random_state(n, rng):
    """Place the blocks in random order, each one on the table or on top of an existing tower."""
    support = [TABLE] * n
    tops = []
    blocks = list(range(1, n + 1))
    rng.shuffle(blocks)
    for k in blocks:
        destination = rng.choice([TABLE] + tops)
        support[k - 1] = destination
        if destination != TABLE:
            tops.remove(destination)
        tops.append(k)
    return State(support)


def generate_problems():
    rng = random.Random(SEED)
    problems = []
    for n in range(3, 16):
        for i in range(1, 6):
            start = random_state(n, rng)
            goal = random_state(n, rng)
            while goal == start:
                goal = random_state(n, rng)
            problems.append((n, i, start, goal))
    return problems


if __name__ == "__main__":
    f = open("results.md", "w", encoding="utf-8")
    f.write(f"# DFS results\n\nSeed: {SEED}. Limit: 1,000,000 nodes or 60 s.\n\n")
    f.write("| N | # | start | goal | length | nodes | time [ms] | verification |\n")
    f.write("|---|---|---|---|---|---|---|---|\n")
    sequences = []

    for n, i, start, goal in generate_problems():
        moves, expanded, elapsed = dfs(start, goal)
        if moves is None:
            length, result = "-", "not found"
        else:
            length, result = len(moves), verify(start, goal, moves)
        f.write(f"| {n} | {i} | {start} | {goal} | {length} | {expanded} | {elapsed * 1000:.2f} | {result} |\n")
        if n <= 8 and moves is not None:
            sequences.append(f"- N={n}, #{i}: {format_moves(moves)}")
        print(f"N={n} #{i}: {length} moves, {expanded} nodes, verification {result}")

    f.write("\n## Move sequences for N <= 8\n\n" + "\n".join(sequences) + "\n")
    f.close()
    print("Saved to results.md")
