# visualizer.py
import sys
from typing import Tuple
from mazegen.generator import MazeGenerator

RESET = "\033[0m"
WALL_COLORS = ["\033[97m", "\033[93m", "\033[94m", "\033[96m"]
ENTRY_COLOR = "\033[95m"
EXIT_COLOR = "\033[91m"
PATH_COLOR = "\033[96m"
PATTERN_COLOR = "\033[37m"

def print_maze(generator: MazeGenerator, entry: Tuple[int, int], exit_coords: Tuple[int, int], show_path: bool, color_idx: int) -> None:
    h = generator.height * 2 + 1
    w = generator.width * 2 + 1
    
    display = [['██' for _ in range(w)] for _ in range(h)]
    wall_c = WALL_COLORS[color_idx % len(WALL_COLORS)]

    for y in range(generator.height):
        for x in range(generator.width):
            dy = y * 2 + 1
            dx = x * 2 + 1
            cell = generator.grid[y][x]

            if cell == 15 and (x, y) not in [entry, exit_coords]:
                display[dy][dx] = '42'
            else:
                display[dy][dx] = '  '
                
            if (cell & 1) == 0: display[dy - 1][dx] = '  '
            if (cell & 2) == 0: display[dy][dx + 1] = '  '
            if (cell & 4) == 0: display[dy + 1][dx] = '  '
            if (cell & 8) == 0: display[dy][dx - 1] = '  '

    for y in range(generator.height):
        for x in range(generator.width):
            dy = y * 2 + 1
            dx = x * 2 + 1
            if display[dy][dx] == '42':
                if x + 1 < generator.width and display[dy][dx + 2] == '42':
                    display[dy][dx + 1] = '  '
                if y + 1 < generator.height and display[dy + 2][dx] == '42':
                    display[dy + 1][dx] = '  '
                if x + 1 < generator.width and y + 1 < generator.height:
                    if display[dy][dx+2] == '42' and display[dy+2][dx] == '42' and display[dy+2][dx+2] == '42':
                        display[dy+1][dx+1] = '  '

    for y in range(h):
        for x in range(w):
            if display[y][x] == '██':
                display[y][x] = f"{wall_c}██{RESET}"
            elif display[y][x] == '42':
                display[y][x] = f"{PATTERN_COLOR}██{RESET}"

    display[entry[1] * 2 + 1][entry[0] * 2 + 1] = f"{ENTRY_COLOR}██{RESET}"
    display[exit_coords[1] * 2 + 1][exit_coords[0] * 2 + 1] = f"{EXIT_COLOR}██{RESET}"

    if show_path and generator.solution_path:
        cx, cy = entry
        for move in generator.solution_path:
            if (cx, cy) != entry and (cx, cy) != exit_coords:
                display[cy * 2 + 1][cx * 2 + 1] = f"{PATH_COLOR}██{RESET}"
            
            if move == 'N':
                display[cy * 2][cx * 2 + 1] = f"{PATH_COLOR}██{RESET}"
                cy -= 1
            elif move == 'S':
                display[cy * 2 + 2][cx * 2 + 1] = f"{PATH_COLOR}██{RESET}"
                cy += 1
            elif move == 'E':
                display[cy * 2 + 1][cx * 2 + 2] = f"{PATH_COLOR}██{RESET}"
                cx += 1
            elif move == 'W':
                display[cy * 2 + 1][cx * 2] = f"{PATH_COLOR}██{RESET}"
                cx -= 1
                
        if (cx, cy) != entry and (cx, cy) != exit_coords:
            display[cy * 2 + 1][cx * 2 + 1] = f"{PATH_COLOR}██{RESET}"

    print("\n")
    for row in display:
        print("".join(row))

def interactive_loop(generator: MazeGenerator, entry: Tuple[int, int], exit_coords: Tuple[int, int]) -> None:
    show_path = False
    color_idx = 0
    
    while True:
        print_maze(generator, entry, exit_coords, show_path, color_idx)
        print("==== A-Maze-ing ====")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        
        choice = input("Choice? (1-4): ")
        
        if choice == '1':
            generator = MazeGenerator(generator.width, generator.height, generator.perfect)
            generator.generate(entry, exit_coords)
        elif choice == '2':
            show_path = not show_path
        elif choice == '3':
            color_idx += 1
        elif choice == '4':
            sys.exit(0)