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
    m = re.search(r"(\d)", line)
    if not m:
        raise ValueError(line)
    x = m.group(1)

    m = re.search(r"(\d)[^\d]*$", line)
    if not m:
        raise ValueError(line)
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

    # To allow for overlapping words, we search from the end by reversing each word
    # and the string being searched and then searching from the front. Alternately,
    # we could use a more-complicated lookahead-assertion or we could apply the
    # forward pattern repeateadly while walking backwards through the string.
    pattern = r"(\d|" + "|".join(w[::-1] for w in words) + ")"
    m = re.search(pattern, line[::-1])
    assert m, line
    y = words.get(m.group(1)[::-1], m.group(1))

    return int(f"{x}{y}")


def part1(lines) -> int:
    return sum(parse1(line) for line in lines)


def part2(lines) -> int:
    return sum(parse2(line) for line in lines)


def test() -> None:
    assert parse2("eighthree") == 83
    assert parse2("sevenine") == 79
    assert part1(SAMPLE1.splitlines()) == 142
    assert part2(SAMPLE2.splitlines()) == 281
    lines = INPUT.splitlines()
    assert part1(lines) == 55477
    assert part2(lines) == 54431


def main() -> None:
    lines = INPUT.splitlines()
    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
