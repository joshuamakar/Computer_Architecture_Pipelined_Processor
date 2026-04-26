# femtoRV32 — Pipelined RISC-V Processor
**CSCE 3301 — Computer Architecture | Spring 2026 | Project 1**

---

## Overview

femtoRV32 is a pipelined RV32I+M processor implemented in Verilog and deployed on the **Nexys A7 FPGA**. It executes the full RISC-V base integer instruction set (RV32I) and, as a bonus, the **M-extension** (integer multiply/divide).

---

## Architecture

- **3-stage pipeline:** IF/ID → EX/MEM → WB
- **2 clocks per stage** using a toggle register — effective CPI = 2
- **Single shared memory** (1024 words) for both instructions and data, time-multiplexed via the toggle signal
- **Memory split:** instructions occupy words 0–511 (`0x0000`–`0x07FC`); data is offset to words 512–1023 (`0x0800`–`0x0FFC`) to prevent overlap
- **Forwarding unit** handles data hazards (MEM/WB → ID/EX), sufficient for the every-other-cycle issue rate
- **Branch resolution** in EX stage with pipeline flush on taken branches

---

## Supported Instructions

| Category | Instructions |
|---|---|
| R-type | ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, SLT, SLTU |
| I-type Arithmetic | ADDI, ANDI, ORI, XORI, SLTI, SLTIU, SLLI, SRLI, SRAI |
| Load | LB, LH, LW, LBU, LHU |
| Store | SB, SH, SW |
| Branch | BEQ, BNE, BLT, BGE, BLTU, BGEU |
| Jump | JAL, JALR |
| Upper Immediate | LUI, AUIPC |
| Halt | FENCE, ECALL |
| **Bonus: M-extension** | **MUL, MULH, MULHU, MULHSU, DIV, DIVU, REM, REMU** |

Up to **512 instructions** can be loaded into the instruction section of memory.

---

## Module Descriptions

| File | Description |
|---|---|
| `CPU.v` | Top-level module; pipeline registers, PC logic, control wiring |
| `Memory.v` | Single synchronous memory (1024 × 32-bit words); holds instructions and data |
| `CU.v` | Main control unit; decodes opcode into control signals |
| `ALU_CU.v` | ALU control unit; maps ALUOp + funct3/funct7 to ALU select |
| `ALU.v` | 32-bit ALU; supports all RV32I operations plus M-extension multiply/divide |
| `ImmGen.v` | Immediate generator; handles I/S/B/U/J-type encodings |
| `RF.v` | 32-entry × 32-bit register file with synchronous write, async read |
| `Forwarding_Unit.v` | Detects and resolves RAW hazards via forwarding |
| `Load_Formatter.v` | Sign/zero-extends loaded bytes and halfwords |
| `Store_Formatter.v` | Generates byte-enable mask and aligns store data |
| `NbitReg.v` | Parameterized pipeline register with enable and reset |
| `Nbit_shift.v` | Left-shift by 1 for branch/jump target calculation |

---

## Bonus: M-Extension (Multiply / Divide)

Full RV32M support was added as a bonus on top of the base RV32I implementation.

**Supported operations and edge cases handled:**

- `MUL` — lower 32 bits of signed × signed
- `MULH` — upper 32 bits of signed × signed
- `MULHU` — upper 32 bits of unsigned × unsigned
- `MULHSU` — upper 32 bits of signed × unsigned
- `DIV` / `DIVU` — signed and unsigned division, truncated toward zero
- `REM` / `REMU` — signed and unsigned remainder
- **Divide-by-zero:** DIV/DIVU return `0xFFFFFFFF`; REM/REMU return the dividend
- **Signed overflow** (`MIN_INT / -1`): DIV returns `MIN_INT`, REM returns `0`

Detection is done via `inst[25]` (the M-extension bit) in `ALU_CU.v`, with no changes required to the main control unit.

---

## Bonus: Test Case Generator

A test case generator was developed to automatically produce RISC-V machine code for verifying processor correctness. It generates instruction encodings along with the expected register output for each operation, covering normal cases, boundary values, and edge cases (divide-by-zero, signed overflow, etc.), making it straightforward to load new test programs into `Memory.v` and validate results.

---

## FPGA I/O

| Signal | Direction | Description |
|---|---|---|
| `clk` | Input | Board clock |
| `rst` | Input | Synchronous reset |
| `ledSel[1:0]` | Input | Selects what to display on LEDs |
| `SSD[3:0]` | Input | Selects value to show on 7-segment display |
| `LEDs[15:0]` | Output | Shows instruction word or control signals |
| `LED_out[6:0]` | Output | 7-segment segments |
| `Anode[3:0]` | Output | 7-segment digit select |

**LED display modes (`ledSel`):**
- `00` — `if_id_inst[15:0]`
- `01` — `if_id_inst[31:16]`
- `10` — control signals

**SSD display modes (`SSD`):** PC, nxtPC, branch target, PC_input, rs1, rs2, writeback, immediate, shifted immediate, ALU input 2, ALU result, data memory output.

---

## Known Limitations

- CPI = 2 due to single-memory time-multiplexing (one cycle for instruction fetch, one for data access)
- No cache; all memory accesses take one clock cycle
- No exception handling beyond FENCE/ECALL halt detection
