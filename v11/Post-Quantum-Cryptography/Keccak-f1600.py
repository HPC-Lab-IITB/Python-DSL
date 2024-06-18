"""
@author: dhruva
"""

from symbolic import *

THETA_REORDER = [[4, 0, 1, 2, 3], [1, 2, 3, 4, 0]]

RHO_SHIFTS = [[0,  36, 3,  41, 18],
              [1,  44, 10, 45, 2 ],
              [62, 6,  43, 15, 61],
              [28, 55, 25, 21, 56],
              [27, 20, 39, 8,  14]]
              
PI_ROW_REORDER = [[0, 3, 1, 4, 2],
                  [1, 4, 2, 0, 3],
                  [2, 0, 3, 1, 4],
                  [3, 1, 4, 2, 0],
                  [4, 2, 0, 3, 1]]


PI_COLUMN_REORDER = [[0, 0, 0, 0, 0],
		             [1, 1, 1, 1, 1],
		             [2, 2, 2, 2, 2],
		             [3, 3, 3, 3, 3],
		             [4, 4, 4, 4, 4]]

CHI_REORDER = [[1, 2, 3, 4, 0], [2, 3, 4, 0, 1]]

# Had to split IOTA_CONSTANTs into 32-bit constants because Verilator wasn't allowing 64-bit constants...          
IOTA_CONSTANTS1 = [0x00000001, 0x00008082, 0x0000808A,
                   0x80008000, 0x0000808B, 0x80000001,
                   0x80008081, 0x00008009, 0x0000008A,
                   0x00000088, 0x80008009, 0x8000000A,
                   0x8000808B, 0x0000008B, 0x00008089,
                   0x00008003, 0x00008002, 0x00000080,
                   0x0000800A, 0x8000000A, 0x80008081,
                   0x00008080, 0x80000001, 0x80008008]

IOTA_CONSTANTS2 = [0x00000000, 0x00000000, 0x80000000,
                   0x80000000, 0x00000000, 0x00000000,
                   0x80000000, 0x80000000, 0x00000000,
                   0x00000000, 0x00000000, 0x00000000,
                   0x00000000, 0x80000000, 0x80000000,
                   0x80000000, 0x80000000, 0x80000000,
                   0x00000000, 0x80000000, 0x80000000,
                   0x80000000, 0x00000000, 0x80000000]                  

@hardware
def keccakf1600 (fin, fout):
    fin           = InputFifo  ("fin", 8)
    fout          = OutputFifo ("fout", 8)
    
    reg           = [Reg ("reg_" + str(r), 8) for r in range(200)]

    state         = [Reg ("state_" + str(r) + "_" + str(c), 64) 
    				 for r in range (5) for c in range (5)]

    arr_shift     = [Reg ("arr_shift_" + str(r) + "_" + str(c), 64) 
    				 for r in range (5) for c in range (5)]

    ro_state      = [Reg ("ro_state_" + str(r) + "_" + str(c), 64) 
    				 for r in range (5) for c in range (5)]

    ro_arr_shift  = [Reg ("ro_arr_shift_" + str(r) + "_" + str(c), 64) 
    				 for r in range (5) for c in range (5)]

    s_0           = [Reg ("s_0_" + str(r), 64) for r in range (5)]
    s_1           = [Reg ("s_1_" + str(r), 64) for r in range (5)]

    ro_state_x    = [Reg ("ro_state_x_" + str(r) + "_" + str(c), 64) 
    				 for r in range (5) for c in range (5)]

    ro_state_y    = [Reg ("ro_state_y_" + str(r) + "_" + str(c), 64) 
    				 for r in range (5) for c in range (5)]
    
    ro_state_xvar = [Var ("ro_state_xvar_" + str(r) + "_" + str(c), 64)
    				 for r in range (5) for c in range (5)]

    all_ones      = Var ("all_ones", 32)
    iota_val1     = Var ("iota_val1", 32)
    iota_val2     = Var ("iota_val2", 32)

    with ForLoopSection ("FLS_0", "p", 0, 200):
        with LeafSection ("LS_0"):
            for _p in range(200):
                if _p == p:
                    reg[_p] = fin.read() 
                    
    with LeafSection ("LS_1"):
        for i in range(5):
            for j in range(5): 
                state[5*i + j][0 :7 ] = reg[40*j + 8*i]
                state[5*i + j][8 :15] = reg[40*j + 8*i + 1]
                state[5*i + j][16:23] = reg[40*j + 8*i + 2]
                state[5*i + j][24:31] = reg[40*j + 8*i + 3]
                state[5*i + j][32:39] = reg[40*j + 8*i + 4]
                state[5*i + j][40:47] = reg[40*j + 8*i + 5]
                state[5*i + j][48:55] = reg[40*j + 8*i + 6]
                state[5*i + j][56:63] = reg[40*j + 8*i + 7]
                
    with ForLoopSection ("FLS_1", "q", 0, 24):
        with LeafSection ("LS_2"): #theta step 1
            for i in range(5):
                for j in range(5):
                    arr_shift[5*i + j] = (state[5*i + j] << 1) | (state[5*i + j] >> 63)
                
        with LeafSection ("LS_3"): #theta step 2
            for i in range(5):
                for j in range(5):
                    ro_state[5*i+j] = state[5*THETA_REORDER[0][i] + j]
                    ro_arr_shift[5*i+j] = arr_shift[5*THETA_REORDER[1][i] + j]
        
        with LeafSection ("LS_4"): #theta step 3	
            for i in range(5):
                s_0[i] = ro_state[5*i] ^ ro_state[5*i+1] ^ ro_state[5*i+2] ^ ro_state[5*i+3] ^ ro_state[5*i+4]			
                s_1[i] = ro_arr_shift[5*i] ^ ro_arr_shift[5*i+1] ^ ro_arr_shift[5*i+2] ^ ro_arr_shift[5*i+3] ^ ro_arr_shift[5*i+4]	
        
        with LeafSection ("LS_5"): #theta step 4
            for i in range(5): 
                for j in range(5):
                    state[5*i+j] = state[5*i+j] ^ s_0[i] ^ s_1[i]	
                
        with LeafSection ("LS_6"): #rho step 1
            for i in range(5):
                for j in range(5):
                    state[5*i+j] = (state[5*i+j] << RHO_SHIFTS[i][j]) | state[5*i+j] >> (64 - RHO_SHIFTS[i][j])	
        
        with LeafSection ("LS_7"): #pi step 1
            for i in range(5):
                for j in range(5):
                    state[5*i+j] = state[5*PI_ROW_REORDER[i][j] + PI_COLUMN_REORDER[i][j]]
        
        with LeafSection ("LS_8"): #chi step 1
            for i in range(5):
                for j in range(5):
                    ro_state_x[5*i+j] = state[5*CHI_REORDER[0][i] + j]
                    ro_state_y[5*i+j] = state[5*CHI_REORDER[1][i] + j]
        
        with LeafSection ("LS_9"): #chi step 2
            all_ones = 0xFFFFFFFF #XORing with all ones because binary operation (i.e negation) wasn't allowed...
            for i in range(5):
                for j in range(5):  
                    ro_state_xvar[5*i+j][0 :31] = all_ones ^ ro_state_x[5*i+j][0 :31]
                    ro_state_xvar[5*i+j][32:63] = all_ones ^ ro_state_x[5*i+j][32:63]
                    state[5*i+j] = state[5*i+j] ^ (ro_state_xvar[5*i+j] & ro_state_y[5*i+j])
                    
        with LeafSection ("LS_10"): #iota step 1
            for _q in range(24):
                if (_q == q):
                    iota_val1 = IOTA_CONSTANTS1[_q]
                    iota_val2 = IOTA_CONSTANTS2[_q]
                    state[0][0 :31] = iota_val1 ^ state[0][0 :31]
                    state[0][32:63] = iota_val2 ^ state[0][32:63] 
        
    with LeafSection ("LS_11"): #converting 2-d array back to 200 length byte array
        for p in range(5):
            for q in range(5):
                reg[40*p + 8*q] = state[5*p + q][0:7]
                reg[40*p + 8*q + 1] = state[5*p + q][8:15]
                reg[40*p + 8*q + 2] = state[5*p + q][16:23]
                reg[40*p + 8*q + 3] = state[5*p + q][24:31]
                reg[40*p + 8*q + 4] = state[5*p + q][32:39]
                reg[40*p + 8*q + 5] = state[5*p + q][40:47]
                reg[40*p + 8*q + 6] = state[5*p + q][48:55]
                reg[40*p + 8*q + 7] = state[5*p + q][56:63]

    with ForLoopSection ("FLS_2", "r", 0, 200):
        with LeafSection ("LS_12"):
            for _r in range(200):
                if _r == r:
                    fout.write (reg[_r])

@hardware
def my_tb():
    m1 = keccakf1600 ("m1", [], [])
    with LeafSection ("S10"):
        m1.start ()
    with ParallelSections ("SP11"):
        with ForLoopSection ("TSRC", "l", 0, 200):
            with LeafSection ("SP11_0"):
                m1.m_["fin"].write (l)
                display ("my_tb : sending data %0d", l)
        with ForLoopSection ("TSINC", "m", 0, 200):
            with LeafSection ("SP11_1"):
                display ("#Result (%0d) = [%0d]", m, m1.m_["fout"].read ())

t = keccakf1600 ("", None, None)
t.emitVerilog (sys.stdout)
t.dumpDot (sys.stderr)
t = my_tb ("")
t.emitVerilog (sys.stdout)
