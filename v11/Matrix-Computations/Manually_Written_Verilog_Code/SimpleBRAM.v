module SimpleBRAM (
  CLK, RST,
  read_addr,
  read_addr_valid,
  read_data,
  write_enable,
  write_addr,
  write_data
);

  parameter datawidth=32;
  parameter addrwidth=8;

  input wire CLK, RST;
  input  wire [(addrwidth-1):0] read_addr;
  input  wire                   read_addr_valid;
  // output reg  [(datawidth-1):0] read_data;
  output wire [(datawidth-1):0] read_data;
         reg  [(addrwidth-1):0] read_addr_reg;
  input  wire [0:0] write_enable;
  input  wire [(addrwidth-1):0] write_addr;
  input  wire [(datawidth-1):0] write_data;

  //(* nomem2reg *) 
  reg [datawidth-1:0] ram[2**addrwidth-1:0];

  always @(posedge CLK) begin
    if (1'b1 == write_enable) begin
      ram[write_addr] <= write_data;
    end
    if (read_addr_valid) begin
      read_addr_reg <= read_addr;
    end
  end
  assign read_data = ram[read_addr_reg];

endmodule
