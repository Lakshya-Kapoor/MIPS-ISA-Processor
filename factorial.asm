.text
main:
addi $s0,$zero,5
sw $s0,0x10010000($zero) # M[24] = n
addi $s1,$s0,1 
addi $t0,$zero,1 #fact = 1 
addi $t1,$zero,1 #i = 1 
target:
	beq $s1,$t1,exitloop
	mul $t0,$t0,$t1
	add $t1,$t1,1
	j target

exitloop:
	sw $t0,0x10010100($zero) 
