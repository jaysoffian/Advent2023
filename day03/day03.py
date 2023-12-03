#!/usr/bin/env python3
"""
https://adventofcode.com/2023/day/3
"""
import itertools
import re
from dataclasses import dataclass
from operator import mul
from pathlib import Path
from typing import Iterator

HERE = Path(__file__).parent
EXAMPLE = (HERE / "example.txt").read_text().splitlines()
INPUT = (HERE / "input.txt").read_text().splitlines()

# [(-1-1j), (-1+0j), (-1+1j), -1j, 1j, (1-1j), (1+0j), (1+1j)]
BORDER = list(
    complex(x, y)
    for x, y in itertools.product(range(-1, 2), range(-1, 2))
    if (x, y) != (0, 0)
)


@dataclass(frozen=True)
class Part:
    "Part number and position"

    pos: complex
    num: int


@dataclass(frozen=True)
class Symbol:
    "Symbol and position"

    pos: complex
    char: str

    @property
    def border(self) -> Iterator[complex]:
        "Iterator over symbol border coordinates"
        for offset in BORDER:
            yield self.pos + offset

    @property
    def is_gear(self) -> bool:
        return self.char == "*"

    def intersect(self, coords: set[complex]) -> set[complex]:
        "Return intersection of coordinates with symbol's border"
        return set(self.border) & coords


class Graph:
    def __init__(self) -> None:
        self.parts: dict[complex, Part] = {}
        self.symbols: list[Symbol] = []

    @classmethod
    def parse(cls, lines) -> "Graph":
        "Return Graph from lines"
        graph = cls()
        for y, line in enumerate(lines):
            # index parts by their span
            for m in re.finditer(r"\d+", line):
                pos = complex(m.start(), y)
                part = Part(pos, int(m.group()))
                for x in range(*m.span()):
                    graph.parts[complex(x, y)] = part
            # symbols
            for m in re.finditer(r"[^\d.]", line):
                pos = complex(m.start(), y)
                sym = Symbol(pos, m.group())
                graph.symbols.append(sym)

        return graph

    @property
    def gears(self) -> list[Symbol]:
        return [sym for sym in self.symbols if sym.is_gear]

    def adjacent_parts(self, symbol) -> list[Part]:
        "Return list of parts that intersect with symbol's border"
        parts = set()
        for pos in symbol.intersect(set(self.parts)):
            parts.add(self.parts[pos])
        return list(parts)


def part1(graph: Graph) -> int:
    total = 0
    for sym in graph.symbols:
        total += sum(p.num for p in graph.adjacent_parts(sym))
    return total


def part2(graph: Graph) -> int:
    total = 0
    for gear in graph.gears:
        part_nums = [p.num for p in graph.adjacent_parts(gear)]
        if len(part_nums) == 2:
            total += mul(*part_nums)
    return total


def test_example() -> None:
    graph = Graph.parse(EXAMPLE)
    assert part1(graph) == 4361
    assert part2(graph) == 467835


def test_input() -> None:
    graph = Graph.parse(INPUT)
    assert part1(graph) == 521515
    assert part2(graph) == 69527306


def main() -> None:
    graph = Graph.parse(INPUT)
    print(part1(graph))
    print(part2(graph))


if __name__ == "__main__":
    main()
