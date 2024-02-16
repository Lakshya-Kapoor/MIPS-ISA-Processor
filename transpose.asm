.text
main :
addi $s0,$zero,3 #s0 = n
addi $t0,$zero,0 #t0 = i
mul $s1,$s0,4 #s1 = 4*n
mul $s2,$s1,$s0 #s2 = 4*n*n
addi $t2,$zero,1 #t2 = counter
addi $s3,$zero,0x10010000 #s3 = address to use 
outer_loop:
	beq $t0,$s2,exit_loop
	addi $t1,$zero,0 #t1 = j
	inner_loop:
		beq $t1,$s1,small_exit
		add $t4,$t0,$t1 #t4 = i+j
		add $t4,$t4,$s3
		sw $t2,0($t4)
		addi $t1,$t1,4 #t1 = t1+4
		addi $t2,$t2,1 #t2 = t2+1
		j inner_loop
	small_exit:
		add $t0,$t0,$s1 #t0 = t0+4*n
		j outer_loop
	
exit_loop:
	outer_loop_1:
	beq $t0,$s2,exit
	addi $t1,$zero,0 #t1 = j
	inner_loop_1:
		beq $t1,$s1,small_exit_1
		add $t4,$t0,$t1 #t4 = i+j
		add $t4,$t4,$s3
		sw $t2,0($t4)
		addi $t1,$t1,4 #t1 = t1+4
		addi $t2,$t2,1 #t2 = t2+1
		j inner_loop_1
	small_exit_1:
		add $t0,$t0,$s1 #t0 = t0+4*n
		j outer_loop_1	

exit:


