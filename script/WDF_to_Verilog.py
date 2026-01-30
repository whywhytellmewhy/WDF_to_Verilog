# import numpy as np
import re
from argparse import ArgumentParser

output_testbench_filename = "test_pattern_generator.v"

debug_mode = True


#-------------- Initialize command-line argument parser --------------#
##### (Initialize command-line argument parser) #####
# parser = ArgumentParser(description = "Usage: python3 WDF_to_Verilog.py <Waveform_Description_File_name>")
parser = ArgumentParser()

##### (Add command-line argument) #####
parser.add_argument("input_WDF_filename", help="Please provide input WDF file name.", default="")  ### positional command-line argument
# parser.add_argument("-test1", help="123456", default="")  ### optional command-line argument
# parser.add_argument("--test2", help="123456", default="")  ### optional command-line argument
args = parser.parse_args()

#print(args.input_WDF_filename)

error = False
signal_name_list = []
waveform_description_list = []

#-------------- Read WDF --------------#
print("[Info] Start reading WDF (" + args.input_WDF_filename + ")")
line_counter = 0
with open(args.input_WDF_filename, 'r') as f_WDF:
    for line in f_WDF.readlines():
        line_counter = line_counter + 1
        line = line.replace(' ', '')
        line = line.replace('\n', '')
        if (line == "") or (line[0] == "#"):
            continue
        line_list = line.split('#')
        if ':' in line_list[0]:
            line_list_without_comment = line_list[0].split(':')
            signal_name_list.append(line_list_without_comment[0])
            waveform_description_list.append(line_list_without_comment[1])
        else:
            error = True
            print("[Error] Cannot find ':' (" + args.input_WDF_filename + " Line " + str(line_counter) + ")")
            break
        
if signal_name_list[0]=="Totalnumberofsamples":
    try:
        total_number_of_samples = int(waveform_description_list[0])
    except ValueError as e:
        error = True
        print('[Error] The parameter "Total number of samples" is set as "' + waveform_description_list[0] + '", which is not an integer (in the file ' + args.input_WDF_filename + ')')
else:
    error = True
    print('[Error] Cannot find "Total number of samples" in the first non-blank line in ' + args.input_WDF_filename)
        
if error:
    exit()

print("[Info] Finish reading WDF (" + args.input_WDF_filename + ")")

signal_name_list = signal_name_list[1:]
waveform_description_list = waveform_description_list[1:]

total_number_of_signals = len(signal_name_list)
print("Total number of signals = " + str(total_number_of_signals))
print("Total number of samples = " + str(total_number_of_samples))
if debug_mode:
    print(signal_name_list)
    print(waveform_description_list)


#-------------- Generate testbench --------------#
def recursive_stage_split(f_write, signal_name, waveform_description, input_iteration_level):
    if (waveform_description[0] == '('):
        ##### (Found a group) #####
        split_group_list = waveform_description[1:].rsplit(')*', 1)
        repeat_number = int(split_group_list[1])
        
        f_write.write("for(repeat_counter_signal_level_" + str(input_iteration_level) + "=0;repeat_index_level_" + str(input_iteration_level) + "<" + repeat_number + ";repeat_index_level_" + str(input_iteration_level) + "=repeat_index_level_" + str(input_iteration_level) + "-1) begin\n")
        # recursive_stage_split(f_write, signal_name, waveform_description, input_iteration_level)
        f_write.write("end\n")
        
        waveform_description = split_group_list[0]
        
    split_waveform_description_list = re.split(r'/(?!\(*[^()]*\))',waveform_description)
    return output_iteration_level

print("[Info] Start generating testbench file (" + output_testbench_filename + ")")
with open(output_testbench_filename, 'w') as f_write:
    with open("./template/template_test_pattern_generator.v", 'r') as f_template:
        for line in f_template.readlines():
            if (line == "    // +++++ define parameter by WDF_to_Verilog.py +++++ //\n"):
                f_write.write("    // ===== generated parameter by WDF_to_Verilog.py ===== //\n")
                
                f_write.write("    parameter Total_Number_of_Signals = " + str(total_number_of_signals) + "\n")
                f_write.write("    parameter Total_Number_of_Samples = " + str(total_number_of_samples) + "\n")
            elif(line == "// +++++ define signals by WDF_to_Verilog.py +++++ //\n"):
                f_write.write("// ===== generated signals by WDF_to_Verilog.py ===== //\n")
                f_write.write("wire [Total_Number_of_Signals-1:0] signal_out;\n")
                
                for signal_index, signal_name in enumerate(signal_name_list):
                    if debug_mode:
                        print(str(signal_index)+". "+signal_name+" : "+waveform_description_list[signal_index])
                    f_write.write("\n\n//----- " + str(signal_index) + ". " + signal_name + " -----//\n")
                    f_write.write("reg " + signal_name + ";\n")
                    f_write.write("\nassign signal_out[" + str(signal_index) + "] = " + signal_name + ";\n")
                    iteration_level = recursive_stage_split(f_write, signal_name, waveform_description_list[signal_index], 1)
                    print("[Info] Finish processing signal #" + str(signal_index) + " (" + signal_name + "): it has " + iteration_level + " level of simplification")
                
                f_write.write("// ================================================== //\n")
            else:
                f_write.write(line)
                
