#!/usr/bin/env python3
"""
Core Visualizer for PyCorewar
Provides real-time text-based visualization of warrior execution
"""

import Corewar
import time
import os
import sys


class CoreVisualizer:
    """Text-based core visualization for PyCorewar debugging"""
    
    def __init__(self, coresize=100, maxprocesses=100, maxcycles=1000):
        self.mars = Corewar.Debugging.MARS88(
            coresize=coresize, 
            maxprocesses=maxprocesses, 
            maxcycles=maxcycles
        )
        self.coresize = coresize
        self.step_count = 0
        self.max_steps = maxcycles * 2
        
        # Visualization symbols
        self.symbols = {
            'empty': '.',      # Empty core cell
            'warrior1': 'A',   # Warrior 1 code
            'warrior2': 'B',   # Warrior 2 code
            'pc1': '1',        # Warrior 1 program counter
            'pc2': '2',        # Warrior 2 program counter
            'both': 'X',       # Both warriors occupy same cell
            'read': 'r',       # Recently read location
            'write': 'w',      # Recently written location
            'exec': '*',       # Currently executing location
        }
        
        # Track warrior positions for coloring
        self.warrior_positions = {0: set(), 1: set()}
        self.recent_reads = set()
        self.recent_writes = set()
        
    def load_warriors(self, warrior_files, positions=None):
        """Load warriors from files"""
        parser = Corewar.Parser(standard=Corewar.STANDARD_88)
        
        for i, filename in enumerate(warrior_files):
            try:
                warrior = parser.parse_file(filename)
                pos = positions[i] if positions else i * (self.coresize // len(warrior_files))
                self.mars.load(warrior, pos)
                
                # Track initial warrior positions
                for j in range(warrior.length):
                    self.warrior_positions[i].add((pos + j) % self.coresize)
                    
                print(f"Loaded {warrior.name} by {warrior.author} at position {pos}")
                
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                return False
        return True
    
    def get_cell_symbol(self, address):
        """Determine symbol for a core cell"""
        # Check if currently executing
        if hasattr(self.mars, '_MARS88__execLoc') and self.mars._MARS88__execLoc == address:
            return self.symbols['exec']
            
        # Check for program counters
        pc_count = 0
        pc_warriors = []
        for warrior_id in range(self.mars.numWarriors):
            if hasattr(self.mars.pqueues[warrior_id], '_ProcessQueue__head'):
                for pc in self.mars.pqueues[warrior_id]._ProcessQueue__head:
                    if pc == address:
                        pc_count += 1
                        pc_warriors.append(warrior_id)
        
        if pc_count > 1:
            return self.symbols['both']
        elif pc_count == 1:
            return self.symbols[f'pc{pc_warriors[0] + 1}']
            
        # Check recent activity
        if address in self.recent_writes:
            return self.symbols['write']
        if address in self.recent_reads:
            return self.symbols['read']
            
        # Check warrior code presence
        warriors_here = []
        for warrior_id in range(2):
            if address in self.warrior_positions.get(warrior_id, set()):
                warriors_here.append(warrior_id)
                
        if len(warriors_here) > 1:
            return self.symbols['both']
        elif len(warriors_here) == 1:
            return self.symbols[f'warrior{warriors_here[0] + 1}']
            
        # Check if cell has non-zero content
        if (self.mars.core[address].opcode != Corewar.OPCODE_DAT or 
            self.mars.core[address].afield != 0 or 
            self.mars.core[address].bfield != 0):
            return '?'  # Unknown code
            
        return self.symbols['empty']
    
    def draw_core(self, width=50):
        """Draw the core as a grid"""
        print(f"\n{'='*60}")
        print(f"Step {self.step_count:4d} | Warrior {self.mars.warrior + 1} executing")
        print(f"{'='*60}")
        
        # Draw core as rectangular grid
        height = (self.coresize + width - 1) // width
        
        for row in range(height):
            line = ""
            for col in range(width):
                addr = row * width + col
                if addr < self.coresize:
                    line += self.get_cell_symbol(addr)
                else:
                    line += " "
            print(f"{row*width:4d}: {line}")
        
        # Show legend
        print(f"\nLegend: {self.symbols['empty']}=empty {self.symbols['warrior1']}=warrior1 {self.symbols['warrior2']}=warrior2")
        print(f"        {self.symbols['pc1']}=PC1 {self.symbols['pc2']}=PC2 {self.symbols['exec']}=executing {self.symbols['write']}=write {self.symbols['read']}=read")
        
        # Show current instruction
        if hasattr(self.mars, '_MARS88__execInsn'):
            print(f"\nExecuting: {self.mars._MARS88__execInsn}")
        
        # Show process queue status
        for i in range(self.mars.numWarriors):
            count = len(self.mars.pqueues[i])
            print(f"Warrior {i+1}: {count} processes")
    
    def update_tracking(self):
        """Update tracking of reads/writes"""
        # Clear old tracking
        self.recent_reads.clear()
        self.recent_writes.clear()
        
        # Track recent activity (if available)
        if hasattr(self.mars, '_MARS88__readLoc'):
            self.recent_reads.update(self.mars._MARS88__readLoc)
        if hasattr(self.mars, '_MARS88__writeLoc'):
            self.recent_writes.update(self.mars._MARS88__writeLoc)
    
    def run_visualization(self, delay=0.5, max_steps=None):
        """Run the visualization with stepping"""
        if max_steps:
            self.max_steps = max_steps
            
        print("Starting Core War visualization...")
        print("Press Ctrl+C to stop, or Enter to step manually")
        
        try:
            while self.step_count < self.max_steps:
                # Clear screen (works on most terminals)
                os.system('clear' if os.name == 'posix' else 'cls')
                
                # Update tracking and draw
                self.update_tracking()
                self.draw_core()
                
                # Check if fight is over
                alive_warriors = sum(1 for i in range(self.mars.numWarriors) 
                                   if len(self.mars.pqueues[i]) > 0)
                if alive_warriors <= 1:
                    print(f"\nFight ended! Warrior {self.get_winner()} wins!")
                    break
                
                # Wait for user input or delay
                if delay == 0:
                    input("\nPress Enter to step...")
                else:
                    time.sleep(delay)
                
                # Execute one step
                try:
                    self.mars.step()
                    self.step_count += 1
                except:
                    print("Execution ended")
                    break
                    
        except KeyboardInterrupt:
            print("\n\nVisualization stopped by user")
    
    def get_winner(self):
        """Determine the winner"""
        for i in range(self.mars.numWarriors):
            if len(self.mars.pqueues[i]) > 0:
                return i + 1
        return "None"


def main():
    """Main function for core visualization"""
    if len(sys.argv) < 3:
        print("Usage: python3 core_visualizer.py <warrior1.red> <warrior2.red> [coresize]")
        print("Example: python3 core_visualizer.py warriors/Test/parser_001.red warriors/Test/parser_002.red 100")
        return
    
    # Parse arguments
    warrior1 = sys.argv[1]
    warrior2 = sys.argv[2]
    coresize = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    
    # Create visualizer
    viz = CoreVisualizer(coresize=coresize, maxprocesses=coresize, maxcycles=10000)
    
    # Load warriors
    if not viz.load_warriors([warrior1, warrior2]):
        return
    
    # Run visualization
    print(f"\nStarting visualization with core size {coresize}")
    print("Choose mode:")
    print("1. Manual stepping (press Enter)")
    print("2. Automatic with delay")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        viz.run_visualization(delay=0)
    else:
        delay = float(input("Enter delay in seconds (e.g., 0.5): ") or "0.5")
        viz.run_visualization(delay=delay)


if __name__ == "__main__":
    main()
