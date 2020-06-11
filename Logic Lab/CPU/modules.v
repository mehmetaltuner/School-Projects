`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 08.06.2020 14:25:59
// Design Name: 
// Module Name: project
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


module decoder3_8(
    input en,
    input wire [2:0] bits,
    output wire [7:0] out
);

    
    assign out[0] = ~bits[0] & ~bits[1] & ~bits[2] & en;
    assign out[1] = bits[0] & ~bits[1] & ~bits[2] & en;
    assign out[2] = ~bits[0] & bits[1] & ~bits[2] & en;
    assign out[3] = bits[0] & bits[1] & ~bits[2] & en;
    assign out[4] = ~bits[0] & ~bits[1] & bits[2] & en;
    assign out[5] = bits[0] & ~bits[1] & bits[2] & en;
    assign out[6] = ~bits[0] & bits[1] & bits[2] & en;
    assign out[7] = bits[0] & bits[1] & bits[2] & en;

    
endmodule

module mux8_1(
    input wire [2:0] sel,
    input wire [7:0] d0, d1, d2, d3, d4, d5, d6, d7,
    output reg [7:0] out
);
    
    always @ (*) begin
       case (sel)
           0 : out = d0;
           1 : out = d1;
           2 : out = d2;
           3 : out = d3;
           4 : out = d4;
           5 : out = d5;
           6 : out = d6;
           7 : out = d7;
           default : out = 1'b0;
       endcase
    end
    
endmodule


module reg8(
    input wrt,
    input [7:0] rin,
    input clk,
    input reset,
    input e,
    output reg [7:0] rout
);

    always @ (posedge clk or negedge reset) begin
        if(wrt & !reset & e) begin
            rout = rin;
        end
    end

endmodule

module register_file(
    input wire [2:0] dst,
    input wire ld,
    input clk,
    input rst,
    input [7:0] dataIn,
    output [7:0] regOut_0,
    output [7:0] regOut_1,
    output [7:0] regOut_2,
    output [7:0] regOut_3,
    output [7:0] regOut_4,
    output [7:0] regOut_5,
    output [7:0] regOut_6
);
    
    wire [7:0] decd_out;
    decoder3_8 decd(ld, dst, decd_out);
    
    reg8 register0(decd_out[0], dataIn, clk, rst, clk, regOut_0);
    reg8 register1(decd_out[1], dataIn, clk, rst, clk, regOut_1);
    reg8 register2(decd_out[2], dataIn, clk, rst, clk, regOut_2);
    reg8 register3(decd_out[3], dataIn, clk, rst, clk, regOut_3);
    reg8 register4(decd_out[4], dataIn, clk, rst, clk, regOut_4);
    reg8 register5(decd_out[5], dataIn, clk, rst, clk, regOut_5);
    reg8 register6(decd_out[6], dataIn, clk, rst, clk, regOut_6);

endmodule


module alu(
    input [7:0] src1,
    input [7:0] src2,
    input e,
    input [2:0] value,
    output reg [7:0] dst,
    output reg zero
);

    
    always @(*) begin
        if(e) begin
            case (value)
                0 : assign dst = src1 + src2; 
                1 : assign dst = src1 - src2;
                2 : assign dst = src1 << 1;
                3 : assign dst = src1;
                4 : assign dst = src1 & src2;
                5 : assign dst = src1 | src2;
                6 : assign dst = src1 ^ src2;
                7 : assign dst = ~src1;
            endcase
            if(!dst)
                assign zero = 1; 
            else
                assign zero = 0;
        end
        else 
            assign dst = 8'b11111111;
    end
    
    
endmodule

module ins_decoder(
    input [20:0] instruction,
    output reg z,
    output reg [2:0] op,
    output reg [7:0] im,
    output reg [2:0] src1,
    output reg [2:0] src2,
    output reg [2:0] dst
);

    initial begin
        assign z = instruction[20:20];
        assign op = instruction[19:17];
        assign im = instruction[16:9];
        assign src1 = instruction[8:6];
        assign src2 = instruction[5:3];
        assign dst = instruction[2:0];
    end

endmodule


module CPU(
    input [20:0] instruction,
    input clk,
    input rst
);

    wire z;
    wire [2:0] op;
    wire [7:0] im;
    wire [2:0] src1;
    wire [2:0] src2;
    wire [2:0] dst;
    
    wire zero;
    wire [7:0] alu_src1;
    wire [7:0] alu_src2;
    wire [7:0] alu_dst;
    
    wire [7:0] reg0, reg1, reg2, reg3, reg4, reg5, reg6;
    
    ins_decoder _ins_decoder(instruction, z, op, im, src1, src2, dst);
    
    register_file regfile(dst, ~(z & zero), clk, rst, alu_dst, reg0, reg1, reg2, reg3, reg4, reg5, reg6);
    
    mux8_1 mux1(src1, reg0, reg1, reg2, reg3, reg4, reg5, reg6, im, alu_src1);
    mux8_1 mux2(src2, reg0, reg1, reg2, reg3, reg4, reg5, reg6, im, alu_src2);
    
    alu _alu(alu_src1, alu_src2, ~(z & zero), op, alu_dst, zero);
    

endmodule
