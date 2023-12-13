from typing import List
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Point:
  x: int
  y: int


@dataclass(frozen=True)
class Number:
  value: str
  points: List[Point]

  def __hash__(self):
    return self.points[0].__hash__()


def day3():
  with open('input/day3.txt') as f:
    grid = f.read().splitlines()

  pattern = r'\d+'
  numbers = []
  for y, line in enumerate(grid):
    for match in re.finditer(pattern, line):
      numbers.append(Number(
        value=match.group(),
        points=[Point(x, y) for x in range(match.start(), match.end())]
      ))

  part_numbers = []
  for number in numbers:
    # readability variables
    x_left_of = number.points[0].x - 1
    x_right_of = number.points[-1].x + 1
    y = number.points[0].y

    # get points surrounding a line
    x_coord_span = range(x_left_of, x_right_of + 1)
    top = [Point(i, y - 1) for i in x_coord_span]
    left = [Point(x_left_of, y)]
    right = [Point(x_right_of, y)]
    bottom = [Point(i, y + 1) for i in x_coord_span]
    surrounding = top + left + right + bottom
    real_surrounding = list(filter(lambda p: is_in_grid(p, grid), surrounding))

    # do what they asked us to do
    is_part_number = any(is_symbol(char_at(p, grid)) for p in real_surrounding)
    if is_part_number:
      part_numbers.append(number)

  print(f'sum of part numbers: {sum([int(p.value) for p in part_numbers])}')

  pattern = r'\*'
  gear_points = []
  for y, line in enumerate(grid):
    for match in re.finditer(pattern, line):
      gear_points.append(Point(match.start(), y))

  gear_ratios = []
  for gear_point in gear_points:
    surrounding = get_surrounding_points(gear_point)
    real_surrounding = list(filter(lambda p: is_in_grid(p, grid), surrounding))
    adjacent_part_numbers = []
    for surrounding_point in real_surrounding:
      for part_num in part_numbers:
        if surrounding_point in part_num.points:
          adjacent_part_numbers.append(part_num)
    adjacent_part_numbers_set = list(set(adjacent_part_numbers))
    if len(adjacent_part_numbers_set) == 2:
      gear_ratios.append(int(adjacent_part_numbers_set[0].value) * int(adjacent_part_numbers_set[1].value))

  print(f'Sum of gear ratios: {sum(gear_ratios)}')


def is_symbol(c):
  return not c.isdigit() and c != '.'


def get_surrounding_points(p):
  x = p.x
  y = p.y
  top = [Point(x - 1, y - 1), Point(x, y - 1), Point(x + 1, y - 1)]
  left = [Point(x-1, y)]
  right = [Point(x+1, y)]
  bottom = [Point(x - 1, y + 1), Point(x, y + 1), Point(x + 1, y + 1)]
  return top + left + right + bottom


def char_at(p, grid):
  return grid[p.y][p.x]


def is_in_grid(p, grid):
  width = len(grid[0])
  height = len(grid)
  return 0 <= p.x < width and 0 <= p.y < height
