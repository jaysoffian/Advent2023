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


def split_line(line: str) -> tuple[int, str]:
    """
    Split game line.

    >>> split_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    (1, '3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green')
    """
    m = re.search(r"^Game (\d+): (.*)", line)
    assert m is not None
    game_number, grabs = m.groups()
    return int(game_number), grabs


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


def parse_game1(line: str) -> int:
    """
    Parse game line. Return game number if valid, else 0.

    >>> parse_game1("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    1
    >>> parse_game1("Game 1: 3 blue, 4 red; 1 red, 2 green, 15 blue; 2 green")
    0
    """
    game_number, grabs = split_line(line)

    def is_valid_grab(grab: str) -> bool:
        r, g, b = parse_grab(grab)
        return r <= 12 and g <= 13 and b <= 14

    for grab in grabs.split("; "):
        if not is_valid_grab(grab):
            return 0

    return game_number


def parse_game2(line: str) -> int:
    """
    Parse game line. Return its power.

    >>> parse_game2("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    48
    >>> parse_game2("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue")
    12
    """
    game_number, grabs = split_line(line)

    max_r, max_g, max_b = 0, 0, 0
    for grab in grabs.split("; "):
        r, g, b = parse_grab(grab)
        max_r = max(max_r, r)
        max_g = max(max_g, g)
        max_b = max(max_b, b)

    return max_r * max_g * max_b


def part1(lines) -> int:
    return sum(parse_game1(line) for line in lines)


def part2(lines) -> int:
    return sum(parse_game2(line) for line in lines)


def test():
    lines = INPUT.splitlines()
    assert part1(SAMPLE.splitlines()) == 8
    assert part1(lines) == 2164
    assert part2(SAMPLE.splitlines()) == 2286
    assert part2(lines) == 69929


def main():
    lines = INPUT.splitlines()
    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
