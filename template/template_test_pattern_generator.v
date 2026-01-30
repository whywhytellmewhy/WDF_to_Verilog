
`timescale 1ns/1ps
//`define CYCLE 10
`define SAMPLING_CLOCK_PERIOD 5  // this parameter can be modified in "hdl.f"
// `define MAX_ALLOWED_SAMPLE_NUMBER 3000000

// `define USE_VCD_INSTEAD_OF_FSDB 1  // this would be defined in "run_sim.sh"



module test_pattern_generator #(
    // +++++ define parameters by WDF_to_Verilog.py +++++ //
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
/*reg clk;
initial begin
    clk = 0;
    while(1) #(`CYCLE/2) clk = ~clk;
end*/

// reset
/*reg reset_n;
initial begin
    reset_n = 1;
    #(`CYCLE) reset_n = 0;
    #(`CYCLE*5) reset_n = 1;
end*/

// create sampling clock
reg sampling_clock;
initial begin
    sampling_clock = 0;
    while(1) #(`SAMPLING_CLOCK_PERIOD/2) sampling_clock = ~sampling_clock;
end


// +++++ define signals by WDF_to_Verilog.py +++++ //


// simulation for "Total_Number_of_Samples" samples
initial begin
	#(`SAMPLING_CLOCK_PERIOD * Total_Number_of_Samples);
	$display("\n=================================================================================");
	$display("  Simulation finished !!  ");
	$display("  You can check the VCD waveform using nWave.  ");
 	$display("=================================================================================\n");
 	$finish;
end

endmodule

