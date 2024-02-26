.text
main:
addi $t4,$zero,5
sw $t4,0($t5) # t5 = 0x10010000
lw $s0,0($t5) # n = 5
addi $s1,$s0,1 
addi $t0,$zero,1 # fact = 1 
addi $t1,$zero,1 # i = 1 
target:
	beq $s1,$t1,exitloop
	mul $t0,$t0,$t1
	addi $t1,$t1,1
	j target

exitloop:
	sw $t0,4($t5)
