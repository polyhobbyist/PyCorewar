#!/usr/bin/env python3
"""
Simple Core Monitor - extends pymars with visualization capabilities
"""

import Corewar
import sys
import time


def visualize_core(mars, step_num, width=40):
    """Simple core visualization function"""
    coresize = mars.coresize
    
    print(f"\n{'='*50}")
    print(f"Step {step_num:4d}")
    print(f"{'='*50}")
    
    # Create a simple grid view
    height = (coresize + width - 1) // width
    
    for row in range(height):
        line = ""
        for col in range(width):
            addr = row * width + col
            if addr < coresize:
                # Get cell content
                cell = mars.core[addr]
                
                # Determine symbol based on content
                if cell.opcode == Corewar.OPCODE_DAT and cell.afield == 0 and cell.bfield == 0:
                    symbol = '.'  # Empty
                elif cell.opcode == Corewar.OPCODE_MOV:
                    symbol = 'M'  # Move instruction
                elif cell.opcode == Corewar.OPCODE_ADD:
                    symbol = '+'  # Add instruction
                elif cell.opcode == Corewar.OPCODE_SUB:
                    symbol = '-'  # Sub instruction
                elif cell.opcode == Corewar.OPCODE_JMP:
                    symbol = 'J'  # Jump instruction
                elif cell.opcode == Corewar.OPCODE_JMZ:
                    symbol = 'Z'  # Jump if zero
                elif cell.opcode == Corewar.OPCODE_JMN:
                    symbol = 'N'  # Jump if not zero
                elif cell.opcode == Corewar.OPCODE_CMP:
                    symbol = 'C'  # Compare
                elif cell.opcode == Corewar.OPCODE_SPL:
                    symbol = 'S'  # Split
                elif cell.opcode == Corewar.OPCODE_DAT:
                    symbol = 'D'  # Data
                else:
                    symbol = '?'  # Unknown
                    
                line += symbol
            else:
                line += " "
                
        print(f"{row*width:4d}: {line}")
    
    print(f"\nLegend: .=empty M=MOV +=ADD -=SUB J=JMP Z=JMZ N=JMN C=CMP S=SPL D=DAT")


def run_debug_fight(warrior1_file, warrior2_file, coresize=100):
    """Run a fight with step-by-step visualization"""
    
    # Create MARS instance
    mars = Corewar.Debugging.MARS88(coresize=coresize, maxprocesses=coresize, maxcycles=10000)
    
    # Parse warriors
    parser = Corewar.Parser(standard=Corewar.STANDARD_88)
    
    try:
        warrior1 = parser.parse_file(warrior1_file)
        warrior2 = parser.parse_file(warrior2_file)
        
        print(f"Loaded: {warrior1.name} vs {warrior2.name}")
        
        # Load warriors into core
        mars.load(warrior1, 0)
        mars.load(warrior2, coresize // 2)
        
        print(f"Warriors loaded. Core size: {coresize}")
        print("Press Enter to step through execution, or 'a' for auto mode")
        
        step_count = 0
        auto_mode = False
        
        while step_count < 1000:  # Limit steps to prevent infinite loops
            # Show current core state
            visualize_core(mars, step_count)
            
            # Check if fight is over
            alive_warriors = sum(1 for i in range(mars.numWarriors) if len(mars.pqueues[i]) > 0)
            if alive_warriors <= 1:
                winner = None
                for i in range(mars.numWarriors):
                    if len(mars.pqueues[i]) > 0:
                        winner = i + 1
                        break
                        
                if winner:
                    print(f"\nFight ended! Warrior {winner} wins after {step_count} steps!")
                else:
                    print(f"\nFight ended in a tie after {step_count} steps!")
                break
            
            # Get user input for stepping
            if not auto_mode:
                user_input = input(f"\nStep {step_count + 1} [Enter to step, 'a' for auto, 'q' to quit]: ").strip().lower()
                if user_input == 'q':
                    break
                elif user_input == 'a':
                    auto_mode = True
                    delay = float(input("Enter delay between steps (seconds): ") or "0.5")
            else:
                time.sleep(delay)
            
            # Execute one step
            try:
                mars.step()
                step_count += 1
            except Exception as e:
                print(f"Execution error: {e}")
                break
                
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 simple_visualizer.py <warrior1.red> <warrior2.red> [coresize]")
        sys.exit(1)
    
    warrior1 = sys.argv[1]
    warrior2 = sys.argv[2]
    coresize = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    
    run_debug_fight(warrior1, warrior2, coresize)
