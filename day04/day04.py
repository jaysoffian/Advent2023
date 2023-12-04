#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/4
"""
import re
from collections import Counter
from pathlib import Path

from aocd import get_data

HERE = Path(__file__).parent
EXAMPLE1 = (HERE / "example1.txt").read_text().splitlines()
EXAMPLE2 = (HERE / "example2.txt").read_text().splitlines()
INPUT = get_data(year=2023, day=4).splitlines()


def parse_line(line: str) -> tuple[int, set[int], set[int]]:
    """
    Return tuple of card number, set of winning numbers, set of numbers in hand.

    >>> parse_line("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    (1, {41, 48, 17, 83, 86}, {6, 9, 48, 17, 83, 53, 86, 31})
    """
    m = re.search(r"^Card *(\d+): (.*)$", line)
    assert m
    card_num, rest = m.groups()
    win, _, have = rest.partition("|")
    return int(card_num), set(map(int, win.split())), set(map(int, have.split()))


def num_matches(line: str) -> int:
    _, win, have = parse_line(line)
    return len(win & have)


def eval1(line: str) -> int:
    """
    Return value of line which is the 2 ** (number of winning cards - 1) or 0
    for no winning cards. i.e. 0=0, 1=1, 2=2, 3=4, 4=8, 5=16, ...

    >>> eval1("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    8
    >>> eval1("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19")
    2
    >>> eval1("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1")
    2
    >>> eval1("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83")
    1
    >>> eval1("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36")
    0
    >>> eval1("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11")
    0
    """
    num_win = num_matches(line)
    return 2 ** (num_win - 1) if num_win else 0


def part1(lines: list[str]) -> int:
    return sum(map(eval1, lines))


def part2(lines: list[str]) -> int:
    num_lines = len(lines)
    copies: Counter[int] = Counter(range(1, num_lines + 1))

    for i, line in enumerate(lines, 1):
        num_wins = num_matches(line)
        for j in range(i + 1, min(i + 1 + num_wins, num_lines + 1)):
            copies[j] += copies[i]

    return copies.total()


def test_examples() -> None:
    assert part1(EXAMPLE1) == 13
    assert part2(EXAMPLE2) == 30


def test_input() -> None:
    assert part1(INPUT) == 21088
    assert part2(INPUT) == 6874754


def main() -> None:
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
