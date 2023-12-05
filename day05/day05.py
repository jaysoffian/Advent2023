#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/5
"""
import re
from dataclasses import dataclass
from pathlib import Path

from aocd import get_data

HERE = Path(__file__).parent
EXAMPLE1 = (HERE / "example1.txt").read_text().splitlines()
EXAMPLE2 = (HERE / "example2.txt").read_text().splitlines()
INPUT = get_data(year=2023, day=5).splitlines()


@dataclass(frozen=True)
class Range:
    dst: int
    src: int
    length: int

    def __contains__(self, seed: int) -> bool:
        return self.src <= seed < self.src + self.length

    def __getitem__(self, seed: int) -> int:
        return seed - self.src + self.dst


class Solver:
    def __init__(self, debug=False):
        self.seeds: list[int] = []
        self.maps: dict[str, list[Range]] = {}
        if debug:
            self.debug = print
        else:
            self.debug = lambda *args, **kwargs: None

    @classmethod
    def parse(cls, lines: list[str], debug=False) -> "Solver":
        solver = cls(debug)
        m = re.search(r"^seeds: (.*)", lines[0])
        assert m
        solver.seeds.extend(map(int, m.group(1).split()))
        map_name = None
        for line in lines[1:]:
            if m := re.search(r"^(.*) map:", line):
                map_name = m.group(1)
                continue
            if not map_name:
                continue
            if m := re.search(r"^\d", line):
                ranges = solver.maps.setdefault(map_name, [])
                ranges.append(Range(*map(int, line.split())))
        return solver

    def find_location(self, seed: int) -> int:
        for name, ranges in self.maps.items():
            for r in ranges:
                if seed in r:
                    new = r[seed]
                    self.debug(f"{name}: {seed} -> {new}")
                    seed = new
                    break
            else:
                self.debug(f"{name}: {seed} -> {seed}")
        self.debug()
        return seed


def part1(solver: Solver) -> int:
    return min(solver.find_location(seed) for seed in solver.seeds)


def part2(solver: Solver) -> int:
    return 0


def test_examples() -> None:
    solver = Solver.parse(EXAMPLE1, True)
    assert solver.find_location(79) == 82
    assert solver.find_location(14) == 43
    assert solver.find_location(55) == 86
    assert solver.find_location(13) == 35
    assert part1(solver) == 35
    assert part2(Solver.parse(EXAMPLE2, True)) == 0


def test_input() -> None:
    solver = Solver.parse(INPUT)
    assert part1(solver) == 227653707
    assert part2(solver) == 0


def main() -> None:
    solver = Solver.parse(INPUT)
    print(part1(solver))
    # print(part2(INPUT))


if __name__ == "__main__":
    main()
