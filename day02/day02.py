#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/2
"""
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
SAMPLE = (HERE / "sample.txt").read_text()
INPUT = (HERE / "input.txt").read_text()


def parse_grab(grab: str) -> tuple[int, int, int]:
    """
    Parse single grab. Return (red, green, blue).

    >>> parse_grab("3 blue, 4 red")
    (4, 0, 3)
    >>> parse_grab("3 green, 15 blue, 14 red")
    (14, 3, 15)
    """
    counts: Counter[str] = Counter()
    for count_color in grab.split(", "):
        count, color = count_color.split()
        counts[color] = int(count)
    return counts["red"], counts["green"], counts["blue"]


def parse_line(line: str) -> tuple[int, tuple[tuple[int, int, int], ...]]:
    """
    Parse game line.

    >>> parse_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    (1, ((4, 0, 3), (1, 2, 6), (0, 2, 0)))
    """
    m = re.search(r"^Game (\d+): (.*)", line)
    assert m is not None
    game_number, grabs = m.groups()

    return int(game_number), tuple(parse_grab(g) for g in grabs.split("; "))


def parse_line_1(line: str) -> int:
    """
    Parse game line. Return game number if valid, else 0.

    >>> parse_line_1("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    1
    >>> parse_line_1("Game 1: 3 blue, 4 red; 1 red, 2 green, 15 blue; 2 green")
    0
    """
    game_number, grabs = parse_line(line)

    for r, g, b in grabs:
        if r > 12 or g > 13 or b > 14:
            return 0

    return game_number


def parse_line_2(line: str) -> int:
    """
    Parse game line. Return its power.

    >>> parse_line_2("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    48
    >>> parse_line_2("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue")
    12
    """
    game_number, grabs = parse_line(line)

    max_r, max_g, max_b = 0, 0, 0
    for r, g, b in grabs:
        max_r = max(max_r, r)
        max_g = max(max_g, g)
        max_b = max(max_b, b)

    return max_r * max_g * max_b


def part1(lines: list[str]) -> int:
    return sum(parse_line_1(line) for line in lines)


def part2(lines: list[str]) -> int:
    return sum(parse_line_2(line) for line in lines)


def test() -> None:
    lines = INPUT.splitlines()
    assert part1(SAMPLE.splitlines()) == 8
    assert part1(lines) == 2164
    assert part2(SAMPLE.splitlines()) == 2286
    assert part2(lines) == 69929


def main() -> None:
    lines = INPUT.splitlines()
    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
