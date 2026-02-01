
`timescale 1ns/1ps
//`define CYCLE 10
`define SAMPLING_CLOCK_PERIOD 5  // this parameter can be modified in "hdl.f"
// `define MAX_ALLOWED_SAMPLE_NUMBER 3000000
`define CURRENT_SAMPLE_COUNTER_START_FROM 0  // this parameter can be modified in "hdl.f"

// `define DUMP_VCD_FILE 1  // this would be defined in "run_sim.sh"



module test_pattern_generator #(
    // +++++ define parameters by WDF_to_Verilog.py +++++ //
);

// dump waveform
initial begin
    `ifdef DUMP_VCD_FILE
        $dumpfile("test_pattern_generator.vcd");
        // +++++ define signals to be dumped in VCD file by WDF_to_Verilog.py +++++ //
        // $dumpvars("+mda");
    `endif
    $fsdbDumpfile("test_pattern_generator.fsdb");
    $fsdbDumpvars("+mda");
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
    while(1) #(`SAMPLING_CLOCK_PERIOD * 0.5) sampling_clock = ~sampling_clock;
end

// create current sample counter
integer current_sample_counter;
initial begin
    current_sample_counter = `CURRENT_SAMPLE_COUNTER_START_FROM;
    // #(`SAMPLING_CLOCK_PERIOD * 0.01);  // in order NOT to aligned with sampling clock rising edge
    while(1) #(`SAMPLING_CLOCK_PERIOD) current_sample_counter = current_sample_counter + 1;
end


// +++++ define signals by WDF_to_Verilog.py +++++ //


// simulation for "Total_Number_of_Samples" samples
initial begin
	#(`SAMPLING_CLOCK_PERIOD * Total_Number_of_Samples);
	$display("\n=================================================================================");
	$display("  Simulation finished !!  ");
	$display("  You can check the FSDB waveform using nWave.  ");
    $display("  If all signals are as expected, then you can import the VCD file into DWE 3.0.  ");
 	$display("=================================================================================\n");
 	$finish;
end

endmodule

