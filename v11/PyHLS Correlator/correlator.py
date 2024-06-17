
from symbolic import *
from scalar_fma_tmp import *
import struct
@hardware
def correlator (fa, fb, fc ):
	ADDR_WIDTH=10
	ref1=37
	N=256
	#ref2=49
	fa=InputFifo("fa",32)
	fb=InputFifo("fb",32)
	fc=OutputFifo("fc",32)
	#inp_ram=SimpleBRAM("inp_ram", ADDR_WIDTH, 32)
	tmp_ram=SimpleBRAM("tmp_ram", ADDR_WIDTH, 32)
	ref_ram=SimpleBRAM("ref_ram", ADDR_WIDTH, 32)
	out_ram=SimpleBRAM("out_ram", ADDR_WIDTH, 32)
	temp_buff=Reg("temp_buff",32)
	flagb=Reg("flagb",ADDR_WIDTH)
	out_calc=Reg("out_clac",32)
	
	ra=Reg("ra",ADDR_WIDTH)
	rb=Reg("rb",ADDR_WIDTH)
	rc=Reg("rc",ADDR_WIDTH)
	with ParallelSections("p1"):
		#with ForLoopSection("f1","i",0,N):
		#	with LeafSection("l1"):
		#		inp_ram.writeData(ra,fa.read())
		#		Assignment(ra,ra+Const(ADDR_WIDTH,1))
				#display ("inp ram: writing %0d at %0d", fa.read(), i)
		with ForLoopSection("f2","j",0,ref1):
			with LeafSection("l2"):
				ref_ram.writeData(rb,fb.read())
				Assignment(rb,rb+Const(ADDR_WIDTH,1))
				#display ("refe ram: writing %0d at %0d", fb.read(), j)
	
		
	with ForLoopSection("f3","k",0,N):
		with LeafSection("rc_init"):
			rc=1
		with SerialSections("s2"):
			with ForLoopSection("f4","l",1,N):
				with SerialSections("s2"):
					with LeafSection("shift_input_read_req"):
						tmp_ram.readRequest(Const(ADDR_WIDTH,N)-l-Const(ADDR_WIDTH,1))
					with LeafSection("shift_input_read_req_1"):
						temp_buff=tmp_ram.readResp()							
					with LeafSection("shift_input_read_req_2"):
						tmp_ram.writeData(Const(ADDR_WIDTH,N)-l,temp_buff)
						Assignment(rc,rc+Const(ADDR_WIDTH,0))
						
			#with LeafSection("inp_at_zero_loc"):
			#	inp_ram.readRequest(k)
				
			with LeafSection("read_inp_stream"):
				tmp_ram.writeData(Const(ADDR_WIDTH,0),fa.read())
				Assignment(out_calc,Const(32,0))
				Assignment(flagb,Const(ADDR_WIDTH,0))
			with ForLoopSection("f5","n",0,N):
				with SerialSections("s3"):
					with LeafSection("calc1"):
						tmp_ram.readRequest(n)
						ref_ram.readRequest(flagb)
						if flagb==36:
							Assignment(flagb,Const(ADDR_WIDTH,0))
						else:
							Assignment(flagb,flagb+Const(ADDR_WIDTH,1))
					with LeafSection("calc2"):
						out_calc=out_calc+tmp_ram.readResp()*ref_ram.readResp()
			with LeafSection("store_outp"):
				out_ram.writeData(k,out_calc)
				fc.write (out_calc)
   			
@hardware
def my_tb():
    NN = 256
    m1 = correlator ("m1", [], [], [])
    with LeafSection ("S10"):
      m1.start ()
    with ParallelSections ("SP11"):
      with ForLoopSection ("TSRC", "l", 0, 37 ):
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

t = correlator ("", None, None, None)
t.emitVerilog (sys.stdout)
t.dumpDot (sys.stderr)
t = my_tb ("")
t.emitVerilog (sys.stdout)	
