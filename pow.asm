.text
main :
addi $s0, $zero, 5 # x = 5
addi $s1, $zero, 4 # n = 4
addi $t0, $zero, 1 # y = 1
loop:
    beq $s1, $zero, exitloop
        andi $t1, $s1, 1
        bne $s1, $t1, target
            mul $t0, $t0, $s0
        target:
            mul $s0, $s0, $s0
            srl $s1, $s1, 1 
exitloop:
    sw $t0, 0x10010100($zero)