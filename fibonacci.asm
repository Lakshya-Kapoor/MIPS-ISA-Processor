.text
main:
addi $t4,$zero,5
sw $t4,0($t5) #t5 = 0x10010000
lw $s0,0($t5) # n = 5
addi $t0,$zero,0 #t0 = 1 = no. of cycles
addi $t1,$zero,0 #t1 = a = 0
addi $t2,$zero,1 #t2 = b = 1 
target:
	addi $t0,$t0,1
  	beq $s0,$t0,exitloop
  	add $t3,$t2,$t1 #c = a+ b
	add $t1,$t2,$zero #a = b
	add $t2,$t3,$zero #b = c
	j target
exitloop:
sw $t3,4($t5)
