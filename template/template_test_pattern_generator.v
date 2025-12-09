
`timescale 1ns/1ps
`define CYCLE 10
`define END_CYCLE 3000000

// `define USE_VCD_INSTEAD_OF_FSDB 1  // this would be defined in "run_sim.sh"



module test_pattern_generator #(
    `ifdef BASIC_VERSION
        parameter Number_of_Config = 5, // Excluding "total_level"
        parameter Config_Bit_Size = 13, // bottleneck by "upscale_scaling_ratio"
    `else
        parameter Number_of_Actual_Config = 25,
        parameter Number_of_Config = 25-8+1, // Excluding "total_level", after concatenate/merge all the 8 "or_not" together
        parameter Config_Bit_Size = 13, // bottleneck by "upscale_scaling_ratio" // Remember to modify bit size of "config_in" in "optical_flow_ISP_core.v"!!!
    `endif
    parameter u_v_Bit_Size = 10,
    parameter delta_It_Bit_Size = 11,
    parameter BRAM_Height = `IMAGE_HEIGHT/2,
    parameter BRAM_Height_Bit_Size = $clog2(BRAM_Height),
    parameter BRAM_Width = `IMAGE_WIDTH/2,
    parameter BRAM_Width_Bit_Size = $clog2(BRAM_Width),
    parameter BRAM_Data_Bit_Size_for_uv = u_v_Bit_Size*2, // if modified, remember to modify the same parameter in the "BRAM_controller" module, too
    parameter BRAM_Data_Bit_Size_for_delta_It = delta_It_Bit_Size, // if modified, remember to modify the same parameter in the "BRAM_controller" module, too
    parameter BRAM_Address_Bit_Size = $clog2(BRAM_Height*BRAM_Width) // if modified, remember to modify the same parameter in the "BRAM_controller" module, too
);

// dump waveform
initial begin
    `ifdef USE_VCD_INSTEAD_OF_FSDB
        $dumpfile("test_pattern_generator.vcd");
        $dumpvars("+mda");
    `else
        $fsdbDumpfile("test_pattern_generator.fsdb");
        $fsdbDumpvars("+mda");
    `endif
end

// create clk
reg clk;
initial begin
    clk = 0;
    while(1) #(`CYCLE/2) clk = ~clk;
end

// reset
reg reset_n;
initial begin
    reset_n = 1;
    #(`CYCLE) reset_n = 0;
    #(`CYCLE*5) reset_n = 1;
end






// working too long
initial begin
	#(`CYCLE * `END_CYCLE);
	$display("\n===================================================");
	$display("      Error!!! Simulation time is too long...      ");
	$display("    There might be something wrong in the code.    ");
 	$display("===================================================\n");
 	$finish;
end

endmodule

