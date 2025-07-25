import curses
from random import randint

# Initialize screen
s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()

# Clamp size to avoid edge writing
sh = min(sh, 20)
sw = min(sw, 60)

w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(150)

# Initial snake position near center
snk_x = sw // 2
snk_y = sh // 2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1],
    [snk_y, snk_x - 2]
]

# Initial food
food = [randint(1, sh - 2), randint(1, sw - 2)]
w.addch(food[0], food[1], curses.ACS_PI)

key = curses.KEY_RIGHT

while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key

    # Move head
    head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_DOWN:
        head[0] += 1
    elif key == curses.KEY_UP:
        head[0] -= 1
    elif key == curses.KEY_LEFT:
        head[1] -= 1
    elif key == curses.KEY_RIGHT:
        head[1] += 1

    snake.insert(0, head)

    # Game over on boundary or self collision
    if (head[0] <= 0 or head[0] >= sh - 1 or
        head[1] <= 0 or head[1] >= sw - 1 or
        head in snake[1:]):
        curses.endwin()
        print("Game Over!")
        quit()

    # Eat food
    if head == food:
        while True:
            nf = [randint(1, sh - 2), randint(1, sw - 2)]
            if nf not in snake:
                food = nf
                break
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ')

    # Draw head
    w.addch(head[0], head[1], '#')
