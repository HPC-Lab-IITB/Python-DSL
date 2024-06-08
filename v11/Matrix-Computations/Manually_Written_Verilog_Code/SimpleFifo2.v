module Fifo (CLK, RST, write_enable, write_data, read_enable,
                       write_ready,  read_ready, read_data);
   parameter width = 8;

    input CLK, RST;
    input wire [0:0] write_enable;
    input wire [width-1:0] write_data;
    input wire [0:0] read_enable;
    output wire [0:0] write_ready;
    output wire [width-1:0] read_data;
    output wire [0:0] read_ready;

    FIFO2#(.width (width)) f1 (.CLK (CLK), .RST (~RST),
                 .D_IN (write_data),
                 .ENQ (write_enable),
                 .FULL_N (write_ready),
                 .D_OUT (read_data),
                 .DEQ (read_enable),
                 .EMPTY_N (read_ready),
                 .CLR (1'b0)
                );
    
endmodule

module InputFifo (CLK, RST, write_enable, write_data, read_enable,
                            write_ready,  read_ready, read_data);
   parameter width = 8;

    input CLK, RST;
    input wire [0:0] write_enable;
    input wire [width-1:0] write_data;
    input wire [0:0] read_enable;
    output wire [0:0] write_ready;
    output wire [width-1:0] read_data;
    output wire [0:0] read_ready;

    FIFO2#(.width (width)) f1 (.CLK (CLK), .RST (~RST),
                 .D_IN (write_data),
                 .ENQ (write_enable),
                 .FULL_N (write_ready),
                 .D_OUT (read_data),
                 .DEQ (read_enable),
                 .EMPTY_N (read_ready),
                 .CLR (1'b0)
                );
    
endmodule

module OutputFifo (CLK, RST, write_enable, write_data, read_enable,
                            write_ready,  read_ready, read_data);
   parameter width = 8;

    input CLK, RST;
    input wire [0:0] write_enable;
    input wire [width-1:0] write_data;
    input wire [0:0] read_enable;
    output wire [0:0] write_ready;
    output wire [width-1:0] read_data;
    output wire [0:0] read_ready;

    FIFO2#(.width (width)) f1 (.CLK (CLK), .RST (~RST),
                 .D_IN (write_data),
                 .ENQ (write_enable),
                 .FULL_N (write_ready),
                 .D_OUT (read_data),
                 .DEQ (read_enable),
                 .EMPTY_N (read_ready),
                 .CLR (1'b0)
                );
    
endmodule
