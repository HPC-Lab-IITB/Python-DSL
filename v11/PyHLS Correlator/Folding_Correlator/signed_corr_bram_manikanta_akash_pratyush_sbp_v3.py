
from symbolic import *
import struct

@hardware
def signed_corr_bram_manikanta_akash_pratyush_sbp_v3 (fa, fb, fc ):
  ADDR_WIDTH_inp_bram=4
  ADDR_WIDTH=3
  K = 1 << ADDR_WIDTH
  Kby2 = 1 << ( ADDR_WIDTH-1 )
  #ref1=37 ref signal is of 16 width
  N=16
  fa=InputFifo("fa",32)
  fb=InputFifo("fb",32)
  fc=OutputFifo("fc",32)
  inp_ram=SimpleBRAM("inp_ram",ADDR_WIDTH_inp_bram ,32)
  b1=SimpleBRAM("b1",ADDR_WIDTH,32)
  b2=SimpleBRAM("b2",ADDR_WIDTH,32)
  b3=SimpleBRAM("b3",ADDR_WIDTH,32)
  b4=SimpleBRAM("b4",ADDR_WIDTH,32)
  result=SignedReg("result",32)

  rArr1 = SignedReg("rArr1", 32)
  rArr2 = SignedReg("rArr2", 32)
  rArr3 = SignedReg("rArr3", 32)
  rArr4 = SignedReg("rArr4", 32)

  ra=Reg("ra",ADDR_WIDTH_inp_bram)

  b1waddr = Reg("b1waddr",ADDR_WIDTH)
  b1raddr = Reg("b1raddr",ADDR_WIDTH)
  b2waddr = Reg("b2waddr",ADDR_WIDTH)
  b2raddr = Reg("b2raddr",ADDR_WIDTH)
  b3waddr = Reg("b3waddr",ADDR_WIDTH)
  b3raddr = Reg("b3raddr",ADDR_WIDTH)
  b4waddr = Reg("b4waddr",ADDR_WIDTH)
  b4raddr = Reg("b4raddr",ADDR_WIDTH)

  with SerialSections("m") :
    with ForLoopSection("f1","i",0,N):
      with LeafSection("l1"):
        inp_ram.writeData(ra,fa.read())
        Assignment(ra,ra+Const(ADDR_WIDTH,1))
        display ("inp ram: writing %0d at %0d", fa.read(), i)
    with ForLoopSection("m_f4","nn04",0,4):
      with LeafSection("m_f4_l1"):
        #display("readRequest to inp_ram")
        inp_ram.readRequest(nn04)
      with LeafSection("m_f4_l2"):
        b4.writeData(b4waddr,inp_ram.readResp())
        #display ("b4: writing %0d at %0d", inp_ram.readResp(), b4waddr)
        if ( b4waddr == 0 ) :
          b4waddr = b4waddr + (K-1)
        else :
          b4waddr = b4waddr - 1 
    with ForLoopSection("m_f3","nn03",4,8):
      with LeafSection("m_f3_l1"):
        #display("readRequest to inp_ram")
        inp_ram.readRequest(nn03)
      with LeafSection("m_f3_l2"):
        b3.writeData(b3waddr,inp_ram.readResp())
        #display ("b3: writing %0d at %0d", inp_ram.readResp(), b3waddr)
        if ( b3waddr == 0 ) :
          b3waddr = b3waddr + (K-1)
        else :
          b3waddr = b3waddr - 1 
    with ForLoopSection("m_f2","nn02",8,12):
      with LeafSection("m_f2_l1"):
        #display("readRequest to inp_ram")
        inp_ram.readRequest(nn02)
      with LeafSection("m_f2_l2"):
        b2.writeData(b2waddr,inp_ram.readResp())
        #display ("b2: writing %0d at %0d", inp_ram.readResp(), b2waddr)
        if ( b2waddr == 0 ) :
          b2waddr = b2waddr + (K-1)
        else :
          b2waddr = b2waddr - 1 
    with ForLoopSection("m_f1","nn01",12,16):
      with LeafSection("m_f1_l1"):
        #display("readRequest to inp_ram")
        inp_ram.readRequest(nn01)
      with LeafSection("m_f1_l2"):
        b1.writeData(b1waddr,inp_ram.readResp())
        #display ("b1: writing %0d at %0d", inp_ram.readResp(), b1waddr)
        if ( b1waddr == 0 ) :
          b1waddr = b1waddr + (K-1)
        else :
          b1waddr = b1waddr - 1 

    with LeafSection("pre_p1_load_f1"):
      b1.readRequest(b1raddr)
      b2.readRequest(b2raddr)
      b3.readRequest(b3raddr)
      b4.readRequest(b4raddr)
      if ( b1raddr == 0 ) :
        b1raddr = b1raddr + (K-1)
      else :
        b1raddr = b1raddr - 1 
      if ( b2raddr == 0 ) :
        b2raddr = b2raddr + (K-1)
      else :
        b2raddr = b2raddr - 1 
      if ( b3raddr == 0 ) :
        b3raddr = b3raddr + (K-1)
      else :
        b3raddr = b3raddr - 1 
      if ( b4raddr == 0 ) :
        b4raddr = b4raddr + (K-1)
      else :
        b4raddr = b4raddr - 1 

    with ForLoopSection("p1_load_f1","nn",0,4):
      with LeafSection("p1_load_f1_l1"):
        #display("dummy ")
        inp_ram.readRequest(nn)
      with ParallelSections("p1_load_fl_p2_"):
        with LeafSection("l2_2"):
          #display("loop iteration index nn is %0d", nn)
          b1.writeData(b1waddr,inp_ram.readResp())
          b1.readRequest(b1raddr)
          #display ("b1: readRequest at %0d", b1raddr)
          if ( b1waddr == 0 ) :
            b1waddr = b1waddr + (K-1)
          else :
            b1waddr = b1waddr - 1 
          if ( b1raddr == 0 ) :
            b1raddr = b1raddr + (K-1)
          else :
            b1raddr = b1raddr - 1 
        with LeafSection("l2_3"):
          #display("loop iteration index nn is %0d", nn)
          b2.writeData(b2waddr,b1.readResp())
          b2.readRequest(b2raddr)
          #display ("b2: readRequest at %0d", b2raddr)
          if ( b2waddr == 0 ) :
            b2waddr = b2waddr + (K-1)
          else :
            b2waddr = b2waddr - 1 
          if ( b2raddr == 0 ) :
            b2raddr = b2raddr + (K-1)
          else :
            b2raddr = b2raddr - 1 
          #display("b1 readResp gives %0d", b1.readResp() )
          rArr1 = rArr1 + b1.readResp()*b1.readResp()
        with LeafSection("l2_4"):
          #display("loop iteration index nn is %0d", nn)
          b3.writeData(b3waddr,b2.readResp())
          b3.readRequest(b3raddr)
          #display ("b3: readRequest at %0d", b3raddr)
          if ( b3waddr == 0 ) :
            b3waddr = b3waddr + (K-1)
          else :
            b3waddr = b3waddr - 1 
          if ( b3raddr == 0 ) :
            b3raddr = b3raddr + (K-1)
          else :
            b3raddr = b3raddr - 1 
          #display("b2 readResp gives %0d", b2.readResp() )
          rArr2 = rArr2 + b2.readResp()*b2.readResp()
        with LeafSection("l2_5"):
          #display("loop iteration index nn is %0d", nn)
          b4.writeData(b4waddr,b3.readResp())
          b4.readRequest(b4raddr)
          #display ("b4: readRequest at %0d", b4raddr)
          if ( b4waddr == 0 ) :
            b4waddr = b4waddr + (K-1)
          else :
            b4waddr = b4waddr - 1 
          if ( b4raddr == 0 ) :
            b4raddr = b4raddr + (K-1)
          else :
            b4raddr = b4raddr - 1 
          #display("b3 readResp gives %0d", b3.readResp() )
          rArr3 = rArr3 + b3.readResp()*b3.readResp()
        with LeafSection("l2_6"):
          #display("loop iteration index nn is %0d", nn)
          #display("b4 readResp gives %0d", b4.readResp() )
          rArr4 = rArr4 + b4.readResp()*b4.readResp()
  
    with LeafSection("l7_1"):
      result = SignedConst(32,0) - rArr1 - rArr2 - rArr3 - rArr4
    with LeafSection("l7_2"):
      display( "writing [%0d] to fC" , result )  
      fc.write(result)
      rArr1 = 0
      rArr2 = 0
      rArr3 = 0
      rArr4 = 0


@hardware
def my_tb():
    NN = 16
    m1 = signed_corr_bram_manikanta_akash_pratyush_sbp_v3 ("m1", [], [], [])
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

t = signed_corr_bram_manikanta_akash_pratyush_sbp_v3 ("", None, None, None)
t.emitVerilog (sys.stdout)
t.dumpDot (sys.stderr)
t = my_tb ("")
t.emitVerilog (sys.stdout)  
