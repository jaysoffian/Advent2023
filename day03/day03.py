#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/3
"""
import re
from collections import namedtuple
from pathlib import Path

HERE = Path(__file__).parent
SAMPLE = (HERE / "sample.txt").read_text()
INPUT = (HERE / "input.txt").read_text()


class PartNumber(namedtuple("PartNumber", "n span y")):
    def hit(self, symbols: set[tuple[int, int]]) -> bool:
        for y in (self.y - 1, self.y + 1):
            for x in range(self.span[0] - 1, self.span[1] + 1):
                if (x, y) in symbols:
                    return True
        for x in (self.span[0] - 1, self.span[1]):
            if (x, self.y) in symbols:
                return True
        return False


class Graph:
    def __init__(self):
        self.parts: list[PartNumber] = []
        self.symbols: set[tuple[int, int]] = set()

    @classmethod
    def parse(cls, lines) -> "Graph":
        inst = cls()
        for y, line in enumerate(lines):
            for m in re.finditer(r"\d+", line):
                inst.parts.append(PartNumber(int(m.group()), m.span(), y))
            for m in re.finditer(r"[^\d.]", line):
                inst.symbols.add((m.start(), y))
        return inst


def part1(graph: Graph) -> int:
    total = 0
    for pn in graph.parts:
        if pn.hit(graph.symbols):
            total += pn.n
    return total


def part2(graph: Graph) -> int:
    return 0


def test() -> None:
    graph = Graph.parse(SAMPLE.splitlines())
    assert part1(graph) == 4361

    graph = Graph.parse(INPUT.splitlines())
    assert part1(graph) == 521515


def main() -> None:
    graph = Graph.parse(INPUT.splitlines())
    print(part1(graph))
    print(part2(graph))


if __name__ == "__main__":
    main()
