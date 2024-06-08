1) Input images(left and right) are read from file and are given to SGM module 

2) Generate out.v file for source code (with command -  make rtl)

3) Store computed disparity values into file by adding below out.v
	a) Instantiate new output file 
	b) Write the output variable(f_outD_read_data) into file   
	
4) Run RTL simulation (with command - make rtl_sim_verilator) 
