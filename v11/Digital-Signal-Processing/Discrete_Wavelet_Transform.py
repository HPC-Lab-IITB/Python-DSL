#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 11:04:05 2024

@author: manikanta
"""

from symbolic import *

@hardware
def dwt(fin, fout):
    ADDR_WIDTH = 4
    INDEX = 2
    
    # Input and output FIFOs
    fin = InputFifo("fin", 32)
    fout = OutputFifo("fout",32)
    
    # Declaring BRAMS
    ram_in = SimpleBRAM("ram_in", ADDR_WIDTH, 32)
    ram_out = SimpleBRAM("ram_out", ADDR_WIDTH, 32)
    ram_row = SimpleBRAM("ram_row", ADDR_WIDTH, 32)
    ram_col = SimpleBRAM("ram_col", ADDR_WIDTH, 32)
    
    # Declaring Registers
    tmp1 = Reg("tmp1", 32)
    tmp2 = Reg("tmp2", 32)
    tmp3 = Reg("tmp3", 32)
    tmp4 = Reg("tmp4", 32)
    tmp5 = Reg("tmp5", 32)
    tmp6 = Reg("tmp6", 32)
    tmp7 = Reg("tmp7", 32)
    tmp8 = Reg("tmp8", 32)
    
    #Functional Logicwith SerialSections("full_serial"):
    with ForLoopSection("input_read", "i", 0, 16):
        with LeafSection("recv_input"):
            ram_in.writeData(i, fin.read())
            display("ram_in: writing %0d at %0d", fin.read(), i)
            
    # Row Processing Block
    with ForLoopSection("row_processing","j",0,8):
        with SerialSections("S1"):
            with LeafSection("First_row_pixel"):
                ram_in.readRequest(j * INDEX)
            with LeafSection("First_row_pixel_resp"):
                tmp1 = ram_in.readResp()
            with LeafSection("Second_row_pixel"):
                ram_in.readRequest(j * INDEX+1)
            with LeafSection("Second_row_pixel_resp"):
                tmp2 = ram_in.readResp()
            with LeafSection("Add_Sub_row"):
                tmp3 = (tmp1 >> 1) + (tmp2 >> 1) 
                if(tmp1 > tmp2):
                    tmp4 = (tmp1 >> 1) - (tmp2 >> 1)
                else:
                    tmp4 = (tmp2 >> 1) - (tmp1 >> 1)
            with LeafSection("Updating_row_BRAMs1"):
                ram_row.writeData(j * INDEX, tmp3)
            with LeafSection("Updating_row_BRAMs2"):
                ram_row.writeData(j * INDEX+1, tmp4)
                
    with ForLoopSection("column_processing","k",0,8):
        with SerialSections("S2"):
            with LeafSection("First_column_pixel"):
                ram_row.readRequest(k)
            with LeafSection("First_column_pixel_resp"):
                tmp5 = ram_row.readResp()
            with LeafSection("Second_column_pixel"):
                ram_row.readRequest(k+8)
            with LeafSection("Second_column_pixel_resp"):
                tmp6 = ram_row.readResp()
            with LeafSection("Add_Sub_column"):
                tmp7 = (tmp5 >> 1) + (tmp6 >> 1) 
                if(tmp5 > tmp6):
                    tmp8 = (tmp5 >> 1) - (tmp6 >> 1)
                else:
                    tmp8 = (tmp6 >> 1) - (tmp5 >> 1)
            with LeafSection("Updating_column_BRAMs1"):
                ram_col.writeData(k, tmp7)
            with LeafSection("Updating_column_BRAMs2"):
                ram_col.writeData(k+8, tmp8)
                fout.write(tmp7)
            with LeafSection("FIFO_write1"):
                fout.write(tmp8)    
@hardware
def my_tb():
    N = 16 
    m1 = dwt("m1", [], [] )
    with LeafSection ("S10"):
      m1.start ()
    with ParallelSections ("SP11"):
      with ForLoopSection ("TSRC", "l", 0, N ):
        with LeafSection ("SP11_0"):
          m1.m_["fin"].write (l)
          display ("my_tb : sending data %0d.", l)
      with ForLoopSection ("TSINC", "m", 0, N ):
        with LeafSection ("SP11_1"):
            display ("#Result (%0d) = [%0d]", m, m1.m_["fout"].read ())

t = dwt("", None, None)
t.emitVerilog (sys.stdout)
t.dumpDot (sys.stderr)
t = my_tb ("")
t.emitVerilog (sys.stdout)
        
                
