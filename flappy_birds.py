import curses
from curses.textpad import rectangle
import time
import random

def main(scr):
  curses.curs_set(0)
  scr.nodelay(1)

  HEIGHT, WIDTH = scr.getmaxyx()
  MARGIN = 3
  GAP_WIDTH = 3
  INTER_GAP_WIDTH = 15
  FLAPPY_BIRD = '@'
  PIPE_COLOR = 1
  FLAPPY_COLOR = 2

  curses.init_pair(PIPE_COLOR, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(FLAPPY_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)

  game_difficulty = 200
  scr.timeout(game_difficulty)

  pipe = []
  x = WIDTH // 2
  while x < WIDTH - MARGIN:
    gap_start = random.randint(MARGIN + 1, HEIGHT - MARGIN - GAP_WIDTH)
    pipe.append((x, gap_start))
    x += INTER_GAP_WIDTH

  rectangle(scr, MARGIN, MARGIN, HEIGHT - MARGIN, WIDTH - MARGIN)
  
  flappy_y, flappy_x = HEIGHT // 2, WIDTH // 4

  score_text = 'Score: {}'
  score = 0

  loop_cntr = 0
  while True:

    game_text = score_text.format(score)
    game_text_y, game_text_x = 1, (WIDTH - len(game_text)) // 2
    scr.addstr(game_text_y, game_text_x, game_text)

    if loop_cntr == INTER_GAP_WIDTH:
      gap_start = random.randint(MARGIN + 1, HEIGHT - MARGIN - GAP_WIDTH)
      pipe.append((pipe[-1][0] + INTER_GAP_WIDTH, gap_start))
      loop_cntr = 0
      game_difficulty = max(1, game_difficulty - 5)
      scr.timeout(game_difficulty)

    obstructions = set()

    for x, gap_start in pipe:
      if flappy_x == x:
        score += 1
      for y in range(MARGIN + 1, HEIGHT - MARGIN):
        if y not in range(gap_start, gap_start + GAP_WIDTH):
          scr.attron(curses.color_pair(PIPE_COLOR))
          scr.addstr(y, x, '| ')
          scr.attroff(curses.color_pair(PIPE_COLOR))
          obstructions.add((y, x))
    pipe = [(x - 1, gap_start) for x, gap_start in pipe if x > MARGIN]

    scr.attron(curses.color_pair(FLAPPY_COLOR))
    scr.addstr(flappy_y, flappy_x, FLAPPY_BIRD)
    scr.attroff(curses.color_pair(FLAPPY_COLOR))
    scr.refresh()
    key = scr.getch()
    
    if flappy_y in [MARGIN, HEIGHT - MARGIN] or \
      (flappy_y, flappy_x) in obstructions:
      if (flappy_y, flappy_x) in obstructions:
        score -= 1
      game_text = f'GAME OVER. Score: {score}'
      game_text_y, game_text_x = 1, (WIDTH - len(game_text)) // 2
      spaces = ' ' * WIDTH
      scr.addstr(1, 0, spaces)
      scr.addstr(game_text_y, game_text_x, game_text)
      scr.refresh()
      scr.timeout(-1)
      scr.getch()
      break
    
    if key == 27: # Esc
      break
    scr.addstr(flappy_y, flappy_x, ' ')
    if key == curses.KEY_UP:
      flappy_y -= 1
    else:
      flappy_y += 1
    
    loop_cntr += 1

curses.wrapper(main)