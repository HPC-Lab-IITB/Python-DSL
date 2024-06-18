#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 13:24:25 2024

@author: manikanta
"""

from symbolic import *

bit_reversal_rom = [0,4,2,6,1,5,3,7]
w_real = [65536, 46340, 0, 46340]
w_imag = [0, 46340, 4294901760, 46340]

@hardware
def fft256_final(fin1, fin2, fin3, fin4, fin5, fout1, fout2):
    OFFSET = 4
    ADDR_WIDTH = 8
    FFT_PTS = 256
    
    # Input and output FIFOs
    fin1 = InputFifo ("fin1", 32)
    fin2 = InputFifo ("fin2", 32)
    fin3 = InputFifo ("fin3", 32)
    fin4 = InputFifo ("fin4", 32)
    fin5 = InputFifo ("fin5", 32)
    fout1 = OutputFifo ("fout1", 32)
    fout2 = OutputFifo ("fout2", 32)
    
    # BRAMS
    bin1 = SimpleBRAM ("bin1", ADDR_WIDTH, 32)
    bin2 = SimpleBRAM ("bin2", ADDR_WIDTH, 32)
    bin3 = SimpleBRAM ("bin3", ADDR_WIDTH, 32)
    bin4 = SimpleBRAM ("bin4", ADDR_WIDTH, 32)
    bin5 = SimpleBRAM ("bin5", ADDR_WIDTH, 32)
    
    # Auxiliary BRAMS
    bitrev_real = SimpleBRAM ("bitrev_real", ADDR_WIDTH+OFFSET, 32)
    bitrev_imag = SimpleBRAM ("bitrev_imag", ADDR_WIDTH+OFFSET, 32)
    
    # Necessary Registers
    tmp1 = Reg ("tmp1", 32)
    tmp2 = Reg ("tmp2", 32)
    tmp3 = Reg ("tmp3", 32)
    tmp4 = Reg ("tmp4", 32)
    tmp5 = Reg ("tmp5", 32)
    tmp6 = Reg ("tmp6", 32)
    tmp7 = Reg ("tmp7", 32)
    tmp8 = Reg ("tmp8", 32)
    tmp9 = Reg ("tmp9", 32)
    
    out1 = Reg ("out1", 32)
    out2 = Reg ("out2", 32)
    out3 = Reg ("out3", 32)
    out4 = Reg ("out4", 32)
    
    count1 = Reg ("count1", 32)
    count2 = Reg ("count2", 32)
    numpts = Reg ("numpts", 32)
    symbo1 = Reg ("symbo1", 32)
    
    out1_var = Var ("out1_var", 32)
    out2_var = Var ("out2_var", 32)
    out3_var = Var ("out3_var", 32)
    out4_var = Var ("out4_var", 32)
    
    butterfly_span = Reg ("butterfly_span", 32)
    butterfly_pass = Reg ("butterfly_pass", 32)
    
    # Necessary Registers
    indexshift  = Reg ("indexshift", 32)
    passshift   = Reg ("passshift", 32)
    passcheck   = Reg ("passcheck", 32)
    fftstage    = Reg ("fftstage", 32)
    index       = Reg ("index", 32)
    Ulimit      = Reg ("Ulimit", 32)
    Llimit      = Reg ("Llimit", 32)
    productreal = Reg ("productreal", 32)
    productimag = Reg ("productimag", 32)
    
    productreal_var = Var ("productreal_var", 32)
    productimag_var = Var ("productimag_var", 32)
    
    index_var       = Var ("index_var", 32)
    Ulimit_var      = Var ("Ulimit_var", 32)
    Llimit_var      = Var ("Llimit_var", 32)
    
    # Reading inputs from FIFO to BRAM
    with ParallelSections ("par_fifo_read"):
      with ForLoopSection ("R_in1", "p", 0, FFT_PTS):
        with LeafSection ("recv_in1"):
          bin1.writeData (p, fin1.read ())
          display ("bram bin1: writing %0d at %0d", fin1.read (), p)
      with ForLoopSection ("R_in2", "q", 0, FFT_PTS):
        with LeafSection ("recv_in2"):
          bin2.writeData (q, fin2.read ())
          display ("bram bin2: writing %0d at %0d", fin2.read (), q)
      with ForLoopSection ("R_in3", "r", 0, FFT_PTS):
        with LeafSection ("recv_in3"):
          bin3.writeData (r, fin3.read ())
          display ("bram bin3: writing %0d at %0d", fin3.read (), r)
      with ForLoopSection ("R_in4", "s", 0, FFT_PTS):
        with LeafSection ("recv_in4"):
          bin4.writeData (s, fin4.read ())
          display ("bram bin4: writing %0d at %0d", fin4.read (), s)
      with ForLoopSection ("R_in5", "t", 0, FFT_PTS):
        with LeafSection ("recv_in5"):
          bin5.writeData (t, fin5.read ())
          display ("bram bin5: writing %0d at %0d", fin5.read (), s)
      with LeafSection("counts_init"):
          Assignment (count1, Const (32, 0))
          Assignment (count2, Const (32, 0))
          Assignment (numpts, Const (32, FFT_PTS))
          Assignment (symbo1, Const (32, 1))
         
    # Bit Reversal Stage
    with ForLoopSection ("ser_f1", "a", 0, FFT_PTS):
        with SerialSections ("bit_serial"):
            with LeafSection("Access_bit_reversal_ROM1"):
                bin5.readRequest(a)
            with LeafSection("Access_bit_reversal_ROM2"):
                tmp1 = bin5.readResp()
            with LeafSection("Access_inputs1"):
                bin1.readRequest(tmp1)
                bin2.readRequest(tmp1)
            with LeafSection("Access_inputs2"):
                tmp2 = bin1.readResp()
                tmp3 = bin2.readResp()
            with LeafSection("writing_bit_reversal"):
                bitrev_real.writeData (a, tmp2)
                bitrev_imag.writeData (a, tmp3)
            
    # FFT Functional logic stage
    
    # FFT stages 
    with SerialSections ("fft_top"):
        with ForLoopSection ("fft_num_stage","j", 0, ADDR_WIDTH):
            with SerialSections ("FFT_stages"):
                with LeafSection("count1_update"):
                    Assignment (count1, count1 + Const (32, 1))
                # FFT stage j
                with LeafSection("const1"):
                    Assignment (indexshift, Const(32, ADDR_WIDTH-1-j))
                    Assignment (passshift , Const(32, j+1))
                    Assignment (passcheck , Const(32, numpts >> count1))
                    Assignment (fftstage  , Const(32, symbo1 << count2))
    
                with LeafSection("count2_update"):
                    Assignment (count2, count2 + Const (32, 1))
                    
                with LeafSection("Reset1"):
                    Assignment (butterfly_span, Const(32, 0))
                    Assignment (butterfly_pass, Const(32, 0))
                    
                with ForLoopSection ("fft_loop1","i", 0, FFT_PTS >> 1):
                    with SerialSections ("fft1_serial"):
                        with LeafSection("Precomputations"):
                            index_var = butterfly_span << indexshift
                            Ulimit_var = butterfly_span + (butterfly_pass << passshift)
                            Llimit_var = Ulimit_var + fftstage
                            
                            index = index_var
                            Ulimit = Ulimit_var
                            Llimit = Llimit_var
                            
                            bin3.readRequest(index_var)
                            bin4.readRequest(index_var)
                            bitrev_real.readRequest(j*FFT_PTS+Llimit_var)
                            bitrev_imag.readRequest(j*FFT_PTS+Llimit_var)
                            
                        with LeafSection("Access_reqd_elements1_Resp"):
                            tmp4 = bin3.readResp()
                            tmp5 = bin4.readResp()
                            tmp6 = bitrev_real.readResp()
                            tmp7 = bitrev_imag.readResp()
                            
                        with LeafSection("Compute1"):
                            productreal_var = (tmp4 * tmp6) - (tmp5 * tmp7)
                            productimag_var = (tmp4 * tmp7) + (tmp5 * tmp6)
                            
                            productreal = productreal_var
                            productimag = productimag_var
                        
                        with LeafSection("Access_reqd_elements2"):
                            bitrev_real.readRequest(j*FFT_PTS+Ulimit)
                            bitrev_imag.readRequest(j*FFT_PTS+Ulimit)
                            
                        with LeafSection("Access_reqd_elements2_Resp"):
                            tmp8 = bitrev_real.readResp()
                            tmp9 = bitrev_imag.readResp()
                            
                        with LeafSection("Post_computations"):
                            out1_var = tmp8 - productreal
                            out2_var = tmp9 - productimag
                            out3_var = tmp8 + productreal
                            out4_var = tmp9 + productimag
                            
                            out1 = out1_var
                            out2 = out2_var
                            out3 = out3_var
                            out4 = out4_var
                            
                        with LeafSection("Storing_fft1outputs1"):
                            bitrev_real.writeData ((j+1)*FFT_PTS+Llimit, out1)
                            bitrev_imag.writeData ((j+1)*FFT_PTS+Llimit, out2)
                            
                        with LeafSection("Storing_fft1outputs2"):
                            bitrev_real.writeData ((j+1)*FFT_PTS+Ulimit, out3)
                            bitrev_imag.writeData ((j+1)*FFT_PTS+Ulimit, out4)
                            
                        with LeafSection("Control1"):
                            if (butterfly_span < (fftstage-1)):
                                Assignment(butterfly_span, butterfly_span + Const(32,1))
                            elif (butterfly_pass < passcheck-1):
                                Assignment(butterfly_span, Const(32,0))
                                Assignment(butterfly_pass, butterfly_pass + Const(32,1))
                            else:
                                Assignment(butterfly_span, Const(32,0))
                                Assignment(butterfly_pass, Const(32,0))
            
        with ForLoopSection("output_read","b", 0, FFT_PTS):
            with LeafSection("real_read_request"):
                bitrev_real.readRequest(b+(ADDR_WIDTH)*FFT_PTS)
                bitrev_imag.readRequest(b+(ADDR_WIDTH)*FFT_PTS)
            with LeafSection("real_read_resp"):
                fout1.write(bitrev_real.readResp())
                fout2.write(bitrev_imag.readResp())
                
@hardware
def my_tb():
    m1 = fft256_final ("m1", [], [], [], [], [], [], [])
    with LeafSection ("S10"):
        m1.start ()
    with ParallelSections ("SP11"):
        with ForLoopSection ("TSRC", "l", 0, 256):
            with LeafSection ("SP11_0"):
                m1.m_["fin1"].write (l)
                m1.m_["fin2"].write (0)
                m1.m_["fin3"].write (1)
                m1.m_["fin4"].write (0)
                m1.m_["fin5"].write (l)
                display ("my_tb : sending data %0d and %0d.", l, 0)

    with ForLoopSection ("TSINC", "m", 0, 256):
        with LeafSection ("SP11_1"):
          display ("#Result real (%0d) = [%0d]", m, m1.m_["fout1"].read ())
          display ("#Result imag (%0d) = [%0d]", m, m1.m_["fout2"].read ())

t = fft256_final ("", None, None, None, None, None, None, None)
t.emitVerilog (sys.stdout)
t.dumpDot (sys.stderr)
t = my_tb ("")
t.emitVerilog (sys.stdout)
        
            
            
        