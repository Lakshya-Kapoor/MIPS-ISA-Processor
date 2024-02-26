.text
main :
addi $t4,$zero,5
sw $t4,0($t5) #t5 = 0x10010000
lw $s0,0($t5) # n = 5
addi $t6,$zero,4
sw $t6, 8($t5)
lw $s1, 8($t5) # n = 4
addi $t0, $zero, 1 # y = 1
loop:
    beq $s1, $zero, exitloop
        andi $t1, $s1, 1
        beq $zero, $t1, target
            mul $t0, $t0, $s0
        target:
            mul $s0, $s0, $s0
            srl $s1, $s1, 1 
    j loop
exitloop:
    sw $t0, 4($t5)