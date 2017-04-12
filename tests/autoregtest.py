import random
def build_write(write_addr,read_addr1,read_addr2):
	def combine(w,r1,r2):
		return r1 | r2<<5 | w<<10 | 1<<15 #combine the values into 16 bit integer
	return [combine(write_addr[i],read_addr1[i],read_addr2[i]) for i in xrange(0,len(write_addr))]
#format integers for putting in out files
def bin_encode(value, length = None ):
	if(length == None):
		length = len(value);
	bin_str = value.__format__('b')
	bin_str = bin_str.zfill(length)
	bin_str_space = [bin_str[i:i+4] for i in range(0, length, 4)]
	return " ".join(bin_str_space)

#encode as a numeric hexidecimal string
def hex_encode(num):
	return num.__hex__()[2:]

#compile a circuit template
#you can put variables in a template
#and this function will substitute values for them
#template is the name of the template file
#test_circ is the name of the generated logisim
#t_vars is a series of keyword arguments where the key is the name of the variable in the template file
#and the value is the hex value to replace it with
def write_circ(template, test_circ, **t_vars):
	template_file = open(template, 'r')
	gen_file = open(test_circ,'w')
	for line in template_file:
		for t_var,t_val in t_vars.iteritems():
			line = line.replace(t_var,t_val)
		gen_file.write(line)

if (__name__=="__main__"):
	#generate the expected output file
	#initialize memory as list of 31 random integers
	memory = [random.randint(0,2**32-1) for i in xrange(1,32)]
	hex_vals = [hex_encode(i) for i in memory]
	write_vals = " ".join(hex_vals)
	#build the instructions to test it
	write_addr = [i for i in xrange(1,32)]+[0,0]
	read_addr = [0]+[i for i in xrange(0,32)]
	write_instr_vals = build_write(write_addr,read_addr,read_addr)
	write_instr_hex = [hex_encode(i) for i in write_instr_vals] #encode values as hex numbers
	write_instr = " ".join(write_instr_hex)
	#generate the register file harness from the template
	write_circ("regtest-template.circ","regtest-harness.circ", __write_vals=write_vals, __write_instr=write_instr)
	#.out file syntax is "Test #", "$s0 Value", "$s1 Value", "$s2 Value", "$ra Value", "$sp Value", "Read Data 1", "Read Data 2"
	#these values are tab separated
	#use the binencode function to format values properly
	memory = [0]+memory
	s0_value = memory[16]
	s1_value = memory[17]
	s2_value = memory[18]
	ra_value = memory[31]
	sp_value = memory[29]
	read_data = [0]+memory
	expected_out = open("reference_output/regtest.out", 'w')
	for testnum in xrange(0,32):
		if(testnum<16):
			s0 = bin_encode(0, 32)
		else:
			s0 = bin_encode(s0_value, 32)
		if(testnum<17):
			s1 = bin_encode(0, 32)
		else:
			s1 = bin_encode(s1_value, 32)
		if(testnum<18):
			s2 = bin_encode(0, 32)
		else:
			s2 = bin_encode(s2_value, 32)
		if(testnum<31):
			ra = bin_encode(0, 32)
		else:
			ra = bin_encode(ra_value, 32)
		if(testnum<29):
			sp = bin_encode(0, 32)
		else:
			sp = bin_encode(sp_value, 32)
		read1 = bin_encode(read_data[testnum], 32)
		read2 = read1
		testnm = bin_encode(testnum, 8)
		line = "\t".join([testnm, s0, s1, s2, ra, sp, read1, read2])
		line = line + "\n"
		expected_out.write(line)
	
	

