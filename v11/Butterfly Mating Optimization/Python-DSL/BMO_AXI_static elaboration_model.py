
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

#--------------------------- Input 1_1 20 iterations input
#x_y_pos_f = [2.0090 ,  1.1996 ,0.9195 ,2.0863 ,   1.7548, 0.3798 ,   0.6166  ,  1.1998 ,   0.2483 ,   2.5662]
#ux_f = 1.7548
#uy_f = 2.5662



x_y_pos_t = [float_to_fixed(x) for x in x_y_pos_f]

#ypos_t = [float_to_fixed(y) for y in ypos_f]

ux_fix = float_to_fixed(ux_f)
uy_fix = float_to_fixed(uy_f)


#----------#----------#----------# Hardware              
from symbolic import *
from HPCpy import *

it = 40 #iteration count 
Reg_ip_count  = 10 # n numbers of input ports ---->   bots xpos + source xpos + bots xpos + source ypos
Reg_op_count  = 10 # m numbers of output ports---->   bots xpos + source xpos + bots xpos + source ypos 


BaseAddress = "0x43C00000" # Base address of the axi-lite IP
                     
Tb_vector = x_y_pos_t

Reg_ip_AxiLite_count   = 1 # Ignored by the tool
Reg_ip_AxiStream_count = 1 # Ignored by the tool
Reg_op_AxiLite_count   = 1 # Ignored by the tool
Reg_op_AxiStream_count = 1 # Ignored by the tool

def Module(Predefined):
#def Module(AxiLite):

    # User to add RegIn() and RegOut() here
    
    # User to add RegIn() and RegOut() ends
    
    reg_ip = In_Ports()
    reg_op = Out_Ports()
    
    #--------------------------- User to add Reg() and Var() here---------------------------
    
    Xpos  = [Reg  ("Xpos"  + str (r1)) for r1 in range (NBT+1)]
    Ypos  = [Reg  ("Ypos"  + str (r2)) for r2 in range (NBT+1)]
    Xpos_dup  = [Reg  ("Xpos_dup"  + str (r11)) for r11 in range (NBT+1)]
    Ypos_dup  = [Reg  ("Ypos_dup"  + str (r21)) for r21 in range (NBT+1)]
    uv = [Reg  ("uv"  + str (r3)) for r3 in range (NBT)]
    uv_dup = [Reg  ("uv_dup"  + str (r31)) for r31 in range (NBT)]
    uvd = [Reg  ("uvd"  + str (r4)) for r4 in range (NBT*NBT)]
    d = [Reg  ("d"  + str (r6)) for r6 in range (NBT*NBT)]
    lm = [Reg  ("lm"  + str (r5)) for r5 in range (NBT)]
    temp1 = [Reg  ("temp1"  + str (r7)) for r7 in range(NBT)]
    temp2 = [Reg  ("temp2"  + str (r8)) for r8 in range(NBT)]
    x = Var ("x")
    f = Var ("f")
    f1 = Var ("f1")
    f2 = Var ("f2")
    w = Var ("w")
    y = Var ("y")
    tmp1 = Var ("tmp1")
    tmp2 = Var ("tmp2")
    tmp1_1 = Var ("tmp1_1",64)
    tmp2_1 = Var ("tmp2_1",64)
    tmp1_2 = Var ("tmp1_2",64)
    tmp2_2 = Var ("tmp2_2",64)
    uy = Var ("uy")
    ux = Var ("ux")
    #FIXED_POINT_ONE_reg = Reg ("FIXED_POINT_ONE_reg")
    dx_square = Var ("dx_square")
    dy_square = Var ("dy_square")
    
    xi = Var ("xi")
    xj = Var ("xj")
    yi = Var ("yi")
    yj = Var ("yj")
    dx = Var ("dx")
    dy = Var ("dy")
    tmp3_1 = Var ("tmp3_1",64)
    tmp3_2 = Var ("tmp3_2",64)
    tmp3_3 = Var ("tmp3_3",64)
    tmp3_4 = Var ("tmp3_4",64)
    tmp3_5 = Var ("tmp3_5",64)
    tmp8_1 = Var ("tmp8_1")
    max_val = Var ("max_val")
    sqrt_inp = Var ("sqrt_inp")
    root = Var ("root")
    root_prev = Var ("root_prev")
    custom_sqrt = Var ("custom_sqrt")
    #NBT_1_1 = Reg("NBT_1_1")
    
    
    sm = Var ("sm")
    uvval2 = Var ("uvval2")
    
    
    
    nxi = Var ("nxi")
    #index1 = Var ("index1")
    #index2 = Var ("index2")
    #result = Var ("result")
    nxj = Var ("nxj")
    nyi = Var ("nyi")
    nyj = Var ("nyj")
    nxjx = Var ("nxjx")
    nx = Var ("nx")
    ny = Var ("ny")
    tmp10_6 = Var ("tmp10_6")
    tmp10_8 = Var ("tmp10_8")
    tmp10_1 = Var ("tmp10_1",64)
    tmp10_2 = Var ("tmp10_2",64)
    tmp10_3 = Var ("tmp10_3",64)
    tmp10_4 = Var ("tmp10_4",64)
    tmp10_5 = Var ("tmp10_5",64)
    tmp10_7 = Var ("tmp10_7",64)
    tmp10_9 = Var ("tmp10_9",64)
    nx_square = Var ("nx_square")
    ny_square = Var ("ny_square")
    sqrt_inp_n = Var ("sqrt_inp_n")
    root_n = Var ("root_n")
    root_prev_n = Var ("root_prev_n")
    custom_sqrt_n = Var ("custom_sqrt_n")
    
    #------------------------------------------------------------------------------------------
    # User to add Reg() and Var() ends
    #input taking
    with Parallel:
    	with Leaf:
    		for p1 in range((NBT+1)):
    			Ypos[p1] = reg_ip[((NBT+1)+p1)]
    			#display ("input values of  Ypos(%d)=  %d:",p1 ,Ypos[p1])
    	with Leaf:
    		for p2 in range((NBT+1)):		
    			Xpos[p2] = reg_ip[p2]
    	with Leaf:
    		for p2 in range(NBT):
    			lm[p2] = NBT	
    
    # ------------------Add user logic here---------------   			
    with Series:
    	for iteration in range(it):
    		#display("Iteration %d is", iteration)
    		for i3 in range(NBT):
    		#-----------------------------------------------uv updation ------------------------------------------
    			with Leaf:
		    		ux = ux_fix
		    		uy = uy_fix
		    		#for iter2 in range(NBT):
		    		x = Xpos[i3]
		    		y = Ypos[i3]
		    		#display ("iteration= %d,x = %d ,y = %d ",iteration, x ,y)
		    		if (x > ux) :
		    			tmp1 = (x - ux)
		    			#display ("x > ux")	 
		    		else :
		    			tmp1 = (ux - x)
		    			#display ("x < ux")
		    		if (y > uy) :
		    			tmp2 = (y - uy)
		    			#display ("y > uy")	 
		    		else :
		    			tmp2 = (uy - y)
		    			#display ("y < uy")
		    		#display ("iteration= %d,tmp1 = %d ,tmp2 = %d ",iteration, tmp1 ,tmp2)
		    		tmp1_1 = (tmp1 * tmp1)
		    		tmp2_1 = (tmp2 * tmp2)
		    		#dx_square = ((tmp1 * tmp1) >> FIXED_POINT_FRACTIONAL_BITS)
		    		dx_square = (tmp1_1 >> FIXED_POINT_FRACTIONAL_BITS)
		    		dy_square = (tmp2_1 >> FIXED_POINT_FRACTIONAL_BITS)
		    		w = dx_square + dy_square
		    		#display ("dx_square= %d ", dx_square)
		    		#display ("dy_square= %d ", dy_square)
		    		#display ("iteration = %d,i3 = %d, w = %d ",iteration,i3, w)
		    		tmp1_2 = (w * w)
		    		f1 = (((tmp1_2 >> FIXED_POINT_FRACTIONAL_BITS) >> 1) + FIXED_POINT_ONE)
		    		tmp2_2 = ((tmp1_2 >> FIXED_POINT_FRACTIONAL_BITS) * w)
		    		f2 = (((tmp2_2 >> FIXED_POINT_FRACTIONAL_BITS) >> 2) + w)
		    		#display("f2= %d ",(f2))
		    		if (f1 > f2) :
		    			uv[i3] = (uv[i3] + (f1 -f2)) 
		    			#display ("Iteration %d is for f1>f2,  f = %d ",iteration, (f1 -f2))
		    		else :
		    			uv[i3] = 0
		    		display ("Iteration %d is for f2>f1,  f = %d ",iteration, (f2 -f1))
		    		#display ("uv[%d] = %d ", i3 ,uv[i3])
    			
    			#-----------------------------------------------uv distribution ------------------------------------------
    			for j3 in range(NBT):
    				with Leaf:
    					#display ("iteration = %d,i3 = %d,j3 =%d",iteration,i3,j3)
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
			    					root = ((root + ((tmp3_3 << FIXED_POINT_FRACTIONAL_BITS) / root)) >> 1)
			    			custom_sqrt = root
		    			#display ("iteration = %d,i3 = %d,j3 =%d, custom_sqrt = %d ",iteration,i3,j3, custom_sqrt)
		    			#display ("sqrt_inp = %d ", sqrt_inp)
		    			display ("custom_sqrt = %d ", custom_sqrt)
		    			d[((i3 * NBT) + j3)] = custom_sqrt
	    		with Leaf:		
	    			for j4 in range(NBT):
	    				#display ("enered_the_dragen1 %d %d",i3,j3)
	    				if (i3 != j4):
    						#display ("enered_the_dragen2 ")
	    					sm = 0
	    					for a4 in range(NBT):
	    						if (i3 != a4):
	    							tmp3_4 = FIXED_POINT_ONE
	    							sm = (sm + ((tmp3_4 << FIXED_POINT_FRACTIONAL_BITS) / d[((i3 * NBT) + a4)]))
	    					tmp3_5 = FIXED_POINT_ONE
	    					uvval2 = (uv[i3] * ((tmp3_5 << FIXED_POINT_FRACTIONAL_BITS) / d[((i3 * NBT) + j4)]))
	    					display ("sm = %d ", sm)
	    					#display ("iteration = %d,i3 = %d,j4 =%d,sm = %d ",iteration ,i3 ,j4, sm)
	    					if sm != 0 :
	    						uvd[((i3 * NBT) + j4)] = (uvval2 / sm)
	    						#display ("iteration = %d,i3 = %d,j4 =%d,uvval2 = %d,sm = %d,uvval = %d ",iteration ,i3 ,j4,uvval2,sm, uvval2/sm)
	    					else :
	    						uvd[((i3 * NBT) + j4)] = 0
	    						#display ("iteration = %d,i3 = %d,j4 =%d,uvval2 = %d,sm = %d,uvval = %d ",iteration ,i3 ,j4,uvval2,sm, uvval2/sm)
	    					#display ("iteration = %d, uvd[%d] = %d ",iteration ,((i3 * NBT) + j4), uvd[((i3 * NBT) + j4)])
	    		
	    		
	    		
	    		#------------------------------------------------------ local mate selection -----------------------------------------------------------
	    		with Leaf:
	    			for k7 in range(NBT):
    					temp1[k7] = uvd[((k7 * NBT) + i3)]
    					temp2[k7] = k7
    					Xpos_dup[k7] = Xpos[k7]
    					Ypos_dup[k7] = Ypos[k7]
    					uv_dup[k7] = uv[k7]
    					#display("temp1[%d] = %d",k7,  temp1[k7] )
    			with Leaf:
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
    			with Leaf:
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
    					if (uv[i3] < uv_dup[0]):
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
    						
    				
		    		#display ("iteration = %d,i3=%d ,nx = %d,ny = %d ",iteration,i3, nx,ny)
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
			    				root_n = ((root_n + ((tmp10_3 << FIXED_POINT_FRACTIONAL_BITS) / root_n)) >> 1)
			    		custom_sqrt_n = root_n	
			    	#display ("iteration = %d ,sqrt_inp_n = %d ",iteration, sqrt_inp_n)
			    	#display ("iteration = %d ,i3=%d,custom_sqrt_n = %d,nx=%d ",iteration+1, i3,custom_sqrt_n,nx)
			    	tmp10_4 = nx
			    	tmp10_5 = ny
			    	#display("iteration %d -> Bot %d: ", iteration, (i3 + 1))
			    	if custom_sqrt_n != 0:
			    		
			    		if (nxj > nxi):
    						tmp10_6 = ((tmp10_4 << FIXED_POINT_FRACTIONAL_BITS) / custom_sqrt_n) 
			    			tmp10_7 = (9830 * tmp10_6)
			    			Xpos[i3] = (nxi + (tmp10_7 >> FIXED_POINT_FRACTIONAL_BITS))	
			    			#display("xpos=%d ", (nxi + (tmp10_7 >> FIXED_POINT_FRACTIONAL_BITS)) ) 
			    		else :
			    			tmp10_6 = (((tmp10_4 << FIXED_POINT_FRACTIONAL_BITS) / custom_sqrt_n) )
			    			tmp10_7 = (9830 * tmp10_6)
			    			Xpos[i3] = (nxi - (tmp10_7 >> FIXED_POINT_FRACTIONAL_BITS)-1)
			    		if (nyj > nyi):
			    			tmp10_8 = ((tmp10_5 << FIXED_POINT_FRACTIONAL_BITS) / custom_sqrt_n)	
			    			tmp10_9 = (9830 * tmp10_8)
			    			Ypos[i3] = (nyi + (tmp10_9 >> FIXED_POINT_FRACTIONAL_BITS))
			    			#display("ypos=%d ", (nyi + (tmp10_9 >> FIXED_POINT_FRACTIONAL_BITS)) ) 
			    		else:
			    			tmp10_8 = (((tmp10_5 << FIXED_POINT_FRACTIONAL_BITS) / custom_sqrt_n) )	
			    			tmp10_9 = (9830 * tmp10_8)
			    			Ypos[i3] = (nyi - (tmp10_9 >> FIXED_POINT_FRACTIONAL_BITS)-1)
			    			#display(" ypos=%d ", (nyi - (tmp10_9 >> FIXED_POINT_FRACTIONAL_BITS)) -1 ) 
    				else :
    					#Xpos[i3] = Xpos[i3] 
    					#Ypos[i3] = Ypos[i3]
    					Xpos[i3] = nxi 
    					Ypos[i3] = nyi
    					#display("xpos=%d ",nxi)
    			#with Leaf:
    				display("iteration %d -> Bot %d: xpos=%d, ypos=%d", iteration, (i3 + 1), Xpos[i3], Ypos[i3])	
    			
    			
    				
    							
		
# ---------------------------------
    #output send 
    with Series:
    	with Leaf:
    		for p_out in range((NBT+1)):
                    reg_op[p_out] = Xpos[p_out] 
                    reg_op[(p_out+(NBT+1))] = Ypos[p_out]
                
    # User logic ends

#----------#----------#----------# Hardware 


def my_tb():

    args = dict(( "reg_ip_" + str(i), x_y_pos_t[i]) for i in range(len(x_y_pos_t)))

    with Series:
      with Leaf:
          Module_dut.start(**args)
      #with Leaf:
      #    display("--------- > final Bot locations <-------- ")
      with Leaf:
          for p in range(((NBT+1)*2)):
                if (p<NBT):
                	display ("Bot " + str(p+1) + " xpos = %0d", Module_dut.isDone()[p])
                if (p==NBT):
                	display ("Source " + " xpos = %0d", Module_dut.isDone()[p])
                if (NBT<p<((2*NBT)+1)):
                	display ("Bot " + str(p-NBT) + " ypos = %0d", Module_dut.isDone()[p])
                if (p==((2*NBT) +1)):
                	display ("Source " + " ypos = %0d", Module_dut.isDone()[p])
