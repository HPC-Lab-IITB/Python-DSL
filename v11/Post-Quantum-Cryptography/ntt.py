from symbolic import *

tf_list = [1, 1729, 2580, 3289, 2642, 630, 1897, 848, 1062, 1919, 193, 797, 2786, 3260, 569, 1746, 296, 2447, 1339, 1476, 3046, 56, 2240, 1333, 1426, 2094, 535, 2882, 2393, 2879, 1974, 821, 289, 331, 3253, 1756, 1197, 2304, 2277, 2055, 650, 1977, 2513, 632, 2865, 33, 1320, 1915, 2319, 1435, 807, 452, 1438, 2868, 1534, 2402, 2647, 2617, 1481, 648, 2474, 3110, 1227, 910, 17, 2761, 583, 2649, 1637, 723, 2288, 1100, 1409, 2662, 3281, 233, 756, 2156, 3015, 3050, 1703, 1651, 2789, 1789, 1847, 952, 1461, 2687, 939, 2308, 2437, 2388, 733, 2337, 268, 641, 1584, 2298, 2037, 3220, 375, 2549, 2090, 1645, 1063, 319, 2773, 757, 2099, 561, 2466, 2594, 2804, 1092, 403, 1026, 1143, 2150, 2775, 886, 1722, 1212, 1874, 1029, 2110, 2935, 885, 2154]

def addr_gen(s, i):
    j = s >> (6 - i)
    k = s & ((64 >> i) - 1)
    ie_r = j * (1 << (7 - i)) + k
    io_r = ie_r + (1 << (6 - i))
    iw = (1 << i) + (s >> (6 - i))
    return ie_r, io_r, iw
    
i1r_addr = []
i2r_addr = []
i1w_addr = []
i2w_addr = []
tf_addr  = []

for i in range(7): 
    for s in range(64):
        ie, io, iw = addr_gen(s, i)
        i1r_addr.append(ie)
        i2r_addr.append(io)
        tf_addr.append(iw)   
             
i1r_addr = i1r_addr + [0,0,0,0,0,0,0,0]
i2r_addr = i2r_addr + [0,0,0,0,0,0,0,0]
tf_addr  = tf_addr + [0,0,0,0,0,0,0,0]
i1w_addr = [0,0,0,0,0,0,0,0] + i1r_addr
i2w_addr = [0,0,0,0,0,0,0,0] + i2r_addr 

@hardware
def ntt (fin, fout):
    fin    = InputFifo  ("fin", 16)
    fout   = OutputFifo ("fout", 16)
    A      = [Reg ("A_"  + str (r),16) for r in range (128)]
    B      = [Reg ("B_"  + str (r),16) for r in range (128)]
    op1    = Reg ("op1" , 16)
    op11   = Reg ("op11", 16)
    op12   = Reg ("op12", 16)
    op13   = Reg ("op13", 16)
    op14   = Reg ("op14", 16)
    op15   = Reg ("op15", 16)
    op16   = Reg ("op16", 16)
    op2    = Reg ("op2" , 16)
    op3    = Reg ("op3" , 16)
    op31   = Reg ("op31", 16)
    op32   = Reg ("op32", 16)
    op33   = Reg ("op33", 16)
    op34   = Reg ("op34", 16)
    op35   = Reg ("op35", 16)
    op36   = Reg ("op36", 16)
    op4    = Reg ("op4" , 16)
    tf     = Reg ("tf"  , 16)
    op2tf  = Reg ("op2tf" , 32)
    op2tf1 = Reg ("op2tf1", 32)
    op2tf2 = Reg ("op2tf2", 32)
    op2tf3 = Reg ("op2tf3", 32)
    t0     = Reg ("t0", 48)
    t1     = Reg ("t1", 16)
    t2     = Reg ("t2", 32)
    t3     = Reg ("t3", 16)
    t4     = Reg ("t4", 16)
    res1   = Reg ("res1", 16)
    res2   = Reg ("res2", 16)
    op4tf  = Reg ("op4tf" , 32)
    op4tf1 = Reg ("op4tf1", 32)
    op4tf2 = Reg ("op4tf2", 32)
    op4tf3 = Reg ("op4tf3", 32)
    s0     = Reg ("s0", 48)
    s1     = Reg ("s1", 16)
    s2     = Reg ("s2", 32)
    s3     = Reg ("s3", 16)
    s4     = Reg ("s4", 16)
    res3   = Reg ("res3", 16)
    res4   = Reg ("res4", 16)
    
    with ForLoopSection ("A_in", "p", 0, 128):
        with LeafSection ("recv_A"):
            for _p in range(128):
                if _p == p:
                    A[_p] = fin.read()

    with ForLoopSection ("B_in", "q", 0, 128):
        with LeafSection ("recv_B"):
            for _q in range(128):
                if _q == q:
                    B[_q] = fin.read()
                    
    with ParallelSections ("PS"):        
        with ForLoopSection ("R_l0", "i", 0, 456): #loop running 7*64 times for 128 point NTT
            with LeafSection ("S0"):  #read operands from registers and twiddle factor
                for _i in range(456):
                    if (i == _i):
                        op1 = A[i1r_addr[_i]]
                        op2 = A[i2r_addr[_i]]
                        op3 = B[i1r_addr[_i]]
                        op4 = B[i2r_addr[_i]]
                        tf = tf_list[tf_addr[_i]]
        
        with ForLoopSection ("R_l1", "i1", 0, 456):            
            with LeafSection ("S1"): #multiplication of operand-2 with twiddle factor for Butterfly Operation	
                op2tf = op2 * tf   
                op11 = op1
                op4tf = op4 * tf   
                op31 = op3
                                
        with ForLoopSection ("R_l2", "i2", 0, 456):
            with LeafSection ("S2"): #Barret reduction step
                t0 = op2tf * 5039
                op2tf1 = op2tf
                op12 = op11
                s0 = op4tf * 5039
                op4tf1 = op4tf
                op32 = op31
                                
        with ForLoopSection ("R_l3", "i3", 0, 456):
            with LeafSection ("S3"): #Barret reduction step
                t1 = t0 >> 24
                op2tf2 = op2tf1
                op13 = op12
                s1 = s0 >> 24
                op4tf2 = op4tf1
                op33 = op32
                                
        with ForLoopSection ("R_l4", "i4", 0, 456):		            
            with LeafSection ("S4"): #Barret reduction step
                t2 = (t1 << 11) + (t1 << 10) + (t1 << 8) + t1
                op2tf3 = op2tf2
                op14 = op13
                s2 = (s1 << 11) + (s1 << 10) + (s1 << 8) + s1
                op4tf3 = op4tf2
                op34 = op33
                
        with ForLoopSection ("R_l5", "i5", 0, 456):
            with LeafSection ("S5"): #Barret reduction step
                t3 = op2tf3 - t2
                op15 = op14 
                s3 = op4tf3 - s2
                op35 = op34 
                
        with ForLoopSection ("R_l6", "i6", 0, 456):
            with LeafSection ("S6"): #Barret reduction step
                if t3 > 3329:
                    t4 = t3 - 3329
                else:
                	t4 = t3
                op16 = op15
                if s3 > 3329:
                    s4 = s3 - 3329
                else:
                	s4 = s3
                op36 = op35
                
        with ForLoopSection ("R_l7", "i7", 0, 456):
            with LeafSection ("S7"): #modular addition and subtraction for Butterfly Operation
                if (op16 + t4 > 3329):
                    res1 = t4 + op16 - 3329
                else:
                    res1 = t4 + op16
                
                if (t4 > op16): 
                    res2 = (op16 + 3329 - t4)
                else:
                    res2 = (op16 - t4)

                if (op36 + s4 > 3329):
                    res3 = s4 + op36 - 3329
                else:
                    res3 = s4 + op36
                
                if (s4 > op36): 
                    res4 = (op36 + 3329 - s4)
                else:
                    res4 = (op36 - s4)

        with ForLoopSection ("R_l8", "j", 0, 456):	        
            with LeafSection ("S8"): #writing Butterfly operation results back into registers
                for _j in range(0, 456):
                    if (j == _j):
                        A[i1w_addr[_j]] = res1
                        A[i2w_addr[_j]] = res2
                        B[i1w_addr[_j]] = res3
                        B[i2w_addr[_j]] = res4
                        
    with ForLoopSection ("A_out", "r", 0, 128):
        with LeafSection ("result_outA"):
            for _r in range(128):
                if _r == r:
                    #display ("Register A: sending %0d", A[_r])
                    fout.write (A[_r])

    with ForLoopSection ("B_out", "s", 0, 128):
        with LeafSection ("result_outB"):
            for _s in range(128):
                if _s == s:
                    #display ("Register A: sending %0d", A[_r])
                    fout.write (B[_s])
@hardware
def my_tb():
    m1 = ntt ("m1", [], [])
    with LeafSection ("S10"):
        m1.start ()
    with ParallelSections ("SP11"):
        with ForLoopSection ("TSRC", "l", 0, 256):
            with LeafSection ("SP11_0"):
                m1.m_["fin"].write (l)
                display ("my_tb : sending data %0d", l)
        with ForLoopSection ("TSINC", "m", 0, 256):
            with LeafSection ("SP11_1"):
                display ("#Result (%0d) = [%0d]", m, m1.m_["fout"].read ())

t = ntt ("", None, None)
t.emitVerilog (sys.stdout)
t.dumpDot (sys.stderr)
t = my_tb ("")
t.emitVerilog (sys.stdout)
