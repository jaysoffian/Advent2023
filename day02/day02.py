#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/2
"""
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
SAMPLE1 = (HERE / "sample1.txt").read_text()
SAMPLE2 = (HERE / "sample2.txt").read_text()
INPUT = (HERE / "input.txt").read_text()


def parse_game1(game: str) -> int:
    def valid_grab(grab: str) -> bool:
        counts: Counter[str] = Counter()
        for count_color in grab.split(", "):
            count, color = count_color.split()
            counts[color] = int(count)
        r, g, b = counts["red"], counts["green"], counts["blue"]
        return r <= 12 and g <= 13 and b <= 14

    m = re.search(r"^Game (\d+): (.*)", game)
    assert m is not None
    game_number, grabs = m.groups()

    for grab in grabs.split("; "):
        if not valid_grab(grab):
            return 0

    return int(game_number)


def part1(lines) -> int:
    return sum(parse_game1(line) for line in lines)


def part2(lines) -> int:
    return 0


def test():
    assert part1(SAMPLE1.splitlines()) == 8
    lines = INPUT.splitlines()
    assert part1(lines) == 2164


def main():
    lines = INPUT.splitlines()
    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
