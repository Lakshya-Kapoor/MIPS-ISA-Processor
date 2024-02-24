.text
main:
addi $s0,$zero,5 #s0 = n
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
sw $t3,0x100($zero)
