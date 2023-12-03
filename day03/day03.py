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
SAMPLE = (HERE / "sample.txt").read_text()
INPUT = (HERE / "input.txt").read_text()

# [(-1-1j), (-1+0j), (-1+1j), -1j, 1j, (1-1j), (1+0j), (1+1j)]
BORDER = list(
    complex(x, y)
    for x, y in itertools.product(range(-1, 2), range(-1, 2))
    if (x, y) != (0, 0)
)


@dataclass(frozen=True)
class Part:
    "Part number and position"

    num: int
    pos: complex


@dataclass(frozen=True)
class Symbol:
    "Symbol and position"

    char: str
    pos: complex

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
                part = Part(int(m.group()), complex(m.start(), y))
                for x in range(*m.span()):
                    graph.parts[complex(x, y)] = part
            # symbols
            for m in re.finditer(r"[^\d.]", line):
                pos = complex(m.start(), y)
                sym = Symbol(m.group(), pos)
                graph.symbols.append(sym)

        return graph

    def nearby_parts(self, symbol) -> list[Part]:
        "Return list of parts that intersect with symbol's border"
        parts = set()
        for pos in symbol.intersect(set(self.parts)):
            parts.add(self.parts[pos])
        return list(parts)


def part1(graph: Graph) -> int:
    total = 0
    for sym in graph.symbols:
        total += sum(p.num for p in graph.nearby_parts(sym))
    return total


def part2(graph: Graph) -> int:
    total = 0
    gears = (sym for sym in graph.symbols if sym.is_gear)
    for gear in gears:
        part_numbers = [p.num for p in graph.nearby_parts(gear)]
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
