import random
import subprocess
import os

# --- PATH FIX ---
# This forces the script to look for the jar file in the exact same folder the script is located in.
script_dir = os.path.dirname(os.path.abspath(__file__))
rars_path = os.path.join(script_dir, "rars1_6.jar")
s_file_path = os.path.join(script_dir, "testcase.s")
hex_file_path = os.path.join(script_dir, "testcase.hex")
# ----------------

asm = [".text"]
safe_sources = [f'x{i}' for i in range(1, 10)] 
all_destinations = [f'x{i}' for i in range(1, 28)]

asm.append("    addi x28, x0, 1024")

for i in range(1, 10):
    asm.append(f"    addi x{i}, x0, {random.randint(-50, 50)}")

asm.append("    # --- Pre-filling memory to prevent X states ---")
for i in range(0, 44, 4):
    asm.append(f"    sw x1, {i}(x28)")
asm.append("    # --- Begin Random Test ---")

for _ in range(40):
    rd = random.choice(all_destinations)
    rs1 = random.choice(safe_sources)
    rs2 = random.choice(safe_sources)
    
    category = random.choice([0, 1, 2])
    
    if category == 0: 
        op = random.choice(['add', 'sub', 'and', 'or', 'slt', 'xor'])
        asm.append(f"    {op} {rd}, {rs1}, {rs2}")
        
    elif category == 1: 
        op = random.choice(['addi', 'andi', 'ori', 'slti', 'xori'])
        asm.append(f"    {op} {rd}, {rs1}, {random.randint(-100, 100)}")
        
    else: 
        op = random.choice(['lw', 'sw'])
        offset = random.choice([i * 4 for i in range(11)]) 
        if op == 'sw':
            asm.append(f"    sw {rs1}, {offset}(x28)") 
        else:
            asm.append(f"    lw {rd}, {offset}(x28)") 

asm.append("END_TEST:")
asm.append("    beq x0, x0, END_TEST")

with open(s_file_path, "w") as f:
    f.write('\n'.join(asm) + '\n')

subprocess.run(["java", "-jar", rars_path, "a", "dump", ".text", "HexText", hex_file_path, s_file_path])
print("Safe testcase generated successfully!")