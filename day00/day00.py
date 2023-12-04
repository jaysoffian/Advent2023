#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/0
"""
from pathlib import Path

from aocd import get_data

HERE = Path(__file__).parent
EXAMPLE1 = (HERE / "example1.txt").read_text().splitlines()
EXAMPLE2 = (HERE / "example2.txt").read_text().splitlines()
INPUT = get_data(year=2023, day=1).splitlines()


def part1(lines: list[str]) -> int:
    return 0


def part2(lines: list[str]) -> int:
    return 0


def test_examples() -> None:
    assert part1(EXAMPLE1) == 0
    assert part2(EXAMPLE2) == 0


def test_input() -> None:
    assert part1(INPUT) == 0
    assert part2(INPUT) == 0


def main() -> None:
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
