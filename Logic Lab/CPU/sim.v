`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 08.06.2020 15:27:06
// Design Name: 
// Module Name: register8_sim
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module register8_sim();

    reg [7:0] inp;
    wire [7:0] out;
    reg wrt;
    reg clk;
    reg e;
    reg reset;
    
    reg8 register(wrt, inp, clk, reset, e, out);
    
    always #10 clk = ~clk;
    
    initial begin
        clk = 0;
        reset = 1;
        wrt = 1;
        e = 1;
        #1 reset = 0;
        inp = 12;
        #49 inp = 4;
        #30 wrt = 0;
        #1 wrt = 1;
        inp = 5;
        #40
        reset = 1;
        inp = 8;
    end

endmodule

module mux_sim();
    reg [2:0] sel;
    reg [7:0] d0, d1, d2, d3, d4, d5, d6, d7;
    wire [7:0] out;
    
    mux8_1 mux(sel, d0, d1, d2, d3, d4, d5, d6, d7, out);
    
    initial begin
        
        d0 = 0;
        d1 = 2;
        d4 = 3;
        d5 = 4;
        d6 = 5;
        d7 = 6;
        d2 = 7;
        d3 = 4;
        sel = 2;
    end

endmodule

module decoder_sim();
    reg [2:0] sel;
    wire [7:0] out;
    reg e;
    
    
    decoder3_8 decd(e, sel, out);
    
    initial begin
        sel = 2;
        e = 1;
    end

endmodule


module regfile_sim();
    reg [2:0] dst;
    reg ld;
    reg clk;
    reg rst;
    reg [7:0] dataIn;
    wire [7:0] regOut_0;
    wire [7:0] regOut_1;
    wire [7:0] regOut_2;
    wire [7:0] regOut_3;
    wire [7:0] regOut_4;
    wire [7:0] regOut_5;
    wire [7:0] regOut_6;
    
    always #10 clk = ~clk;
    
    register_file regfile(dst, ld, clk, rst, dataIn, 
        regOut_0, regOut_1, regOut_2, regOut_3, regOut_4, regOut_5, regOut_6);
    
    initial begin
        clk = 0;
        rst = 1;
        ld = 1;
        dst = 0;
        #1 rst = 0;
        dataIn = 4;
        #39 dst = 2;
        dataIn = 7; 
        
    end
    
endmodule


module ins_decoder_sim();
    reg [20:0] instruction;
    wire z;
    wire [2:0] op;
    wire [7:0] im;
    wire [2:0] src1;
    wire [2:0] src2;
    wire [2:0] dst;
    
    ins_decoder _ins_decoder(instruction, z, op, im, src1, src2, dst);
    
    initial begin
        
        instruction = 21'b101100001100101111101;
    
    end

endmodule


module cpu_sim();
    reg [20:0] instruction;
    reg clk, rst;
    
    CPU _cpu(instruction, clk, rst);
    
    always #10 clk = ~clk;
    
    initial begin
        clk = 0;
        rst = 1;
        #1 rst = 0;
        
        instruction <= {1'b0, 3'd3, 8'd45, 3'b111, 3'b000, 3'b000}; #9;
        instruction <= {1'b0, 3'd3, 8'd12, 3'b111, 3'b000, 3'b001}; #20;
        instruction <= {1'b0, 3'd0, 8'd0, 3'b000, 3'b001, 3'b010}; #20;
        instruction <= {1'b0, 3'd3, 8'd30, 3'b111, 3'b000, 3'b000}; #20;
        instruction <= {1'b0, 3'd1, 8'd0, 3'b010, 3'b000, 3'b001}; #20;
    
    end

endmodule
