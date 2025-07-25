import curses
from random import randint

# Setup window
s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
sh -= 1  # reduce height by 1 to stay within bounds
sw -= 1  # reduce width by 1
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

# Initial snake setup
snk_x = sw // 4
snk_y = sh // 2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1],
    [snk_y, snk_x - 2]
]

# Place first food
food = [sh // 2, sw // 2]
w.addch(food[0], food[1], curses.ACS_PI)

# Initial direction
key = curses.KEY_RIGHT

while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key

    # Calculate new head position
    new_head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    elif key == curses.KEY_UP:
        new_head[0] -= 1
    elif key == curses.KEY_LEFT:
        new_head[1] -= 1
    elif key == curses.KEY_RIGHT:
        new_head[1] += 1

    snake.insert(0, new_head)

    # Game over if snake hits wall or itself
    if (new_head[0] <= 0 or new_head[0] >= sh or
        new_head[1] <= 0 or new_head[1] >= sw or
        new_head in snake[1:]):
        curses.endwin()
        print("Game Over!")
        quit()

    # Handle food consumption
    if new_head == food:
        food = None
        while food is None:
            nf = [randint(1, sh - 2), randint(1, sw - 2)]
            if nf not in snake:
                food = nf
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        # Safely clear the tail position
        if 0 < tail[0] < sh and 0 < tail[1] < sw:
            w.addch(tail[0], tail[1], ' ')

    # Safely draw the new head
    if 0 < new_head[0] < sh and 0 < new_head[1] < sw:
        w.addch(new_head[0], new_head[1], '#')
