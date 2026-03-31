# a_maze_ing.py [cite: 113]
import sys
from typing import Dict
from mazegen.generator import MazeGenerator # [cite: 220]
import visualizer

def parse_config(filepath: str) -> Dict[str, str]:
    """Parses the configuration file. [cite: 118]"""
    config = {}
    try:
        with open(filepath, 'r') as f: # [cite: 75]
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): # [cite: 120]
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip() # [cite: 119]
    except FileNotFoundError: # [cite: 74, 116]
        print(f"Error: Configuration file {filepath} not found.")
        sys.exit(1)
    return config

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt [cite: 112]")
        sys.exit(1)

    config = parse_config(sys.argv[1])
    
    try:
        width = int(config.get('WIDTH', 20)) # [cite: 122]
        height = int(config.get('HEIGHT', 15)) # [cite: 122]
        entry_str = config.get('ENTRY', '0,0').split(',')
        exit_str = config.get('EXIT', f'{width-1},{height-1}').split(',')
        entry = (int(entry_str[0]), int(entry_str[1])) # [cite: 122]
        exit_coords = (int(exit_str[0]), int(exit_str[1])) # [cite: 122]
        output_file = config.get('OUTPUT_FILE', 'maze.txt') # [cite: 122]
        perfect = config.get('PERFECT', 'True') == 'True' # [cite: 122]
    except (ValueError, IndexError): # [cite: 116]
        print("Error: Invalid configuration format.")
        sys.exit(1)

    generator = MazeGenerator(width, height, perfect) # [cite: 219]
    generator.generate(entry, exit_coords)
    generator.save_to_file(output_file, entry, exit_coords) # [cite: 146]
    
    visualizer.interactive_loop(generator, entry, exit_coords) # [cite: 192]

if __name__ == "__main__":
    main()