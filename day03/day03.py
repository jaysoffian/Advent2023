#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/3
"""
import re
from collections import namedtuple
from operator import mul
from pathlib import Path
from typing import Iterator

HERE = Path(__file__).parent
SAMPLE = (HERE / "sample.txt").read_text()
INPUT = (HERE / "input.txt").read_text()

Coord = namedtuple("Coord", "x y")
Span = namedtuple("Span", "start end")  # end is 1 past the end


class Part(namedtuple("Part", "number span y")):
    def border(self) -> Iterator[Coord]:
        for y in (self.y - 1, self.y + 1):
            for x in range(self.span.start - 1, self.span.end + 1):
                yield Coord(x, y)
        for x in (self.span.start - 1, self.span.end):
            yield Coord(x, self.y)

    def hit(self, coords: set[Coord]) -> bool:
        for coord in self.border():
            if coord in coords:
                return True
        return False


class Graph:
    def __init__(self):
        self.parts: list[Part] = []
        self.symbols: set[Coord] = set()
        self.gears: set[Coord] = set()

    @classmethod
    def parse(cls, lines) -> "Graph":
        inst = cls()
        for y, line in enumerate(lines):
            for m in re.finditer(r"\d+", line):
                inst.parts.append(Part(int(m.group()), Span(*m.span()), y))
            for m in re.finditer(r"[^\d.]", line):
                inst.symbols.add(Coord(m.start(), y))
            for m in re.finditer(r"\*", line):
                inst.gears.add(Coord(m.start(), y))
        return inst


def part1(graph: Graph) -> int:
    total = 0
    for part in graph.parts:
        if part.hit(graph.symbols):
            total += part.number
    return total


def part2(graph: Graph) -> int:
    total = 0
    for gear in graph.gears:
        nearby_parts = [
            p for p in graph.parts if p.y in {gear.y - 1, gear.y, gear.y + 1}
        ]
        part_numbers: list[int] = []
        for part in nearby_parts:
            if part.hit({gear}):
                part_numbers.append(part.number)
        if len(part_numbers) == 2:
            total += mul(*part_numbers)
    return total


def test() -> None:
    graph = Graph.parse(SAMPLE.splitlines())
    assert part1(graph) == 4361
    assert part2(graph) == 467835

    graph = Graph.parse(INPUT.splitlines())
    assert part1(graph) == 521515
    assert part2(graph) == 69527306


def main() -> None:
    graph = Graph.parse(INPUT.splitlines())
    print(part1(graph))
    print(part2(graph))


if __name__ == "__main__":
    main()
