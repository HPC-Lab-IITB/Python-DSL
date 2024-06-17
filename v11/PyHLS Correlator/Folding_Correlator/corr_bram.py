
from symbolic import *
import struct
@hardware
def corr_bram (fa, fb, fc ):
	ADDR_WIDTH=4
	#ref1=37 ref signal is of 16 width
	N=16
	bram_chain=2
	#ref2=49
	fa=InputFifo("fa",32)
	fb=InputFifo("fb",32)
	fc=OutputFifo("fc",32)
	inp_ram=SimpleBRAM("inp_ram",ADDR_WIDTH ,32)
	b11=SimpleBRAM("b11",1,32)
	b12=SimpleBRAM("b12",1,32)
	b13=SimpleBRAM("b13",1,32)
	b14=SimpleBRAM("b14",1,32)
	b21=SimpleBRAM("b21",1,32)
	b22=SimpleBRAM("b22",1,32)
	b23=SimpleBRAM("b23",1,32)
	b24=SimpleBRAM("b24",1,32)
	b31=SimpleBRAM("b31",1,32)
	b32=SimpleBRAM("b32",1,32)
	b33=SimpleBRAM("b33",1,32)
	b34=SimpleBRAM("b34",1,32)
	b41=SimpleBRAM("b41",1,32)
	b42=SimpleBRAM("b42",1,32)
	b43=SimpleBRAM("b43",1,32)
	b44=SimpleBRAM("b44",1,32)

	y11=SimpleBRAM("y11",1,32)
	y12=SimpleBRAM("y12",1,32)
	y13=SimpleBRAM("y13",1,32)
	y14=SimpleBRAM("y14",1,32)
	y21=SimpleBRAM("y21",1,32)
	y22=SimpleBRAM("y22",1,32)
	y23=SimpleBRAM("y23",1,32)
	y24=SimpleBRAM("y24",1,32)
	y31=SimpleBRAM("y31",1,32)
	y32=SimpleBRAM("y32",1,32)
	y33=SimpleBRAM("y33",1,32)
	y34=SimpleBRAM("y34",1,32)
	y41=SimpleBRAM("y41",1,32)
	y42=SimpleBRAM("y42",1,32)
	y43=SimpleBRAM("y43",1,32)
	y44=SimpleBRAM("y44",1,32)
	
	ref_ram=SimpleBRAM("ref_ram", ADDR_WIDTH, 32)
		
	result=Reg("result",32)

	rArr1 = Reg("rArr1", 32)
	rArr2 = Reg("rArr2", 32)
	rArr3 = Reg("rArr3", 32)
	rArr4 = Reg("rArr4", 32)

	ra=Reg("ra",ADDR_WIDTH)
	rb=Reg("rb",ADDR_WIDTH)
	#rc=Reg("rc",ADDR_WIDTH)
	with ParallelSections("p1"):
		with ForLoopSection("f1","i",0,N):
			with LeafSection("l1"):
				inp_ram.writeData(ra,fa.read())
				Assignment(ra,ra+Const(ADDR_WIDTH,1))
				#display ("inp ram: writing %0d at %0d", fa.read(), i)
		with ForLoopSection("f2","j",0,N):
			with LeafSection("l2"):
				ref_ram.writeData(rb,fb.read())
				Assignment(rb,rb+Const(ADDR_WIDTH,1))
				#display ("refe ram: writing %0d at %0d", fb.read(), j)
	with ParallelSections("p1_load"):
		with SerialSections("s0"):
			with LeafSection("l2_1"):
				ref_ram.readRequest(0)
			with LeafSection("l2_2"):
				y11.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(1)
			with LeafSection("l2_3"):
				y21.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(2)
			with LeafSection("l2_4"):
				y31.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(3)
			with LeafSection("l2_5"):
				y41.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(4)
			with LeafSection("l2_6"):
				y12.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(5)
			with LeafSection("l2_7"):
				y22.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(6)
			with LeafSection("l2_8"):
				y32.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(7)
			with LeafSection("l2_9"):
				y42.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(8)
			with LeafSection("l2_10"):
				y13.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(9)
			with LeafSection("l2_11"):
				y23.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(10)
			with LeafSection("l2_12"):
				y33.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(11)
			with LeafSection("l2_13"):
				y43.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(12)
			with LeafSection("l2_14"):
				y14.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(13)
			with LeafSection("l2_15"):
				y24.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(14)
			with LeafSection("l2_16"):
				y34.writeData(0,ref_ram.readResp())
				ref_ram.readRequest(15)
			with LeafSection("l2_17"):
				y44.writeData(0,ref_ram.readResp())
				
		with SerialSections("s1"):
			with LeafSection("l3_1"):
				inp_ram.readRequest(0)
			with LeafSection("l3_2"):
				b11.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(1)
			with LeafSection("l3_3"):
				b21.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(2)
			with LeafSection("l3_4"):
				b31.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(3)
			with LeafSection("l3_5"):
				b41.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(4)
			with LeafSection("l3_6"):
				b12.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(5)
			with LeafSection("l3_7"):
				b22.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(6)
			with LeafSection("l3_8"):
				b32.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(7)
			with LeafSection("l3_9"):
				b42.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(8)
			with LeafSection("l3_10"):
				b13.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(9)
			with LeafSection("l3_11"):
				b23.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(10)
			with LeafSection("l3_12"):
				b33.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(11)
			with LeafSection("l3_13"):
				b43.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(12)
			with LeafSection("l3_14"):
				b14.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(13)
			with LeafSection("l3_15"):
				b24.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(14)
			with LeafSection("l3_16"):
				b34.writeData(0,inp_ram.readResp())
				inp_ram.readRequest(15)
			with LeafSection("l3_17"):
				b44.writeData(0,inp_ram.readResp())
			
		
	with ForLoopSection("f3","l",0,N):
		with SerialSections("s2"):
			with ForLoopSection("f4","n",0,4):
				with LeafSection("l4_1"):
					b11.readRequest(0)
					b21.readRequest(0)
					b31.readRequest(0)
					b41.readRequest(0)
					y11.readRequest(0)
					y21.readRequest(0)
					y31.readRequest(0)
					y41.readRequest(0)
				with LeafSection("l4_2"):
					rArr1 = rArr1 + b11.readResp()*y11.readResp()
					rArr2 = rArr2 + b21.readResp()*y21.readResp()
					rArr3 = rArr3 + b31.readResp()*y31.readResp()
					rArr4 = rArr4 + b41.readResp()*y41.readResp()
				with ParallelSections("p2"):
					with LeafSection("l5_1"):
						b12.readRequest(0)
						b13.readRequest(0)
						b14.readRequest(0)
						b22.readRequest(0)
						b23.readRequest(0)
						b24.readRequest(0)
						b32.readRequest(0)
						b33.readRequest(0)
						b34.readRequest(0)
						b42.readRequest(0)
						b43.readRequest(0)
						b44.readRequest(0)
						
						y11.readRequest(0)
						y12.readRequest(0)
						y13.readRequest(0)
						y14.readRequest(0)
						y21.readRequest(0)
						y22.readRequest(0)
						y23.readRequest(0)
						y24.readRequest(0)
						y31.readRequest(0)
						y32.readRequest(0)
						y33.readRequest(0)
						y34.readRequest(0)
						y41.readRequest(0)
						y42.readRequest(0)
						y43.readRequest(0)
						y44.readRequest(0)
					with LeafSection("l5_2"):
						b11.writeData(0,b12.readResp())	
						b12.writeData(0,b13.readResp())
						b13.writeData(0,b14.readResp())			
						b21.writeData(0,b22.readResp())	
						b22.writeData(0,b23.readResp())
						b23.writeData(0,b24.readResp())
						b31.writeData(0,b32.readResp())	
						b32.writeData(0,b33.readResp())
						b33.writeData(0,b34.readResp())
						b41.writeData(0,b42.readResp())	
						b42.writeData(0,b43.readResp())
						b43.writeData(0,b44.readResp())
						
						y11.writeData(0,y12.readResp())	
						y12.writeData(0,y13.readResp())
						y13.writeData(0,y14.readResp())	
						y14.writeData(0,y11.readResp())			
						y21.writeData(0,y22.readResp())	
						y22.writeData(0,y23.readResp())
						y23.writeData(0,y24.readResp())
						y24.writeData(0,y21.readResp())	
						y31.writeData(0,y32.readResp())	
						y32.writeData(0,y33.readResp())
						y33.writeData(0,y34.readResp())
						y34.writeData(0,y31.readResp())	
						y41.writeData(0,y42.readResp())	
						y42.writeData(0,y43.readResp())
						y43.writeData(0,y44.readResp())
						y44.writeData(0,y41.readResp())	
				
				with SerialSections("s3"):						
					with LeafSection("l6_1"):
						if(n*4+l+1<16):
							inp_ram.readRequest(n*4+l+1)
						else:
							inp_ram.readRequest(0)
					with LeafSection("l6_2"):
						if(n*4+l+1<16):
							b14.writeData(0,inp_ram.readResp())
						else:
							b14.writeData(0,0)
						if(n*4+l+2<16):
							inp_ram.readRequest(n*4+l+2)
						else:
							inp_ram.readRequest(0)
					with LeafSection("l6_3"):
						if(n*4+l+2<16):
							b24.writeData(0,inp_ram.readResp())
						else:
							b24.writeData(0,0)
						if(n*4+l+3<16):
							inp_ram.readRequest(n*4+l+3)
						else:
							inp_ram.readRequest(0)
					with LeafSection("l6_4"):
						if(n*4+l+3<16):
							b34.writeData(0,inp_ram.readResp())
						else:
							b34.writeData(0,0)
						if(n*4+l+4<16):
							inp_ram.readRequest(n*4+l+4)
						else:
							inp_ram.readRequest(0)
					with LeafSection("l6_5"):
						if(n*4+l+4<16):
							b44.writeData(0,inp_ram.readResp())
						else:
							b44.writeData(0,0)
			with LeafSection("l7_1"):
				result = rArr1 + rArr2 + rArr3 + rArr4
			with LeafSection("l7_2"):
				fc.write(result)
				rArr1 = 0
				rArr2 = 0
				rArr3 = 0
				rArr4 = 0
	
   			
@hardware
def my_tb():
    NN = 16
    m1 = corr_bram ("m1", [], [], [])
    with LeafSection ("S10"):
      m1.start ()
    with ParallelSections ("SP11"):
      with ForLoopSection ("TSRC", "l", 0, NN ):
        with LeafSection ("SP11_0"):
          m1.m_["fb"].write (l)
          #m1.m_["fB"].write (l * 2)
          display ("my_tb : sending data %0d", l)
     
      with ForLoopSection("input_send","c2",0,NN):
	with LeafSection ("SP11_12"):        
	  m1.m_["fa"].write (c2)
       	  display ("my_tb : sending data %0d", c2)

      with ForLoopSection ("TSINC", "c3", 0, NN):
        with LeafSection ("SP11_1"):
            display ("#Result = [%0d]", m1.m_["fc"].read ())

t = corr_bram ("", None, None, None)
t.emitVerilog (sys.stdout)
t.dumpDot (sys.stderr)
t = my_tb ("")
t.emitVerilog (sys.stdout)	
