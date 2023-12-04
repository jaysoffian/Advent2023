#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/1
"""
import re
from pathlib import Path

from aocd import data

HERE = Path(__file__).parent
EXAMPLE1 = (HERE / "example1.txt").read_text().splitlines()
EXAMPLE2 = (HERE / "example2.txt").read_text().splitlines()
INPUT = data.splitlines()


def parse1(line: str) -> int:
    """
    Parse line, returning the first and last digit as a two-digit number number.

    >>> parse1("abc1def")
    11

    >>> parse1("a1b9c")
    19
    """
    m = re.search(r"(\d)", line)
    assert m, line
    x = m.group(1)

    # prefixing the pattern with .* consumes the entire string and then backtracks
    # till it finds a match, returning the final matching digit.
    m = re.search(r".*(\d)", line)
    assert m, line
    y = m.group(1)

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

    words = {
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
    pattern = r"(\d|" + "|".join(words) + ")"
    m = re.search(pattern, line)
    assert m, line
    x = words.get(m.group(1), m.group(1))

    # prefixing the pattern with .* consumes the entire string and then backtracks
    # till it finds a match, returning the final matching digit (or word).
    m = re.search(f".*{pattern}", line)
    assert m, line
    y = words.get(m.group(1), m.group(1))

    return int(f"{x}{y}")


def part1(lines) -> int:
    return sum(parse1(line) for line in lines)


def part2(lines) -> int:
    return sum(parse2(line) for line in lines)


def test_examples() -> None:
    assert part1(EXAMPLE1) == 142
    assert part2(EXAMPLE2) == 281


def test_input() -> None:
    assert part1(INPUT) == 55477
    assert part2(INPUT) == 54431


def main() -> None:
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
