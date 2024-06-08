module mmul_gen(
  CLK, RST,
  START,
  Done,

  fA_write_ready,
  fA_write_enable,
  fA_write_data,
  
  fB_write_ready,
  fB_write_enable,
  fB_write_data,
  
  fC_read_ready,
  fC_read_enable,
  fC_read_data
);

  input wire CLK, RST;
  input  wire [0:0] START;
  output reg  [0:0] Done;

  output wire [0:0] fA_write_ready;
  input  wire [0:0] fA_write_enable;
  input  wire [31:0] fA_write_data;
  
  output wire [0:0] fB_write_ready;
  input  wire [0:0] fB_write_enable;
  input  wire [31:0] fB_write_data;
  
  output wire [0:0] fC_read_ready;
  input  wire [0:0] fC_read_enable;
  output wire [31:0] fC_read_data;

  
  parameter integer order = 64; // A_{64x64} * B_{64x64}
  parameter integer counter_width = 6;
  parameter integer BRAM_Size = 10,
  parameter integer address_counter_width = $clog2((order**2)+2);
  

  // Declare member instances :
  wire [0:0] fA_read_ready_wire;
  wire [31:0] fA_read_data_wire;
  reg  [0:0] fA_read_enable_wire;
  wire [0:0] fA_write_ready_wire;
  wire [0:0] fA_write_enable_wire;
  wire [31:0] fA_write_data_wire;
  InputFifo#(.width (32)) fA(
    .CLK (CLK), .RST (RST),
    .read_ready (fA_read_ready_wire),
    .read_data (fA_read_data_wire),
    .read_enable (fA_read_enable_wire),
    .write_ready (fA_write_ready_wire),
    .write_enable (fA_write_enable_wire),
    .write_data (fA_write_data_wire)
  );
  wire [0:0] fB_read_ready_wire;
  wire [31:0] fB_read_data_wire;
  reg  [0:0] fB_read_enable_wire;
  wire [0:0] fB_write_ready_wire;
  wire [0:0] fB_write_enable_wire;
  wire [31:0] fB_write_data_wire;
  InputFifo#(.width (32)) fB(
    .CLK (CLK), .RST (RST),
    .read_ready (fB_read_ready_wire),
    .read_data (fB_read_data_wire),
    .read_enable (fB_read_enable_wire),
    .write_ready (fB_write_ready_wire),
    .write_enable (fB_write_enable_wire),
    .write_data (fB_write_data_wire)
  );
  wire [0:0] fC_read_ready_wire;
  wire [31:0] fC_read_data_wire;
  wire [0:0] fC_read_enable_wire;
  wire [0:0] fC_write_ready_wire;
  reg  [0:0] fC_write_enable_wire;
  reg  [31:0] fC_write_data_wire;
  OutputFifo#(.width (32)) fC(
    .CLK (CLK), .RST (RST),
    .read_ready (fC_read_ready_wire),
    .read_data (fC_read_data_wire),
    .read_enable (fC_read_enable_wire),
    .write_ready (fC_write_ready_wire),
    .write_enable (fC_write_enable_wire),
    .write_data (fC_write_data_wire)
  );
  reg  [BRAM_Size-1:0] A_read_addr_wire;
  reg  [0:0] A_read_addr_valid_wire;
  wire [31:0] A_read_data_wire;
  reg  [0:0] A_write_enable_wire;
  reg  [11:0] A_write_addr_wire;
  reg  [31:0] A_write_data_wire;
  SimpleBRAM#(.addrwidth (12),.datawidth (32)) A(
    .CLK (CLK), .RST (RST),
    .read_addr (A_read_addr_wire),
    .read_addr_valid (A_read_addr_valid_wire),
    .read_data (A_read_data_wire),
    .write_enable (A_write_enable_wire),
    .write_addr (A_write_addr_wire),
    .write_data (A_write_data_wire)
  );
  reg  [BRAM_Size-1:0] B_read_addr_wire;
  reg  [0:0] B_read_addr_valid_wire;
  wire [31:0] B_read_data_wire;
  reg  [0:0] B_write_enable_wire;
  reg  [11:0] B_write_addr_wire;
  reg  [31:0] B_write_data_wire;
  SimpleBRAM#(.addrwidth (12),.datawidth (32)) B(
    .CLK (CLK), .RST (RST),
    .read_addr (B_read_addr_wire),
    .read_addr_valid (B_read_addr_valid_wire),
    .read_data (B_read_data_wire),
    .write_enable (B_write_enable_wire),
    .write_addr (B_write_addr_wire),
    .write_data (B_write_data_wire)
  );
  reg  [BRAM_Size-1:0] C_read_addr_wire;
  reg  [0:0] C_read_addr_valid_wire;
  wire [31:0] C_read_data_wire;
  reg  [0:0] C_write_enable_wire;
  reg  [11:0] C_write_addr_wire;
  reg  [31:0] C_write_data_wire;
  SimpleBRAM#(.addrwidth (12),.datawidth (32)) C(
    .CLK (CLK), .RST (RST),
    .read_addr (C_read_addr_wire),
    .read_addr_valid (C_read_addr_valid_wire),
    .read_data (C_read_data_wire),
    .write_enable (C_write_enable_wire),
    .write_addr (C_write_addr_wire),
    .write_data (C_write_data_wire)
  );

  reg [2:0] state;
  reg [address_counter_width-1:0] p = 0;
  reg [counter_width-1:0] k = 0;
  reg [counter_width-1:0] i = 0;
  reg [counter_width-1:0] j = 0;
  reg [address_counter_width-1:0] mm = 0;
  reg [BRAM_Size-1:0] temp_addr;
  reg stopijk;
  reg stopijk1;
  reg stopijk2;

  assign fA_write_ready = fA_write_ready_wire;
  assign fA_write_enable_wire = fA_write_enable;
  assign fA_write_data_wire = fA_write_data;
  assign fB_write_ready = fB_write_ready_wire;
  assign fB_write_enable_wire = fB_write_enable;
  assign fB_write_data_wire = fB_write_data;
  assign fC_read_ready = fC_read_ready_wire;
  assign fC_read_enable_wire = fC_read_enable;
  assign fC_read_data = fC_read_data_wire;
  
  
  always @(posedge CLK) begin
    if (RST) begin
      i <= 0;
      j <= 0;
      k <= 0;
		stopijk<=0;
		stopijk1<=0;
		stopijk2<=0;
		end
    else if (state == 2 && (!stopijk)) begin
      j <= j+1;
      if(j == (order-1)) begin
        i <= i + 1;
        j <= 0;
        if (i == order-1 ) begin
          k <= k+1;
          i <= 0;
          if (k == order-1) begin
            k <= 0;
            i <= 0;
            j <= 0;
		      stopijk <= 1;
          end
		  end
		end
    end
	 	stopijk1 <= stopijk;
		stopijk2 <= stopijk1;
  end
  
  always @ (*)
    begin
	 if (RST) begin
	    fA_read_enable_wire <= 0;
		 fB_read_enable_wire <= 0;
		 A_write_enable_wire <= 0;
		 B_write_enable_wire <= 0;
		 C_write_enable_wire <= 0;
		 A_read_addr_valid_wire <= 0;
		 B_read_addr_valid_wire <= 0;
		 C_read_addr_valid_wire <= 0;
		 fC_write_enable_wire <= 0;
	 end
		 
	   if(state==1) begin
		  if (p < ((order**2)-1) && p >= 0) begin
           if ((fA_read_ready_wire == 1'd1) && (fB_read_ready_wire == 1'd1)) begin
             fA_read_enable_wire <= 1'd1;
             A_write_enable_wire <= 1'd1;
				 
				 fB_read_enable_wire <= 1'd1;
             B_write_enable_wire <= 1'd1;
				 
				 C_write_enable_wire <= 1'd1;
			   end
			end
		end
		
		if(state==2) begin
		  if(stopijk2!=1) begin
		    C_write_enable_wire <= 1'd1;
			 A_read_addr_valid_wire <= 1'd1;
			 B_read_addr_valid_wire <= 1'd1;
			 C_read_addr_valid_wire <= 1'd1;
		  end
		end
		
		if(state == 3) begin
		  if (mm < (order**2)) begin
			 if ((1'd1 == fC_write_ready_wire)) begin
		      C_read_addr_valid_wire <= 1'd1;
				fC_write_enable_wire <= 1'd1;
		    end
		  end
		 end
	end
  
  always @ (posedge CLK) begin
    if (RST) begin
      state <= 0;
      Done <= 0;
		p <= 0;
		mm <= 0;
		temp_addr <= 0;
		fC_write_data_wire <= 0;
		A_read_addr_wire <= 0;
      A_write_addr_wire <= 0;
      A_write_data_wire <= 0;
		B_read_addr_wire <= 0;
      B_write_addr_wire <= 0;
      B_write_data_wire <= 0;
		C_read_addr_wire <= 0;
      C_write_addr_wire <= 0;
      C_write_data_wire <= 0;
    end 
	 else begin
      case(state)
        0: begin // IDLE
          if (START) begin
            state <= 1;
          end
        end
        1: begin // FETCH_A and FETCH_B and Intialize C
          if (p < (order**2) && p >= 0) begin
           if ((fA_read_ready_wire == 1'd1) && (fB_read_ready_wire == 1'd1)) begin
            A_write_addr_wire <= p;
            A_write_data_wire <= fA_read_data_wire;
            B_write_addr_wire <= p;
            B_write_data_wire <= fB_read_data_wire;
            C_write_addr_wire <= p;
            C_write_data_wire <= 32'd0;
            p <= (p + 1);
           end
			  else begin
			   state <= 1;
			  end
			 end
			 else begin
			  state <= 2;
			 end
			end
        2: begin // Compute
		     if(stopijk2 == 1) begin
			  state <= 3;
			  end
			  else begin
			   if (!stopijk &&(i==0 && j==0 && k==0) )begin 
	           A_read_addr_wire <= (i * order) + k;
              B_read_addr_wire <= (k * order) + j;
              C_read_addr_wire <= (i * order) + j;
			     temp_addr <= C_read_addr_wire;
             end
				else begin
		      A_read_addr_wire <= (i * order) + k;
            B_read_addr_wire <= (k * order) + j;
            C_read_addr_wire <= (i * order) + j;
				temp_addr <= C_read_addr_wire;
				C_write_data_wire <= (A_read_data_wire*B_read_data_wire) + C_read_data_wire;
			   C_write_addr_wire <= temp_addr;
			 end
			end	
        end
        3: begin // UPDATE in FIFO C
		      if (mm < ((order**2)+2)) begin
				 if ((1'd1 == fC_write_ready_wire)) begin
				  C_read_addr_wire <= (mm);
				  fC_write_data_wire <= C_read_data_wire;
				  mm <= mm + 1;
				 end
				end
				 else begin
				 state <= 0;
				 Done <= 1;
				 end
        	  end
			default : state <= 0;
      endcase
    end
  end

endmodule
