#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/1
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
SAMPLE1 = (HERE / "sample1.txt").read_text()
SAMPLE2 = (HERE / "sample2.txt").read_text()
INPUT = (HERE / "input.txt").read_text()


def parse1(line: str) -> int:
    """
    Parse line, returning the first and last digit as a two-digit number number.

    >>> parse1("abc1def")
    11

    >>> parse1("a1b9c")
    19
    """
    m1 = re.search(r"(\d)", line)
    if not m1:
        raise ValueError(line)

    m2 = re.search(r"(\d)[^\d]*$", line)
    if not m2:
        raise ValueError(line)

    x, y = m1.group(1), m2.group(1)
    return int(f"{x}{y}")


def parse2(line: str) -> int:
    """
    Parse line, returning the first and last digit as a two-digit number number.
    The digits may also be spelled out as words and the words may overlap.

    >>> parse2("eighthree")
    83

    >>> parse2("sevenine")
    79
    """
    repls = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    search = re.compile(r"(\d|" + "|".join(repls) + ")").search
    digits = []
    # This is complicated by allowing for overlapping words so we apply
    # the pattern repeatedly from first to last character of the line rather
    # than trying to be clever with the pattern. It performs well enough to solve
    # the puzzle.
    for i in range(len(line)):
        if m := search(line[i:]):
            digits.append(repls.get(m.group(1), m.group(1)))
    a, b = digits[0], digits[-1]
    return int(f"{a}{b}")


def part1(lines) -> int:
    return sum(parse1(line) for line in lines)


def part2(lines) -> int:
    return sum(parse2(line) for line in lines)


def test():
    assert parse2("eighthree") == 83
    assert parse2("sevenine") == 79
    assert part1(SAMPLE1.splitlines()) == 142
    assert part2(SAMPLE2.splitlines()) == 281


def main():
    lines = INPUT.splitlines()
    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
