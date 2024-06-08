module my_tb (
  CLK, RST,
  START,
  Done,
);
  // Declare port widths and directions :
  output reg CLK, RST;
  output reg  [0:0] START;
  output reg [0:0] Done;
  parameter ordertb = 64;
  parameter integer address_counter_width_tb = $clog2((ordertb**2)+2);
 
  // Declare member instances :
  reg  [0:0] m1_START_wire;
  wire [0:0] m1_Done_wire;

  wire [0:0] m1_fA_write_ready_wire;
  reg  [0:0] m1_fA_write_enable_wire;
  reg  [31:0] m1_fA_write_data_wire;
  wire [0:0] m1_fB_write_ready_wire;
  reg  [0:0] m1_fB_write_enable_wire;
  reg  [31:0] m1_fB_write_data_wire;
  wire [0:0] m1_fC_read_ready_wire;
  reg  [0:0] m1_fC_read_enable_wire;
  wire [31:0] m1_fC_read_data_wire;
  mmul_gen m1(
    .CLK (CLK), .RST (RST),
    .START (m1_START_wire),
    .Done (m1_Done_wire),
    .fA_write_ready (m1_fA_write_ready_wire),
    .fA_write_enable (m1_fA_write_enable_wire),
    .fA_write_data (m1_fA_write_data_wire),
    .fB_write_ready (m1_fB_write_ready_wire),
    .fB_write_enable (m1_fB_write_enable_wire),
    .fB_write_data (m1_fB_write_data_wire),
    .fC_read_ready (m1_fC_read_ready_wire),
    .fC_read_enable (m1_fC_read_enable_wire),
    .fC_read_data (m1_fC_read_data_wire)
  );
  
  // Attach wires between member-instance-ports and self ports:
  // Declare variables:
  // Declare registers (and driver wires):
  reg [1:0] state_st = 2'd0;
  reg [1:0] state_st_WIRE;
  reg [0:0] Done_outreg = 1'd0;
  reg [0:0] Done_outreg_WIRE;
  reg [1:0] state_S10 = 2'd0;
  reg [1:0] state_S10_WIRE;
  reg [address_counter_width_tb-1:0] l = 0;
  reg [address_counter_width_tb-1:0] l_WIRE;
  reg [1:0] state_for_TSRC_CONDITION_section = 2'd0;
  reg [1:0] state_for_TSRC_CONDITION_section_WIRE;
  reg [1:0] state_SP11_0 = 2'd0;
  reg [1:0] state_SP11_0_WIRE;
  reg [address_counter_width_tb-1:0] m = 0;
  reg [address_counter_width_tb-1:0] m_WIRE;
  reg [1:0] state_for_TSINC_CONDITION_section = 2'd0;
  reg [1:0] state_for_TSINC_CONDITION_section_WIRE;
  reg [1:0] state_SP11_1 = 2'd0;
  reg [1:0] state_SP11_1_WIRE;
  reg [1:0] state_SP11_parallel_merge = 2'd0;
  reg [1:0] state_SP11_parallel_merge_WIRE;
  //assign m1_fA_write_ready_wire = 1;
  //assign m1_fB_write_ready_wire = 1;
  //assign m1_fC_read_ready_wire = 1;
  always #1 CLK = ~CLK;
  initial begin
    CLK = 1'b0;
    RST = 1'b0; // Set RST initially to 1
	 START = 1'b0;
    #50; // Wait for 10 time units
    RST = 1'b1; // Deassert RST to start the simulation
    #30; // Wait for additional time
	 RST = 1'b0;
	 #10;
	 START = 1'b1;
	 #10;
	 START = 1'b0;
  end
  always @(posedge CLK) begin
    if (1'b1 == RST) begin
      state_st <= 2'd0;
      Done_outreg <= 1'd0;
      state_S10 <= 2'd0;
      l <= 0;
      state_for_TSRC_CONDITION_section <= 2'd0;
      state_SP11_0 <= 2'd0;
      m <= 0;
      state_for_TSINC_CONDITION_section <= 2'd0;
      state_SP11_1 <= 2'd0;
      state_SP11_parallel_merge <= 2'd0;
    end
    else begin
      state_st <= state_st_WIRE;
      Done_outreg <= Done_outreg_WIRE;
      state_S10 <= state_S10_WIRE;
      l <= l_WIRE;
      state_for_TSRC_CONDITION_section <= state_for_TSRC_CONDITION_section_WIRE;
      state_SP11_0 <= state_SP11_0_WIRE;
      m <= m_WIRE;
      state_for_TSINC_CONDITION_section <= state_for_TSINC_CONDITION_section_WIRE;
      state_SP11_1 <= state_SP11_1_WIRE;
      state_SP11_parallel_merge <= state_SP11_parallel_merge_WIRE;
    end
  end
  always @(*) begin
    // Default values for variables (to avoid latches):
    // Default values for member-instance input ports:
    m1_START_wire = 1'd0;
    m1_fA_write_enable_wire = 0;
    m1_fA_write_data_wire = 0;
    m1_fB_write_enable_wire = 0;
    m1_fB_write_data_wire = 0;
    m1_fC_read_enable_wire = 0;
	 
    state_st_WIRE = state_st;
    Done_outreg_WIRE = Done_outreg;
    state_S10_WIRE = state_S10;
    l_WIRE = l;
    state_for_TSRC_CONDITION_section_WIRE = state_for_TSRC_CONDITION_section;
    state_SP11_0_WIRE = state_SP11_0;
    m_WIRE = m;
    state_for_TSINC_CONDITION_section_WIRE = state_for_TSINC_CONDITION_section;
    state_SP11_1_WIRE = state_SP11_1;
    state_SP11_parallel_merge_WIRE = state_SP11_parallel_merge;
    // Default values for output ports: 2
    Done = 1'd0;
    if ((state_st != 2'b1) && (START == 1'b1)) begin
      state_st_WIRE = 2'b1;
      state_S10_WIRE = 1;
    end
    Done = Done_outreg;
    // body: S10:
    if (state_S10 == 1) begin
        m1_START_wire = 1'd1;
        state_S10_WIRE = 2;
        state_for_TSRC_CONDITION_section_WIRE = 1;
        state_for_TSINC_CONDITION_section_WIRE = 1;
        state_SP11_parallel_merge_WIRE = 1;
    end
    if (state_for_TSRC_CONDITION_section == 1) begin
      if ((ordertb**2 > l)) begin
        if ((1'd1 == m1_fA_write_ready_wire) && (1'd1 == m1_fB_write_ready_wire)) begin
          m1_fA_write_data_wire = l;
          m1_fA_write_enable_wire = 1'd1;
          m1_fB_write_data_wire = l;
          m1_fB_write_enable_wire = 1'd1;
          l_WIRE = (l + 1); //
        state_for_TSRC_CONDITION_section_WIRE = 2;
          state_for_TSRC_CONDITION_section_WIRE = 1;
        end
      end
      else begin
        l_WIRE = 0; //
        state_for_TSRC_CONDITION_section_WIRE = 2;
      end
    end
    if (state_for_TSINC_CONDITION_section == 1) begin
      if ((ordertb**2)+2 > m) begin
        if ((1'd1 == m1_fC_read_ready_wire)) begin
          m1_fC_read_enable_wire = 1'd1;
          m_WIRE = (m + 1);
        state_for_TSINC_CONDITION_section_WIRE = 2;
          state_for_TSINC_CONDITION_section_WIRE = 1;
        end
      end
      else begin
        m_WIRE = 0;
        state_for_TSINC_CONDITION_section_WIRE = 2;
      end
    end
    // body: SP11_parallel_merge:
    if (state_SP11_parallel_merge == 1) begin
      if ((2'd2 == state_for_TSRC_CONDITION_section) && (2'd2 == state_for_TSINC_CONDITION_section)) begin
        state_SP11_parallel_merge_WIRE = 2;
        state_st_WIRE = 2; //#
        Done_outreg_WIRE = 1;
      end
    end
  end
endmodule