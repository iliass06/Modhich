# a_maze_ing.py
import sys
from typing import Dict
from mazegen.generator import MazeGenerator
import visualizer

def parse_config(filepath: str) -> Dict[str, str]:
    """Parses the configuration file."""
    config = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip().upper()] = value.strip() # .upper() pour ignorer la casse
    except FileNotFoundError:
        print(f"Error: Configuration file {filepath} not found.")
        sys.exit(1)
    return config

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config = parse_config(sys.argv[1])
    
    try:
        width = int(config.get('WIDTH', 20))
        height = int(config.get('HEIGHT', 15))
        entry_str = config.get('ENTRY', '0,0').split(',')
        exit_str = config.get('EXIT', f'{width-1},{height-1}').split(',')
        entry = (int(entry_str[0]), int(entry_str[1]))
        exit_coords = (int(exit_str[0]), int(exit_str[1]))
        output_file = config.get('OUTPUT_FILE', 'maze.txt')
        
        # Gère 'True', 'true', 'TRUE', etc.
        perfect = config.get('PERFECT', 'True').lower() == 'true'
        
        # Récupère le SEED s'il existe
        seed_str = config.get('SEED')
        seed_val = int(seed_str) if seed_str is not None else None

    except (ValueError, IndexError):
        print("Error: Invalid configuration format.")
        sys.exit(1)

    # On passe le seed_val au générateur
    generator = MazeGenerator(width, height, perfect, seed=seed_val)
    generator.generate(entry, exit_coords)
    generator.save_to_file(output_file, entry, exit_coords)
    
    visualizer.interactive_loop(generator, entry, exit_coords)

if __name__ == "__main__":
    main()