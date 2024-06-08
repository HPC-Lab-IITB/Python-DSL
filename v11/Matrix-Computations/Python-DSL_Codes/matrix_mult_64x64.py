from symbolic import *

@hardware
def matrix_mult (fA, fB, fC):
    ADDR_WIDTH = 12
    N = 64
    fA = InputFifo  ("fA", 32)
    fB = InputFifo  ("fB", 32)
    fC = OutputFifo ("fC", 32)
    A  = SimpleBRAM ("A", ADDR_WIDTH, 32)
    B  = SimpleBRAM ("B", ADDR_WIDTH, 32)
    C  = SimpleBRAM ("C", ADDR_WIDTH, 32)
    var_Res = Var("var_Res",32)
    with ParallelSections ("par_A_B"):
      with ForLoopSection ("R_A", "p", 0, N * N):
        with LeafSection ("recv_A"):
          A.writeData (p, fA.read ())
          display ("bram A: writing %0d at %0d", fA.read (), p)
      with ForLoopSection ("R_B", "q", 0, N * N):
        with LeafSection ("recv_B"):
          B.writeData (q, fB.read ())
          C.writeData (q, Const (32, 0))
          display ("bram B: writing %0d at %0d", fB.read (), q)
    with ForLoopSection ("R_k", "k", 0, N):
      with ForLoopSection ("R_i", "i", 0, N):
        with PipelinedSerialSectionLoop ("R_j", "j", 2, 0, N):
            with LeafSection ("S1"):
                A.readRequest (i * N + k)
                B.readRequest (k * N + j)
                C.readRequest (i * N + j)
            with LeafSection ("S2"):
                var_Res = A.readResp ()*B.readResp ()+C.readResp ()
                C.writeData (i * N + j, var_Res)
    with PipelinedSerialSectionLoop ("mDM2", "mm", 2, 0, N * N):
        with LeafSection ("read_c"):
            C.readRequest (mm)
            display ("mDM2 read_c : mm = %0d", mm)
        with LeafSection ("result_out"):
            fC.write (C.readResp ())

@hardware
def my_tb():
    N = 64
    m1 = matrix_mult ("m1", [], [], [])
    with LeafSection ("S10"):
      m1.start ()
    with ParallelSections ("SP11"):
      with ForLoopSection ("TSRC", "l", 0, N * N):
        with LeafSection ("SP11_0"):
          m1.m_["fA"].write (l)
          m1.m_["fB"].write (l)
          display ("my_tb : sending data %0d and %0d.", l, l)
      with ForLoopSection ("TSINC", "m", 0, N * N):
        with LeafSection ("SP11_1"):
          display ("#Result (%0d) = [%0d]", m, m1.m_["fC"].read ())

t = matrix_mult ("", None, None, None)
t.emitVerilog (sys.stdout)
#t.debugDumpSectionTree (sys.stderr)

t.dumpDot (sys.stderr)
t = my_tb ("")
t.emitVerilog (sys.stdout)
