from symbolic import *

@hardware
def matrix_mult (fA, fB, fC):
    ADDR_WIDTH = 10
    N = 3
    fA = InputFifo  ("fA", 32)
    fB = InputFifo  ("fB", 32)
    fC = OutputFifo ("fC", 32)
    A  = SimpleBRAM ("A", ADDR_WIDTH, 32)
    B  = SimpleBRAM ("B", ADDR_WIDTH, 32)
    C  = SimpleBRAM ("C", ADDR_WIDTH, 32)
    fma = scalar_fma ("fma")
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
    with ParallelSections ("multiply"):
      with ForLoopSection ("R_k", "k", 0, N):
        with ForLoopSection ("R_i", "i", 0, N):
          with PipelinedSerialSectionLoop ("R_j", "j", 2, 0, N):
              with LeafSection ("S1"):
                  A.readRequest (i * N + k)
                  B.readRequest (k * N + j)
                  C.readRequest (i * N + j)
                  display ("j=%0d bram: sending read requests for A[%0d], B[%0d], C[%0d]", j, i * N + k, k * N + j, i * N + j)
              with LeafSection ("S2"):
                  fma.enqOperands (A.readResp (), B.readResp (), C.readResp ())
                  display ("j=%0d fma: operands : %0d, %0d, %0d", j, A.readResp (), B.readResp (), C.readResp ())
      with ForLoopSection ("R_k_", "k_", 0, N):
        with ForLoopSection ("R_i_", "i_", 0, N):
          with ForLoopSection ("R_j_", "j_", 0, N):
            with LeafSection ("update_C"):
              C.writeData (i_ * N + j_, fma.getResult ())
              display ("bram: writing %0d at C[%0d]", fma.getResult (), i_ * N + j_)
              display ("fma: result %0d", fma.getResult ())
    with PipelinedSerialSectionLoop ("mDM2", "mm", 2, 0, N * N):
        with LeafSection ("read_c"):
            C.readRequest (mm)
            display ("mDM2 read_c : mm = %0d", mm)
        with LeafSection ("result_out"):
            fC.write (C.readResp ())

@hardware
def my_tb():
    N = 3
    m1 = matrix_mult ("m1", [], [], [])
    with LeafSection ("S10"):
      m1.start ()
    with ParallelSections ("SP11"):
      with ForLoopSection ("TSRC", "l", 0, N * N):
        with LeafSection ("SP11_0"):
          m1.m_["fA"].write (l)
          m1.m_["fB"].write (l * 2)
          display ("my_tb : sending data %0d and %0d.", l, l * 2)
      with ForLoopSection ("TSINC", "m", 0, N * N):
        with LeafSection ("SP11_1"):
          display ("#Result (%0d) = [%0d]", m, m1.m_["fC"].read ())

t = matrix_mult ("", None, None, None)
t.emitVerilog (sys.stdout)
#t.debugDumpSectionTree (sys.stderr)
t.dumpDot (sys.stderr)
t = my_tb ("")
t.emitVerilog (sys.stdout)

# For simulating yosys-synthesized modules, replace
#   \$paramod\SimpleBRAM\datawidth=32\addrwidth=10 instances
#   with SimpleBRAM#(.datawidth(32),.addrwidth(10)) instances,
#   and add SimpleBRAM.v to iverilog list of files.
