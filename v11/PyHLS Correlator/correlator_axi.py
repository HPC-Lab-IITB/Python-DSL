#----------#----------#----------# Import_Libraries
import math
tf_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#tf_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
from symbolic import *
from HPCpy import *

Reg_ip_count = 32
Reg_op_count = 64

BaseAddress = " 0x44A00000"

#Tb_vector = [i for i in range(128)] # + tf_list
Tb_vector=  [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]


#============================================


Reg_ip_AxiLite_count   = 1 # Ignored by the tool
Reg_ip_AxiStream_count = 1 # Ignored by the tool
Reg_op_AxiLite_count   = 1 # Ignored by the tool
Reg_op_AxiStream_count = 1 # Ignored by the tool


def Module(AxiStream):

    # User to add RegIn() and RegOut() here
         
    reg_ip = In_Ports()
    reg_op = Out_Ports()
    
    # User to add RegIn() and RegOut() ends
    
  
    # User to add Reg() and Var() here
    
    
    
    #======================================================== left_image elements ================================================================
    
    tmp_acc =  Var ("tmp_acc",32)
    input_block = [Reg ("input_block" + str(r), 32) for r in range (32)]
    inter_block = [Reg ("inter_block" + str(r), 32) for r in range (64)]
    output_block = [Reg ("output_block" + str(r), 64) for r in range (64)]
    jk = Var("jk",32)
    

    



    # Add user logic here
    
    with Parallel:
        for i in range(32):
            with Leaf:
                input_block[i]=reg_ip[i]
        		
        for i in range(32):
            with Leaf:
                inter_block[i]=tf_list[i]
       	
        		            
    
    with Series:
        with Leaf:
            for j in range (64):
                tmp_acc=0 
    		#display("=========================row value is %d",row)		
                for k in range (32):
                    #display("=========================col value is j=%d k=%d",j,k)
    		    #display("row = %d , col = %d " , j , k)
                    if(0 <= (j-k)):
                        if((j-k)<32):
                            #display("j-k = %d", (j-k))
                            #display("input_block[%d] = %d",k,inter_block[j-k])
                            tmp_acc=tmp_acc+ input_block[k] * tf_list[(j-k)]
                reg_op[j]=tmp_acc
            #for j in range (64):
            #    if(j>31):
             #       tmp_acc=0 
    		    #display("=========================row value is %d",row)		
                #    for k in range (32):
                        #display("=========================col value is j=%d k=%d",j,k)
    		        #display("row = %d , col = %d " , j , k)
                 #       if(0 <= (j-k)):
                  #          if((j-k)<32):
                                #display("j-k = %d", (j-k))
                                #display("input_block[%d] = %d",k,inter_block[j-k])
                   #             tmp_acc=tmp_acc+ input_block[k] * tf_list[(j-k)]
                    #reg_op[j]=tmp_acc       	

    #with Series:
  	
     #   with Leaf:
      #      for p in range(64):
    		#reg_op[p] = 2
       #         display ("reg_op[%0d] = [%0d]", p, reg_op[p])
	                
                                  
    # User logic ends

#----------#----------#----------# Hardware 


def my_tb():

    args = dict(( "reg_ip_" + str(i), Tb_vector[i]) for i in range(len(Tb_vector)))

    with Series:
      with Leaf:
          Module_dut.start(**args)
      with Leaf:
          for p in range(64):
              #for q in range(imgW):
              display ("Result_" + str(p) + "_" + " = %0d", Module_dut.isDone()[p])
