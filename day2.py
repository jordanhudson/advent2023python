from collections import defaultdict


def day2():
  bag = {
    'red': 12,
    'green': 13,
    'blue': 14
  }

  with open('input/day2.txt') as f:
    lines = f.readlines()

  games = [line_to_game(line) for line in lines]

  sum_of_possible_ids = sum(game['id'] for game in games if is_possible(game, bag))
  sum_of_game_power = sum(game['power'] for game in games)

  print('sum_of_possible_ids', sum_of_possible_ids)
  print('sum_of_game_power', sum_of_game_power)


def is_possible(game, bag):
  for reveal in game['reveals']:
    if reveal['count'] > bag[reveal['colour']]:
      return False
  return True


def line_to_game(line):
  game_str, game_raw = line.split(':')
  game_id = int(game_str.split()[1])
  reveals = []
  maxes = defaultdict(lambda: 0)
  for set_str in game_raw.strip().split(';'):
    for cube_str in set_str.strip().split(','):
      (count, colour) = cube_str.strip().split()
      count = int(count)
      if count > maxes[colour]:
        maxes[colour] = count
      reveals.append({'count': count, 'colour': colour})
  power = maxes['green'] * maxes['red'] * maxes['blue']
  return {'id': game_id, 'reveals': reveals, 'power': power}
