"""
@author: dhruva
"""

from symbolic import *

itf_list = [1, 1600, 40, 749, 2481, 1432, 2699, 687, 1583, 2760, 69, 543, 2532, 3136, 1410, 2267, 2508, 1355, 450, 936, 447, 2794, 1235, 1903, 1996, 1089, 3273, 283, 1853, 1990, 882, 3033, 2419, 2102, 219, 855, 2681, 1848, 712, 682, 927, 1795, 461, 1891, 2877, 2522, 1894, 1010, 1414, 2009, 3296, 464, 2697, 816, 1352, 2679, 1274, 1052, 1025, 2132, 1573, 76, 2998, 3040, 1175, 2444, 394, 1219, 2300, 1455, 2117, 1607, 2443, 554, 1179, 2186, 2303, 2926, 2237, 525, 735, 863, 2768, 1230, 2572, 556, 3010, 2266, 1684, 1239, 780, 2954, 109, 1292, 1031, 1745, 2688, 3061, 992, 2596, 941, 892, 1021, 2390, 642, 1868, 2377, 1482, 1540, 540, 1678, 1626, 279, 314, 1173, 2573, 3096, 48, 667, 1920, 2229, 1041, 2606, 1692, 680, 2746, 568, 3312]

def addr_gen(s, i):
    i = 6 - i
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
tf_addr  = tf_addr +  [0,0,0,0,0,0,0,0]
i1w_addr = [0,0,0,0,0,0,0,0] + i1r_addr
i2w_addr = [0,0,0,0,0,0,0,0] + i2r_addr 

invr_addr = [i for i in range(128)] + [0,0,0,0,0,0,0,0]
invw_addr = [0,0,0,0,0,0,0,0] + [i for i in range(128)]

@hardware
def intt (fin, fout):
    fin    = InputFifo  ("fin", 16)
    fout   = OutputFifo ("fout", 16)
    A      = [Reg ("A_"  + str (r),16) for r in range (128)]
    B      = [Reg ("B_"  + str (r),16) for r in range (128)]
    op1    = Reg ("op1" , 16)
    op2    = Reg ("op2" , 16)
    op3    = Reg ("op3" , 16)
    op4    = Reg ("op4" , 16)
    tfa    = Reg ("tfa"  , 16)
    tfb    = Reg ("tfb"  , 16)
    tf2c   = Reg ("tf2c" , 32)
    tf2d   = Reg ("tf2d" , 32)
    tf2e   = Reg ("tf2e" , 32)
    tf2f   = Reg ("tf2f" , 32)
    tf4c   = Reg ("tf4c" , 32)
    tf4d   = Reg ("tf4d" , 32)
    tf4e   = Reg ("tf4e" , 32)
    tf4f   = Reg ("tf4f" , 32)
    sum12  = Reg ("sum12", 16)
    sum34  = Reg ("sum34", 16)
    dif12  = Reg ("dif12", 16)
    dif34  = Reg ("dif34", 16)
    sum12c = Reg ("sum12c", 16)
    sum34c = Reg ("sum34c", 16)
    sum12d = Reg ("sum12d", 16)
    sum34d = Reg ("sum34d", 16)
    sum12e = Reg ("sum12e", 16)
    sum34e = Reg ("sum34e", 16)
    sum12f = Reg ("sum12f", 16)
    sum34f = Reg ("sum34f", 16)
    sum12g = Reg ("sum12g", 16)
    sum34g = Reg ("sum34g", 16)
    t0     = Reg ("t0", 48)
    t1     = Reg ("t1", 16)
    t2     = Reg ("t2", 32)
    t3     = Reg ("t3", 16)
    s0     = Reg ("s0", 48)
    s1     = Reg ("s1", 16)
    s2     = Reg ("s2", 32)
    s3     = Reg ("s3", 16)
    res1   = Reg ("res1", 16)
    res2   = Reg ("res2", 16)
    res3   = Reg ("res3", 16)
    res4   = Reg ("res4", 16)
    reg_vala = Reg ("reg_vala", 16)
    reg_valb = Reg ("reg_valb", 16)
    reg_inva = Reg ("reg_inva", 32)
    reg_invb = Reg ("reg_invb", 32)
    reg_inva2 = Reg ("reg_inva2", 32)
    reg_invb2 = Reg ("reg_invb2", 32)
    reg_inva3 = Reg ("reg_inva3", 32)
    reg_invb3 = Reg ("reg_invb3", 32)
    reg_inva4 = Reg ("reg_inva4", 32)
    reg_invb4 = Reg ("reg_invb4", 32)
    k0     = Reg ("k0", 48)
    k1     = Reg ("k1", 16)
    k2     = Reg ("k2", 32)
    k3     = Reg ("k3", 16)
    j0     = Reg ("j0", 48)
    j1     = Reg ("j1", 16)
    j2     = Reg ("j2", 32)
    j3     = Reg ("j3", 16)
    tempi  = Reg ("tempi", 16)
    tempj  = Reg ("tempj", 16)
    sum12_var = Var ("sum12_var", 16)
    sum34_var = Var ("sum34_var", 16)
    dif12_var = Var ("dif12_var", 16)
    dif34_var = Var ("dif34_var", 16)
        
    with ForLoopSection ("A_in", "p", 0, 128):
        with LeafSection ("S_i1"):
            for _p in range(128):
                if _p == p:
                    A[_p] = fin.read()

    with ForLoopSection ("B_in", "q", 0, 128):
        with LeafSection ("S_i2"):
            for _q in range(128):
                if _q == q:
                    B[_q] = fin.read()

    with ParallelSections ("PS1"):        
        with ForLoopSection ("R_l0", "i0", 0, 456): #loop running 7*64 times for 128 point NTT
            with LeafSection ("S0"):  #read operands from registers and twiddle factor
                for _i0 in range(456):
                    if (i0 == _i0):
                        op1 = A[i1r_addr[_i0]]
                        op2 = A[i2r_addr[_i0]]
                        op3 = B[i1r_addr[_i0]]
                        op4 = B[i2r_addr[_i0]]
                        tfa = itf_list[tf_addr[_i0]]

        with ForLoopSection ("R_l1", "i1", 0, 456):   
            with LeafSection ("S1"):
                #Modular addition and subtraction (cycle 1)
                sum12_var = op1 + op2
                if (sum12_var > 3329):
                    sum12 = sum12_var - 3329
                else:
                    sum12 = sum12_var

                dif12_var = op1 - op2
                if (op1 > op2):
                    dif12 = dif12_var
                else:
                    dif12 = dif12_var + 3329

                sum34_var = op3 + op4
                if (sum34_var > 3329):
                    sum34 = sum34_var - 3329
                else:
                    sum34 = sum34_var

                dif34_var = op3 - op4
                if (op3 > op4):
                    dif34 = dif34_var
                else:
                    dif34 = dif34_var + 3329

                tfb = tfa

        with ForLoopSection ("R_l2", "i2", 0, 456):
            with LeafSection ("S2"):
                #Multiplication of operand-2 with twiddle factor for Butterfly Operation (cycle 2)
                tf2c = dif12 * tfb
                sum12c = sum12

                tf4c = dif34 * tfb
                sum34c = sum34
                
        with ForLoopSection ("R_l3", "i3", 0, 456):    
            with LeafSection ("S3"):
                #Barret reduction step  (cycle 3)
                t0 =  tf2c * 5039
                tf2d = tf2c
                sum12d = sum12c

                s0 = tf4c * 5039
                tf4d = tf4c
                sum34d = sum34c

        with ForLoopSection ("R_l4", "i4", 0, 456):    
            with LeafSection ("S4"):
                #Barret reduction step  (cycle 4)
                tf2e = tf2d
                t1 = t0 >> 24
                sum12e = sum12d

                tf4e = tf4d
                s1 = s0 >> 24
                sum34e = sum34d

        with ForLoopSection ("R_l5", "i5", 0, 456):
            with LeafSection ("S5"):
                #Barret reduction step  (cycle 5)
                tf2f = tf2e
                t2 = (t1 << 11) + (t1 << 10) + (t1 << 8) + t1  #t2 = t1 * 3329
                sum12f = sum12e

                tf4f = tf4e
                s2 = (s1 << 11) + (s1 << 10) + (s1 << 8) + s1  #t4 = s1 * 3329
                sum34f = sum34e

        with ForLoopSection ("R_l6", "i6", 0, 456):
            with LeafSection ("S6"):
                #Barret reduction step  (cycle 6)
                t3 = tf2f - t2
                sum12g = sum12f

                s3 = tf4f - s2
                sum34g = sum34f
		        
        with ForLoopSection ("R_l7", "i7", 0, 456):
            with LeafSection ("S7"):
                #Barret reduction step  (cycle 7)
                if t3 > 3329:
                    res2 = t3 - 3329
                else:
                    res2 = t3
                res1 = sum12g

                if s3 > 3329:
                    res4 = s3 - 3329
                else:
                    res4 = s3
                res3 = sum34g

        with ForLoopSection ("R_l8", "i8", 0, 456):
            with LeafSection ("S8"):
            	for _i8 in range(456):
                	if (i8 == _i8):
				        #write results into registers
				        A[i1w_addr[_i8]] = res1
				        A[i2w_addr[_i8]] = res2
				        B[i1w_addr[_i8]] = res3
				        B[i2w_addr[_i8]] = res4

    #Pipeline to multiply with N^(-1) = 3303
    with ParallelSections ("PS2"):
        with ForLoopSection ("R_l9", "i9", 0, 135):
            with LeafSection ("S9"):
            	for _i9 in range(135):
                	if (i9 == _i9):
				        reg_vala = A[invr_addr[_i9]]
				        reg_valb = B[invr_addr[_i9]]

        with ForLoopSection ("R_l10", "i10", 0, 135):
            with LeafSection ("S10"):  #multiply input data with inv_N (cycle 1)
                reg_inva = reg_vala * 3303
                reg_invb = reg_valb * 3303
                
        with ForLoopSection ("R_l11", "i11", 0, 135):
            with LeafSection ("S11"): #Barret reduction step (cycle 2)
                k0 = reg_inva * 5039
                reg_inva2 = reg_inva
                j0 = reg_invb * 5039
                reg_invb2 = reg_invb

        with ForLoopSection ("R_l12", "i12", 0, 135):
            with LeafSection ("S12"): #Barret reduction step (cycle 2)
                k1 = k0 >> 24
                reg_inva3 = reg_inva2
                j1 = j0 >> 24
                reg_invb3 = reg_invb2

        with ForLoopSection ("R_l13", "i13", 0, 135):
            with LeafSection ("S13"): #Barret reduction step (cycle 3)
                k2 = (k1 << 11) + (k1 << 10) + (k1 << 8) + k1
                j2 = (j1 << 11) + (j1 << 10) + (j1 << 8) + j1
                reg_inva4 = reg_inva3
                reg_invb4 = reg_invb3
		
        with ForLoopSection ("R_l14", "i14", 0, 135):
            with LeafSection ("S14"): #Barret reduction step (cycle 4)
                k3 = reg_inva4 - k2
                j3 = reg_invb4 - j2
		        
        with ForLoopSection ("R_l15", "i15", 0, 135):
            with LeafSection ("S15"): #Barret reduction step (cycle 5)
                if k3 > 3329:
                    tempi = k3 - 3329
                else:
                    tempi = k3
                if j3 > 3329:
                    tempj = j3 - 3329
                else:
                    tempj = j3

        with ForLoopSection ("R_l16", "i16", 0, 135):
            with LeafSection ("S16"): #Final assignment
            	for _i16 in range(135):
                	if (i16 == _i16):
				        A[invw_addr[_i16]] = tempi
				        B[invw_addr[_i16]] = tempj
		                                            
    with ForLoopSection ("A_out", "r1", 0, 128):
        with LeafSection ("S_o1"):
            for _r1 in range(128):
                if _r1 == r1:
                    fout.write (A[_r1])

    with ForLoopSection ("B_out", "r2", 0, 128):
        with LeafSection ("S_o2"):
            for _r2 in range(128):
                if _r2 == r2:
                    fout.write (B[_r2])

@hardware
def my_tb():
    m1 = intt ("m1", [], [])
    with LeafSection ("S00"):
        m1.start ()
    with ParallelSections ("SP11"):
        with ForLoopSection ("TSRC", "l", 0, 256):
            with LeafSection ("SP11_0"):
                m1.m_["fin"].write (l)
                display ("my_tb : sending data %0d", l)
        with ForLoopSection ("TSINC", "m", 0, 256):
            with LeafSection ("SP11_1"):
                display ("#Result (%0d) = [%0d]", m, m1.m_["fout"].read ())

t = intt ("", None, None)
t.emitVerilog (sys.stdout)
t.dumpDot (sys.stderr)
t = my_tb ("")
t.emitVerilog (sys.stdout)
