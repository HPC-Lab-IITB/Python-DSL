
#----------#----------#----------# Import_Libraries
import math

#----------#----------#----------# Variables
NBT = 4
NBT_1 = NBT -1
sq = 8
FIXED_POINT_FRACTIONAL_BITS = 16
FIXED_POINT_ONE = 1 << FIXED_POINT_FRACTIONAL_BITS
#----------#---------#---------# preprocessing
# Convert floating-point to fixed-point
def float_to_fixed(value):
    return int(value * FIXED_POINT_ONE)

# Convert fixed-point to floating-point
def fixed_to_float(value):
    return float(value) / FIXED_POINT_ONE

#--------------------------- Input 1  2bot 
#x_y_pos_f = [3.4741,   1.8276,0.4857,1.5855,3.9760,4.1173]
#x_y_pos_f = [1.4741, 2.7511, 0.4857,2.5855, 4.1722, 4.1173]
x_y_pos_f = [3.4741, 4.7511, 2.1937, 1.8276, 0.4857,1.5855, 0.1722, 1.9078, 3.9760, 4.1173]
#ypos_f = [1.5855, 0.1722, 1.9078, 3.9760, 4.1173]
ux_f = 0.4857
uy_f = 4.1173
x_y_pos_t = [float_to_fixed(x) for x in x_y_pos_f]

#ypos_t = [float_to_fixed(y) for y in ypos_f]

ux_fix = float_to_fixed(ux_f)
uy_fix = float_to_fixed(uy_f)




# Tb_vector =  inL + inR


from symbolic import *
#from scalar_fda_tmp import *

it = 40 #iteration count 



@hardware
def Module (f_inL, f_outD) : 

	f_inL = InputFifo  ("f_inL", 32)  
    	f_outD = OutputFifo("f_outD", 32)
 
 
 	
 	# input and output register
 
 	reg_ip =  RegArray("reg_ip",32,2*(NBT+1))
 	reg_op =  RegArray("reg_op",32,2*(NBT+1))
	
	#=====================internal reg required =============================


	Xpos  = RegArray ( "Xpos" ,32 , (NBT+1))
	Ypos  = RegArray ( "Ypos" ,32 , (NBT+1))
	Xpos_dup  = RegArray ( "Xpos_dup" ,32 , (NBT+1))
	Ypos_dup  = RegArray ( "Ypos_dup" ,32 , (NBT+1))
	uv  = RegArray ( "uv" ,32 , (NBT))
	uv_dup  = RegArray ( "uv_dup" ,32 , (NBT))
	uvd  = RegArray ( "uvd" ,32 , (NBT*NBT))
	d  = RegArray ( "d" ,32 , (NBT*NBT))
	lm  = RegArray ( "lm" ,32 , (NBT))
	temp1  = RegArray ( "temp1" ,32 , (NBT))
	temp2  = RegArray ( "temp2" ,32 , (NBT))
	
	#=====================variables required ============================= 
	
	x = Var ("x",32)
	f = Var ("f",32)
	f1 = Var ("f1",32)
	f2 = Var ("f2",32)
	w = Var ("w",32)
	y = Var ("y",32)
	tmp1 = Var ("tmp1",32)
	tmp2 = Var ("tmp2",32)
	tmp1_1 = Var ("tmp1_1",64)
	tmp2_1 = Var ("tmp2_1",64)
	tmp1_2 = Var ("tmp1_2",64)
	tmp2_2 = Var ("tmp2_2",64)
	uy = Var ("uy",32)
	ux = Var ("ux",32)
	#FIXED_POINT_ONE_reg = Reg ("FIXED_POINT_ONE_reg")
	dx_square = Var ("dx_square",32)
	dy_square = Var ("dy_square",32)

	xi = Var ("xi",32)
	xj = Var ("xj",32)
	yi = Var ("yi",32)
	yj = Var ("yj",32)
	dx = Var ("dx",32)
	dy = Var ("dy",32)
	tmp3_1 = Var ("tmp3_1",64)
	tmp3_2 = Var ("tmp3_2",64)
	tmp3_3 = Var ("tmp3_3",64)
	tmp3_4 = Var ("tmp3_4",64)
	tmp3_5 = Var ("tmp3_5",64)
	tmp8_1 = Var ("tmp8_1",32)
	max_val = Var ("max_val",32)
	sqrt_inp = Var ("sqrt_inp",32)
	root = Var ("root",32)
	root_prev = Var ("root_prev",32)
	custom_sqrt = Var ("custom_sqrt",32)
	#NBT_1_1 = Reg("NBT_1_1")


	sm = Var ("sm",32)
	uvval2 = Var ("uvval2",32)



	nxi = Var ("nxi",32)
	#index1 = Var ("index1")
	#index2 = Var ("index2")
	#result = Var ("result")
	nxj = Var ("nxj",32)
	nyi = Var ("nyi",32)
	nyj = Var ("nyj",32)
	nxjx = Var ("nxjx",32)
	nx = Var ("nx",32)
	ny = Var ("ny",32)
	tmp10_6 = Var ("tmp10_6",32)
	tmp10_8 = Var ("tmp10_8",32)
	tmp10_1 = Var ("tmp10_1",64)
	tmp10_2 = Var ("tmp10_2",64)
	tmp10_3 = Var ("tmp10_3",64)
	tmp10_4 = Var ("tmp10_4",64)
	tmp10_5 = Var ("tmp10_5",64)
	tmp10_7 = Var ("tmp10_7",64)
	tmp10_9 = Var ("tmp10_9",64)
	f1f2 = Var ("f1f2",32)
	f2f2 = Var ("f2f2",32)
	nx_square = Var ("nx_square",32)
	ny_square = Var ("ny_square",32)
	sqrt_inp_n = Var ("sqrt_inp_n",32)
	root_n = Var ("root_n",32)
	root_prev_n = Var ("root_prev_n",32)
	custom_sqrt_n = Var ("custom_sqrt_n",32)
	#fma = scalar_fma ("fma")
	#scalar_fda_tmp_i0 = scalar_fda_tmp("scalar_fda_tmp_i0")
	
	

	# Add user logic here
	with SerialSections ("initial_P1"):
		
		with ForLoopSection ("fifo_to_reg", "p", 0, 2*(NBT+1)):
      			with LeafSection ("recv_pixel_in_fifo"):
          			reg_ip[p] = f_inL.read ()
          			
          	with ForLoopSection ("xpos_ypos_for", "p1", 0, (NBT+1)):
      			with LeafSection ("xpos_ypos_leaf"):
          			Xpos[p1] = reg_ip[p1]
          			Ypos[p1] = reg_ip[((NBT+1)+p1)]
          			
		with ForLoopSection ("xpos_ypos_for1", "p5", 0, (NBT+1)):
      			with LeafSection ("xpos_ypos_leaf11"):
      				display ("Xpos[%d] = %d,ypos[%d]= %d ",p5,p5, Xpos[p5],Ypos[p5])
      				
		
		with ForLoopSection ("M_itr", "a", 0, NBT):
    			with LeafSection ("leaf_le1"):
				lm[a] = NBT
				
		

#=============================================================================
	'''
	with SerialSections ("initial_S1"):
		with ForLoopSection ("xpos_ypos_for", "p1", 0, (NBT+1)):
      			with LeafSection ("xpos_ypos_leaf"):
          			Xpos[p1] = reg_ip[p1]
          			Ypos[p1] = reg_ip[((NBT+1)+p1)]
         ''' 								
	with SerialSections ("initial_S3"):
		for ii in range(it):
		#with ForLoopSection ("iter1", "ii", 0, 1,1):
			for i3 in range(NBT):
			#with ForLoopSection ("iter2", "i3", 0, NBT):
			
#-----------------------------------------------uv updation --------------------------------------------				
				with LeafSection ("leaf_C1"+ str (i3)+ str (ii)):
					ux = ux_fix
		    			uy = uy_fix
		    			x = Xpos[i3]
		    			y = Ypos[i3]
		    			if (x > ux) :
		    				tmp1 = (x - ux)
		    			else :
		    				tmp1 = (ux - x)
		    			if (y > uy) :
		    				tmp2 = (y - uy)
		    			#display ("y > uy")	 
		    			else :
		    				tmp2 = (uy - y)
		    			tmp1_1 = (tmp1 * tmp1)
			    		tmp2_1 = (tmp2 * tmp2)
			    		#dx_square = ((tmp1 * tmp1) >> FIXED_POINT_FRACTIONAL_BITS)
			    		dx_square = (tmp1_1 >> FIXED_POINT_FRACTIONAL_BITS)
			    		dy_square = (tmp2_1 >> FIXED_POINT_FRACTIONAL_BITS)
			    		w = dx_square + dy_square
			    		tmp1_2 = (w * w)
			    		f1 = (((tmp1_2 >> FIXED_POINT_FRACTIONAL_BITS) >> 1) + FIXED_POINT_ONE)
			    		tmp2_2 = ((tmp1_2 >> FIXED_POINT_FRACTIONAL_BITS) * w)
			    		f2 = (((tmp2_2 >> FIXED_POINT_FRACTIONAL_BITS) >> 2) + w)
			    		#display("f2= %d ",(f2))
			    		if (f1 > f2) :
			    			f1f2 = ( f1 -f2)
			    			#fma.enqOperands (1, f1f2, uv[i3])
			    			#C.writeData (i_ * N + j_, fma.getResult ())
			    			#fma.enqOperands (A.readResp (), B.readResp (), C.readResp ())
			    			uv[i3] = f1f2 + uv[i3]
		    				#uv[i3] = fma.getResult ()
		    				#display ("Iteration %d is for f1>f2,  f = %d ",ii, (f1 -f2))
		    			else :
		    				uv[i3] = 0
		    			display ("Iteration %d is for f2>f1,  f = %d ",ii, (f2 -f1))
		    		#display ("uv[%d] = %d ", i3 ,uv[i3])
			    		
#-----------------------------------------------uv distribution ------------------------------------------
				for j3 in range(NBT):
				#with ForLoopSection ("uv_dist_for1", "j3", 0, NBT):
					with LeafSection ("uv_dist_l1"+str (j3)+ str (i3)+ str (ii)):
						xi = Xpos[i3]
		    				yi = Ypos[i3]
		    				xj = Xpos[j3]
		    				yj = Ypos[j3]
	    					if (xj > xi) :
			    				dx = (xj - xi)	 
			    			else :
			    				dx = (xi - xj)
			    			if (yj > yi) :
			    				dy = (yj - yi)	 
			    			else :
			    				dy = (yi - yj)
			    			tmp3_1 =(dx * dx)
			    			tmp3_2 =(dy * dy)
		    			
		    				dx_square = (tmp3_1>> FIXED_POINT_FRACTIONAL_BITS)
		    				dy_square = (tmp3_2 >> FIXED_POINT_FRACTIONAL_BITS)
		    				sqrt_inp = dx_square + dy_square
		    				if (sqrt_inp == 0) :
			    				custom_sqrt = 0
			    			else :
			    				root = sqrt_inp
			    				tmp3_3 = sqrt_inp
			    				for k3 in range(sq):
				    				if (root != root_prev):
				    					root_prev = root
				    					root = ((root + ((tmp3_3 << FIXED_POINT_FRACTIONAL_BITS) // root)) >> 1)
				    			custom_sqrt = root
			    			#display ("iteration = %d,i3 = %d,j3 =%d, custom_sqrt = %d ",iteration,i3,j3, custom_sqrt)
			    			#display ("sqrt_inp = %d ", sqrt_inp)
			    			display ("custom_sqrt = %d ", custom_sqrt)
			    			d[((i3 * NBT) + j3)] = custom_sqrt
			    	for j4 in range(NBT):
			    		with LeafSection ("uv_dist_l2"+str (j4)+ str (i3)+ str (ii)):
			    	#with ForLoopSection ("uv_dist_for2", "j4", 0, NBT):
					#with LeafSection ("uv_dist_l2"):
						if (i3 != j4):
    						#display ("enered_the_dragen2 ")
		    					sm = 0
		    					for a4 in range(NBT):
		    						if (i3 != a4):
		    							tmp3_4 = FIXED_POINT_ONE
		    							#scalar_fda_tmp_i0.enqOperands((tmp3_4 << FIXED_POINT_FRACTIONAL_BITS), d[((i3 * NBT) + a4)],0)
		    							#fma.enqOperands((tmp3_4 << FIXED_POINT_FRACTIONAL_BITS), d[((i3 * NBT) + a4)],0)
		    							#sm = (sm + fma.getResult())
		    							sm = (sm + ((tmp3_4 << FIXED_POINT_FRACTIONAL_BITS) // d[((i3 * NBT) + a4)]))
		    					tmp3_5 = FIXED_POINT_ONE
		    					#scalar_fda_tmp_i0.enqOperands((tmp3_5 << FIXED_POINT_FRACTIONAL_BITS), d[((i3 * NBT) + j4)],0)
		    					#fma.enqOperands((tmp3_5 << FIXED_POINT_FRACTIONAL_BITS), d[((i3 * NBT) + j4)],0)
		    					#fma.enqOperands (fma.getResult(), uv[i3] , 0)
		    					#uvval2 = fma.getResult()
		    					uvval2 = (uv[i3] * ((tmp3_5 << FIXED_POINT_FRACTIONAL_BITS) // d[((i3 * NBT) + j4)]))
		    					display ("sm = %d ", sm)
		    					#display ("iteration = %d,i3 = %d,j4 =%d,sm = %d ",iteration ,i3 ,j4, sm)
		    					if sm != 0 :
		    						uvd[((i3 * NBT) + j4)] = (uvval2 // sm)
		    						#display ("iteration = %d,i3 = %d,j4 =%d,uvval2 = %d,sm = %d,uvval = %d ",iteration ,i3 ,j4,uvval2,sm, uvval2/sm)
		    					else :
		    						uvd[((i3 * NBT) + j4)] = 0
		    						#display ("iteration = %d,i3 = %d,j4 =%d,uvval2 = %d,sm = %d,uvval = %d ",iteration ,i3 ,j4,uvval2,sm, uvval2/sm)
		    					#display ("iteration = %d, uvd[%d] = %d ",iteration ,((i3 * NBT) + j4), uvd[((i3 * NBT) + j4)])			    		
		    					
		
#------------------------------------------------------ local mate selection -----------------------------------------------------------
				for k7 in range(NBT):
			    		with LeafSection ("local_mate_for1"+str (k7)+ str (i3)+ str (ii)):
				#with ForLoopSection ("local_mate_for1", "k7", 0, NBT):
					#with LeafSection ("local_mate_l1"):
						temp1[k7] = uvd[((k7 * NBT) + i3)]
	    					temp2[k7] = k7
	    					Xpos_dup[k7] = Xpos[k7]
	    					Ypos_dup[k7] = Ypos[k7]
	    					uv_dup[k7] = uv[k7]
	    					
	    			with LeafSection ("local_mate_l2"+ str (i3)+ str (ii)):
	    				for j8 in range(NBT_1):
	    					for k8 in range(NBT_1):
	    						if (temp1[k8] < temp1[k8 + 1]):
	    							temp1[k8] = temp1[k8 + 1]
	    							temp1[k8 + 1] = temp1[k8]
	    							temp2[k8] = temp2[k8 + 1]
	    							temp2[k8 + 1] = temp2[k8]
	    							Xpos_dup[k8] = Xpos_dup[k8 + 1]
	    							Xpos_dup[k8 + 1] = Xpos_dup[k8]
	    							Ypos_dup[k8] = Ypos_dup[k8 + 1]
	    							Ypos_dup[k8 + 1] = Ypos_dup[k8]
	    							uv_dup[k8] = uv_dup[k8 + 1]
	    							uv_dup[k8 + 1] = uv_dup[k8]
	    						#display("iteration = %d,i3 = %d,j8 = %d,k8 =%d,temp2[%d] = %d",iteration,i3, j8, k8,k8,  temp2[k8] )
	    						
	    			#display("iteration = %d ,uv_check[%d]=%d,temp2[0] = %d",iteration,max (0,temp2[0]),uv[max (temp2[0],0)],temp2[0])
	    					
#----------------------------------------------- movement phase-------------------------
				with LeafSection ("movement_l1"+ str (i3)+ str (ii)):
	    				if (temp2[0] == 0):
	    					nxj = Xpos[NBT]
	    					nxi = Xpos[i3]
	    					nyj = Ypos[NBT]
	    					nyi = Ypos[i3]
		    				if (nxj > nxi):
		    					nx = (nxj - nxi)	 
				    		else :
				    			nx = (nxi - nxj)
				    		if (nyj > nyi):
				    			ny = (nyj - nyi)	 
				    		else:
				    			ny = (nyi - nyj)
	    					#nx = Xpos[NBT] - Xpos[i3]
	    					#ny = Ypos[NBT] - Ypos[i3]
	    				else:
	    					if (uv[0] < uv_dup[0]):
		    					nxj = Xpos_dup[0]
		    					nxi = Xpos[i3]
		    					nyj = Ypos_dup[0]
		    					nyi = Ypos[i3]
			    				if (nxj > nxi):
			    					nx = (nxj - nxi)	 
					    		else :
					    			nx = (nxi - nxj)
					    		if (nyj > nyi):
					    			ny = (nyj - nyi)	 
					    		else:
					    			ny = (nyi - nyj)
	    						#nx = Xpos_dup[0] - Xpos[i3]
	    						#ny = Ypos_dup[0] - Ypos[i3]
	    					else:
	    						nxj = Xpos[NBT]
		    					nxi = Xpos[i3]
		    					nyj = Ypos[NBT]
		    					nyi = Ypos[i3]
			    				if (nxj > nxi):
			    					nx = (nxj - nxi)	 
					    		else :
					    			nx = (nxi - nxj)
					    		if (nyj > nyi):
					    			ny = (nyj - nyi)	 
					    		else:
					    			ny = (nyi - nyj)
	    						#nx = Xpos[NBT] - Xpos[i3]
	    						#ny = Ypos[NBT] - Ypos[i3]	
	    						
	    				
			    		tmp10_1 =(nx * nx)
			    		tmp10_2 =(ny * ny)	    			
		    			nx_square = (tmp10_1>> FIXED_POINT_FRACTIONAL_BITS)
		    			ny_square = (tmp10_2 >> FIXED_POINT_FRACTIONAL_BITS)
		    			sqrt_inp_n = nx_square + ny_square
		    			if (sqrt_inp_n == 0) :
			    			custom_sqrt_n = 0
			    		else :
			    			root_n = sqrt_inp_n
			    			tmp10_3 = sqrt_inp_n
			    			for k10 in range(sq):
				    			if (root_n != root_prev_n):
				    				root_prev_n = root_n
				    				root_n = ((root_n + ((tmp10_3 << FIXED_POINT_FRACTIONAL_BITS) // root_n)) >> 1)
				    		custom_sqrt_n = root_n	
				    	#display ("iteration = %d ,sqrt_inp_n = %d ",iteration, sqrt_inp_n)
				    	#display ("iteration = %d ,i3=%d,custom_sqrt_n = %d,nx=%d ",iteration+1, i3,custom_sqrt_n,nx)
				    	tmp10_4 = nx
				    	tmp10_5 = ny
				    	#display("iteration %d -> Bot %d: ", iteration, (i3 + 1))
				    	if custom_sqrt_n != 0:
				    		
				    		if (nxj > nxi):
	    						tmp10_6 = ((tmp10_4 << FIXED_POINT_FRACTIONAL_BITS) // custom_sqrt_n) 
				    			tmp10_7 = (tmp10_6 * 9830 )
				    			Xpos[i3] = (nxi + (tmp10_7 >> FIXED_POINT_FRACTIONAL_BITS))	
				    			#display("xpos=%d ", (nxi + (tmp10_7 >> FIXED_POINT_FRACTIONAL_BITS)) ) 
				    		else :
				    			tmp10_6 = (((tmp10_4 << FIXED_POINT_FRACTIONAL_BITS) // custom_sqrt_n) )
				    			tmp10_7 = (  tmp10_6 * 9830)
				    			Xpos[i3] = (nxi - (tmp10_7 >> FIXED_POINT_FRACTIONAL_BITS)-1)
				    		if (nyj > nyi):
				    			tmp10_8 = ((tmp10_5 << FIXED_POINT_FRACTIONAL_BITS) // custom_sqrt_n)	
				    			tmp10_9 = ( tmp10_8 * 9830)
				    			Ypos[i3] = (nyi + (tmp10_9 >> FIXED_POINT_FRACTIONAL_BITS))
				    			#display("ypos=%d ", (nyi + (tmp10_9 >> FIXED_POINT_FRACTIONAL_BITS)) ) 
				    		else:
				    			tmp10_8 = (((tmp10_5 << FIXED_POINT_FRACTIONAL_BITS) // custom_sqrt_n) )	
				    			tmp10_9 = (tmp10_8 * 9830)
				    			Ypos[i3] = (nyi - (tmp10_9 >> FIXED_POINT_FRACTIONAL_BITS)-1)
	    				else :
	    					#Xpos[i3] = Xpos[i3] 
	    					#Ypos[i3] = Ypos[i3]
	    					Xpos[i3] = nxi 
	    					Ypos[i3] = nyi
	    			#with Leaf:
	    				display("iteration %d -> Bot %d: xpos=%d, ypos=%d", ii, (i3 + 1), Xpos[i3], Ypos[i3])
	
##=========================================sending output to reg ===================
	
	with SerialSections ("initial_S4"):		
		with LeafSection ("output_l1"):
			for p_out in range((NBT+1)):
		            reg_op[p_out] = Xpos[p_out] 
		            reg_op[(p_out+(NBT+1))] = Ypos[p_out]
		            
		with LeafSection ("output_l2"):
			for b in range(2*(NBT+1)):
				f_outD.write (reg_op[b])
				display ("reg_op[%0d] = [%0d]", b, reg_op[b])
'''						
	with SerialSections ("initial_P22"):    			
	    	with LeafSection ("results_out"):
		      for p in range (64):
		      	display ("reg_op[%0d] = [%0d]", p, reg_op[p])
                

'''


@hardware
def my_tb():
  m1 = Module ("m1", [], [])
  with LeafSection ("S10"):
      m1.start ()
  for l_in in range(((NBT+1)*2)):
  #with ForLoopSection ("p1_fl1", "l_in", 0, T_S ):
  	#with ForLoopSection ("p1_fl1", "l_in", 0, T_S ):
	with LeafSection ("p1_fl1_l1_"+ str (l_in)):
	  #m1.m_["f_inL"].write (l_in*2)
	  #m1.m_["f_inR"].write (l_in*3)
	  m1.m_["f_inL"].write (x_y_pos_t[l_in])
	#  m1.m_["f_inR"].write (inR[l_in])
	  display ("my_tb : sending bot position %0d.", x_y_pos_t[l_in])
  with ForLoopSection ("TSINC", "m", 0, 2*(NBT+1)):
        with LeafSection ("SP11_1"):
          display ("#Result (%0d) = [%0d]", m, m1.m_["f_outD"].read ())

t = Module ("", None, None)
#t = min_sum_decoder ("")
t.emitVerilog (sys.stdout)
t = my_tb ("")
t.emitVerilog (sys.stdout)


