# mazegen/generator.py
import random
from typing import List, Tuple, Optional
from collections import deque

class MazeGenerator:
    def __init__(self, width: int, height: int, perfect: bool = True, seed: Optional[int] = None) -> None:
        self.width = width
        self.height = height
        self.perfect = perfect
        if seed is not None:
            random.seed(seed)
        self.grid: List[List[int]] = [[15 for _ in range(width)] for _ in range(height)]
        self.visited: List[List[bool]] = [[False for _ in range(width)] for _ in range(height)]
        self.solution_path: str = ""

    def _carve_42(self) -> None:
        if self.width < 10 or self.height < 8:
            return

        cx = self.width // 2 - 3
        cy = self.height // 2 - 2

        pattern_42 = [
            (0,0), (0,1), (0,2), (0,3),
            (1,3),
            (2,0), (2,1), (2,2), (2,3), (2,4),
            (4,0), (5,0), (6,0),
            (6,1),
            (4,2), (5,2), (6,2),
            (4,3),
            (4,4), (5,4), (6,4)
        ]

        for dx, dy in pattern_42:
            x, y = cx + dx, cy + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.visited[y][x] = True
                self.grid[y][x] = 15

    def _carve_passages_from(self, cx: int, cy: int) -> None:
        self.visited[cy][cx] = True
        directions = [(0, -1, 1, 4, 'N'), (1, 0, 2, 8, 'E'), (0, 1, 4, 1, 'S'), (-1, 0, 8, 2, 'W')]
        random.shuffle(directions)
        
        for dx, dy, wall, opposite_wall, _ in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and not self.visited[ny][nx]:
                self.grid[cy][cx] &= ~wall
                self.grid[ny][nx] &= ~opposite_wall
                self._carve_passages_from(nx, ny)

    def solve_bfs(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        queue = deque([(start[0], start[1], "")])
        visited = set([(start[0], start[1])])
        
        while queue:
            x, y, path = queue.popleft()
            if (x, y) == end:
                self.solution_path = path
                return
                
            cell = self.grid[y][x]
            moves = [(0, -1, 1, 'N'), (1, 0, 2, 'E'), (0, 1, 4, 'S'), (-1, 0, 8, 'W')]
            for dx, dy, wall, dir_char in moves:
                nx, ny = x + dx, y + dy
                if (cell & wall) == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + dir_char))

    def generate(self, entry: Tuple[int, int], exit_coords: Tuple[int, int]) -> None:
        self._carve_42()
        self._carve_passages_from(entry[0], entry[1])
        self.solve_bfs(entry, exit_coords)

    def save_to_file(self, filename: str, entry: Tuple[int, int], exit_coords: Tuple[int, int]) -> None:
        try:
            with open(filename, 'w') as f:
                for row in self.grid:
                    line = "".join([f"{cell:X}" for cell in row])
                    f.write(line + "\n")
                f.write("\n")
                f.write(f"{entry[0]},{entry[1]}\n")
                f.write(f"{exit_coords[0]},{exit_coords[1]}\n")
                f.write(f"{self.solution_path}\n")
        except IOError as e:
            print(f"File writing error: {e}")