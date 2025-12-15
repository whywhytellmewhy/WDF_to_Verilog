
`timescale 1ns/1ps
//`define CYCLE 10
`define SAMPLING_CLOCK_PERIOD 5 // corresponding to "CYCLE = 10"
`define MAX_ALLOWED_SAMPLE_NUMBER 3000000

// `define USE_VCD_INSTEAD_OF_FSDB 1  // this would be defined in "run_sim.sh"



module test_pattern_generator #(
    // +++++ define parameter by WDF_to_Verilog.py +++++ //
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


// simulation too long
initial begin
	#(`SAMPLING_CLOCK_PERIOD * `MAX_ALLOWED_SAMPLE_NUMBER);
	$display("\n=================================================================================");
	$display("  Error!!! Simulation time is too long (The number of samples exceeded 'MAX_ALLOWED_SAMPLE_NUMBER')  ");
	$display("  You can change the value in 'MAX_ALLOWED_SAMPLE_NUMBER' in hdl.f if needed.  ");
    $display("  Or perhaps there might be something wrong.  ");
 	$display("=================================================================================\n");
 	$finish;
end

endmodule

