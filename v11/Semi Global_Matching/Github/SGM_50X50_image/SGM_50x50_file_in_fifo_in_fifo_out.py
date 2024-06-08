
import math
imgW = 50 	#Image_Size
imgH = 50

    
inL = []
inR = []


##=======================left image file in +===================================================
def read_data_from_file(file_path):
    image_values = []
 
    with open(file_path, "r") as file:
    	for line1 in file.readlines():
    		#row = []
		for line in line1.split():
		    try:
			image_values.append(int(''.join(char for char in line if char.isdigit() or char == '-')))
		    except ValueError:
			print("Skipping line: {} (not a valid integer)".format(line.strip()))
    return image_values

inL = read_data_from_file("./left_compressed_teddy.txt")
inR = read_data_from_file("./right_compressed_teddy.txt")


from symbolic import *

#d=0
imgW = 50 	#Image_Size
imgH = 50 
T_S = imgH*imgW
FILTER_SIZE = 3   #kernel_Size
total_input_count = 2*(imgW*imgH)
total_output_count = (imgW*imgH)
FILTER_SIZE_1 = FILTER_SIZE - 1
N = FILTER_SIZE*FILTER_SIZE
N_1 = N - 1
mid = N_1 >> 1
FILTER_OFFSET = FILTER_SIZE_1 / 2
SEARCH_RANGE = 8
ADDR_WIDTH =  3
MAX_SUM = 127
MAX_COST = 127
P1 =2
P2 = 20


@hardware
def Module (f_inL, f_inR ,f_outD) : 

	f_inL = InputFifo  ("f_inL", 16)  #
    	f_inR = InputFifo  ("f_inR", 16)
    	f_outD = OutputFifo("f_outD", 16)

	inp_imgL  = RegArray ("inp_imgL", 16, T_S)
	inp_imgR  = RegArray ("inp_imgR", 16, T_S)

	#======================================================== left_image elements ================================================================

	#=======line_bufferL elements

	Line_bufferL  = RegArray  ("Line_bufferL",16, FILTER_SIZE * imgW)	#(name , width , depth)

	#======= left_window elements

	windowL = RegArray ("windowL" ,16, N)   
	right_colL = RegArray ("right_colL" ,16, FILTER_SIZE) 
	#======================================================== right_image elements ================================================================

	#=======line_bufferR elements

	Line_bufferR  = RegArray  ("Line_bufferR",16, FILTER_SIZE * imgW)	#(name , width , depth)

	#======= right_window elements

	windowR = RegArray ("windowR" ,16, N)
	windowR_shift = RegArray ("windowR_shift" ,16, N)  
	right_colR = RegArray ("right_colR" ,16, FILTER_SIZE) 

	#=====================variables required =============================

	v_sim = Var("v_sim", 16)
	abs_sum = Var("abs_sum" , 16)
	winning_disp = Reg("winning_disp" ,16)
	abs_val = Var("abs_val" , 16)
	jj_var = Var("jj_var" , 16)
	index = Var("index" , 16)

	#===============sgm variables =========================================

	min1 = Var("min1",16)
	min2 = Var("min2",16)
	index1 = Var("index1",16)
	cost_row = RegArray ("cost_row" ,16, (imgW*SEARCH_RANGE))
	min_cost_row = RegArray ("min_cost_row",16,imgW)
	cost_left = RegArray ("cost_left",16,SEARCH_RANGE)
	min_cost_left = Reg("min_cost_left" , 16)
	ham_dist = RegArray ("ham_dist",16,SEARCH_RANGE)
	sum_cost = Var("sum_cost" , 16)
	path_cost= Var("path_cost" , 16)
	min_sum_cost = Reg("min_sum_cost" , 16)
	x_ham = Var("x_ham",16)
	y_ham = Var("y_ham",16)
	cap = RegArray ("cap",16,16)
	cost = RegArray ("cost",16,4)
	path_var = Var("path_var",16)
	#====================SGM variable=======================================

	top_left_d_prev = Reg("top_left_d_prev" , 16)
	top_left_d = Reg("top_left_d" , 16)
	top_left_d_forw = Reg("top_left_d_forw" , 16)
	top_d_prev = Reg("top_d_prev" , 16)
	top_d = Reg("top_d" , 16)
	top_d_forw = Reg("top_d_forw" , 16)
	top_right_d_prev = Reg("top_right_d_prev" , 16) 
	top_right_d = Reg("top_right_d" , 16)
	top_right_d_forw = Reg("top_right_d_forw" , 16)
	left_d_prev = Reg("left_d_prev" , 16) 
	left_d = Reg("left_d" , 16) 
	left_d_forw = Reg("left_d_forw" , 16)

	# User to add Reg() and Var() ends

	# Add user logic here
	with ParallelSections ("initial_P1"):
		
		with ForLoopSection ("R_pixel_in_fifo", "p", 0, imgH * imgW):
      			with LeafSection ("recv_pixel_in_fifo"):
          			inp_imgL[p] = f_inL.read ()
          			inp_imgR[p] = f_inR.read ()
		
		with ForLoopSection ("M_itr", "a", 0, (FILTER_SIZE * imgW), 1):
    			with LeafSection ("leaf_le1"):
				Assignment(Line_bufferL[a] , 0)
				Assignment(Line_bufferR[a] , 0)
		
		with ForLoopSection ("WIN_new", "win", 0, N):
			with LeafSection ("leaf_le2"):
				Assignment(windowL[win] , 0)
				Assignment(windowR[win] , 0)
				Assignment(min_cost_left , MAX_SUM)
		with ForLoopSection ("leaf_le3", "c_r", 0, (imgW*SEARCH_RANGE), 1):
    			with LeafSection ("leaf_le12"):
				Assignment(cost_row[c_r] , MAX_SUM)
		with ForLoopSection ("leaf_le12l", "cl", 0, SEARCH_RANGE, 1):
    			with LeafSection ("leaf_le13"):
				Assignment(cost_left[cl] , MAX_SUM)
		with ForLoopSection ("cr_loop", "cr", 0, imgW, 1):
			with LeafSection ("leaf_le5"):
			#for cr in range(imgW):
				Assignment(min_cost_row[cr] , MAX_SUM)

	with SerialSections ("initial_P1"):
		with ForLoopSection ("row_iter", "row", 0, imgH):
			with ForLoopSection ("col_iter", "col", 0, imgW-2):
	    			with LeafSection ("leaf_le_pp1"):
	    				min_sum_cost = MAX_SUM
					winning_disp = 1
	    			
	    			
	    			with LeafSection ("leaf_le_pp2"):
	    				for ii in range(FILTER_SIZE-1):
	    					Assignment(Line_bufferL[((ii*imgW)+(col+1))] , Line_bufferL[((col+1)+(imgW*(ii+1)))])
	    					Assignment(Line_bufferR[((ii*imgW)+(col+1))] , Line_bufferR[((col+1)+(imgW*(ii+1)))])
	    					Assignment(right_colL[ii] , Line_bufferL[((col+1)+(imgW*(ii+1)))])
	    					Assignment(right_colR[ii] , Line_bufferR[((col+1)+(imgW*(ii+1)))])
	##======================================================Reading input =================================================================	    				
	    			with LeafSection ("leaf_le_pp222_"+ str (row)+"_"+str (col)):
	    				Assignment(Line_bufferL[((col+1)+(imgW*(FILTER_SIZE - 1)))],inp_imgL[((col+1)+(row*imgW))])
	    				Assignment(Line_bufferR[((col+1)+(imgW*(FILTER_SIZE - 1)))],inp_imgR[((col+1)+(row*imgW))])
	    				Assignment(right_colL[(FILTER_SIZE-1)] , inp_imgL[((col+1)+(row*imgW))])
	    				Assignment(right_colR[(FILTER_SIZE-1)] , inp_imgR[((col+1)+(row*imgW))])
	    				
	 ##==========================================================================================================================	   				 
    			
	    			with ForLoopSection ("ii_loop1", "ii_0", 0, FILTER_SIZE):
	    				with ForLoopSection ("jj_loop1", "jj_0", 0, FILTER_SIZE-1):
	    					with LeafSection ("leaf_le_pp3_"+ str (row)+"_"+str (col)):
							Assignment(windowL[(jj_0+(ii_0*FILTER_SIZE))] , windowL[((jj_0+1)+(ii_0*FILTER_SIZE))])
							Assignment(windowR[(jj_0+(ii_0*FILTER_SIZE))] , windowR[((jj_0+1)+(ii_0*FILTER_SIZE))])
	    			
	    			with LeafSection ("leaf_le_pp39"):
					for ii in range(FILTER_SIZE):
						Assignment(windowL[((FILTER_SIZE-1)+(ii*FILTER_SIZE))] , right_colL[ii])
						Assignment(windowR[((FILTER_SIZE-1)+(ii*FILTER_SIZE))] , right_colR[ii])
	    			
	    			with ForLoopSection ("ii_loop2", "ii", 0, FILTER_SIZE):
	    				with ForLoopSection ("jj_loop2", "jj", 0, FILTER_SIZE):
	    					with LeafSection ("leaf_le_pp4"):
							Assignment(windowR_shift[(jj+(ii*FILTER_SIZE))] , windowR[(jj+(ii*FILTER_SIZE))])
	    			
	    			with LeafSection ("leaf_le_pp5_"+ str (row)+"_"+str (col)):
					Assignment(top_left_d_prev  , cost_row[((col)*SEARCH_RANGE)])
					Assignment(top_left_d , cost_row[((col)*SEARCH_RANGE)+1])
					Assignment(top_right_d_prev , cost_row[((col+2)*SEARCH_RANGE)])
					Assignment(top_right_d , cost_row[((col+2)*SEARCH_RANGE)+1])
					Assignment(top_d_prev , cost_row[((col+1)*SEARCH_RANGE)])
					Assignment(top_d , cost_row[((col+1)*SEARCH_RANGE)+1])
					Assignment(left_d_prev , cost_left[0])
					Assignment(left_d , cost_left[1])
				
				with SerialSections ("disp_output"):
		    			with ForLoopSection ("d_iter", "d", 0, (SEARCH_RANGE-2)):
		    				'''
		    				with LeafSection ("leaf_le_disp100"):
		    					#with Leaf:
		    					for ii in range(FILTER_SIZE):
			    					for jj in range(FILTER_SIZE):
			    						display ("windowL %d ", windowL[(jj+(ii*FILTER_SIZE))])
			    				for ii1 in range(FILTER_SIZE):
			    					for kk in range(FILTER_SIZE):
			    						display ("windowR_shift : %d ", windowR_shift[(kk+(ii1*FILTER_SIZE))])
						'''
						
						with LeafSection ("leaf_le_disp1"):
		    					Assignment(cost_row[(d+1)+(col*SEARCH_RANGE)] , left_d) 
		    					Assignment(top_left_d_forw    , cost_row[(d+2)+(col)*(SEARCH_RANGE)])
		    					Assignment(top_right_d_forw   , cost_row[(d+2)+((col+2)*(SEARCH_RANGE))])
		    					#display("top_right_d_forw = cost_row[(d+2)+((col+2)*(SEARCH_RANGE))]=%d",cost_row[(d+2)+((col+2)*(SEARCH_RANGE))])
		    					Assignment(top_d_forw         , cost_row[(d+2)+(col+1)*(SEARCH_RANGE)])
		    					Assignment(left_d_forw        , cost_left[d+2])
		    					
		    				with LeafSection ("leaf_le_disp2"):
		    					Assignment(x_ham , windowL[mid])
		    					Assignment(y_ham , windowR_shift[mid])
		    					Assignment(abs_sum , 0)
		    					for ii in range(N):
		    						if (windowL[ii] > x_ham) != (windowR_shift[ii] > y_ham):
		    							Assignment(abs_sum , abs_sum+1)
		    						else:
		    							Assignment(abs_sum , abs_sum)
		    					Assignment(ham_dist[d+1] , abs_sum)
		    					#display("for search depth of %d for pixel row=%d , col=%d obtained sum_cost is %d",(d+1),row,(col+1),abs_sum)
		    					Assignment(cap[0],top_left_d ) #dup2 
		    					Assignment(cap[1],top_left_d_prev)
		    					Assignment(cap[2],top_left_d_forw)
		    					Assignment(cap[3],min_cost_row[col])
		    					Assignment(cap[4],top_d)
		    					Assignment(cap[5],top_d_prev)
		    					Assignment(cap[6],top_d_forw)
		    					Assignment(cap[7],min_cost_row[col+1])
		    					Assignment(cap[8],top_right_d)
		    					Assignment(cap[9],top_right_d_prev)
		    					Assignment(cap[10],top_right_d_forw)
		    					Assignment(cap[11],min_cost_row[col+2]	)
		    					Assignment(cap[12],left_d)
		    					Assignment(cap[13],left_d_prev)
		    					Assignment(cap[14],left_d_forw)
		    					Assignment(cap[15],min_cost_left)
		    					Assignment(top_left_d_prev  , top_left_d)
			    				Assignment(top_left_d       , top_left_d_forw)
			    				Assignment(top_right_d_prev , top_right_d)
			    				Assignment(top_right_d      , top_right_d_forw)
			    				Assignment(top_d_prev       , top_d)
			    				Assignment(top_d            , top_d_forw)
			    				Assignment(left_d_prev      , left_d)
			    				Assignment(left_d           , left_d_forw)
		    				
		    				with LeafSection ("leaf_le_disp3"):
			    				for i in range(4):
		    						if(cap[i*4] > (cap[(i*4+1)]+P1)):
		    							Assignment(min1 , (cap[(i*4+1)]+P1))

		    						else :
		    							Assignment(min1 , cap[i*4])
		    						if((cap[(i*4+2)]+P1) > (cap[(i*4+3)]+P2)):
		    							Assignment(min2 , (cap[(i*4+3)]+P2))
		    						else :
		    							Assignment(min2 , (cap[(i*4+2)]+P1))
		    						if (min1 > min2) :
		    							Assignment(cost[i] , min2 - cap[(i*4+3)])
		    						else :
		    							Assignment(cost[i] , min1 - cap[(i*4+3)])
			    				for kk in range(FILTER_SIZE_1):
			    					for ii in range(FILTER_SIZE):
			    						Assignment(windowR_shift[FILTER_SIZE_1+(ii*FILTER_SIZE)-kk] , windowR_shift[((FILTER_SIZE_1-1)+(ii*FILTER_SIZE)-kk)])
		    				
		    				with LeafSection ("leaf_le_disp4"):
			    				Assignment(index, (((col-d)-FILTER_SIZE)+1))
			    				for ii in range(FILTER_SIZE):
			    					if(index > 65500):
			    						#display("index value is less than 0"))
			    						Assignment(windowR_shift[(ii*FILTER_SIZE)] , 0)
			    					else:
			    						#display("index value is more than 0")
			    						Assignment(windowR_shift[(ii*FILTER_SIZE)], Line_bufferR[((((col-d)-FILTER_SIZE)+1)+(ii*imgW))])
		    				with LeafSection ("leaf_le_disp45"):	
		    					Assignment(path_cost , (cost[0] + cost[1] + cost[2] + cost[3]))
		    					path_var =  ham_dist[d+1]
		    					sum_cost = ((path_cost) >> 2) + path_var
		    					
		    					if (sum_cost > (MAX_COST + P2)):
		    						Assignment(sum_cost , MAX_COST + P2)
		    					Assignment(cost_left[d+1] ,  sum_cost)
		    					if(sum_cost < min_sum_cost):
			    					Assignment(min_sum_cost , sum_cost)
			    					Assignment(winning_disp , d)
				
			    		with LeafSection ("leaf_le_out"):
			    			f_outD.write (winning_disp+1)
						Assignment(min_cost_row[col] , min_cost_left)
						Assignment(min_cost_left , min_sum_cost	)
'''						
	with SerialSections ("initial_P22"):    			
	    	with LeafSection ("results_out"):
		      for p in range (64):
		      	display ("reg_op[%0d] = [%0d]", p, reg_op[p])
                

'''

## testbench code =================
@hardware
def my_tb():
  m1 = Module ("m1", [], [], [])
  with LeafSection ("S10"):
      m1.start ()
  for l_in in range(T_S):
  #with ForLoopSection ("p1_fl1", "l_in", 0, T_S ):
	with LeafSection ("p1_fl1_l1"+ str (l_in)):
	  m1.m_["f_inL"].write (inL[l_in])
	  m1.m_["f_inR"].write (inR[l_in])
	  display ("my_tb : sending image pixels %0d and %0d.", (inL[l_in]),(inR[l_in]))
  with ForLoopSection ("TSINC", "m", 0, imgH*(imgW-2)):
        with LeafSection ("SP11_1"):
          display ("#Result (%0d) = [%0d]", m, m1.m_["f_outD"].read ())

t = Module ("", None, None , None )
t.emitVerilog (sys.stdout)
t = my_tb ("")
t.emitVerilog (sys.stdout)


