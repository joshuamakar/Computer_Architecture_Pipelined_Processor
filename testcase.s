.text
    addi x28, x0, 1024
    addi x1, x0, 3
    addi x2, x0, 9
    addi x3, x0, -45
    addi x4, x0, 29
    addi x5, x0, 5
    addi x6, x0, 37
    addi x7, x0, 19
    addi x8, x0, 41
    addi x9, x0, 3
    # --- Pre-filling memory to prevent X states ---
    sw x1, 0(x28)
    sw x1, 4(x28)
    sw x1, 8(x28)
    sw x1, 12(x28)
    sw x1, 16(x28)
    sw x1, 20(x28)
    sw x1, 24(x28)
    sw x1, 28(x28)
    sw x1, 32(x28)
    sw x1, 36(x28)
    sw x1, 40(x28)
    # --- Begin Random Test ---
    sub x23, x7, x9
    slt x22, x7, x2
    xori x14, x7, -48
    slti x20, x3, 88
    addi x5, x4, 70
    andi x16, x3, -25
    lw x13, 36(x28)
    sub x3, x1, x6
    lw x22, 28(x28)
    lw x7, 24(x28)
    lw x14, 36(x28)
    addi x7, x8, 51
    xori x14, x1, 78
    xor x19, x8, x5
    lw x20, 28(x28)
    sw x8, 12(x28)
    lw x13, 16(x28)
    ori x25, x7, 1
    xori x7, x6, -41
    lw x13, 28(x28)
    xor x8, x9, x4
    ori x3, x8, 17
    sw x5, 40(x28)
    sw x5, 0(x28)
    and x26, x9, x3
    addi x23, x4, -100
    addi x5, x4, -14
    andi x4, x4, 95
    slt x13, x2, x4
    xor x21, x5, x8
    lw x8, 28(x28)
    or x13, x1, x7
    lw x26, 28(x28)
    sw x8, 36(x28)
    lw x24, 20(x28)
    slt x23, x1, x1
    lw x11, 0(x28)
    ori x14, x4, 100
    xor x10, x6, x6
    lw x11, 20(x28)
END_TEST:
    beq x0, x0, END_TEST
