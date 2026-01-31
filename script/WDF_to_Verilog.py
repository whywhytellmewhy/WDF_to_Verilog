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
def count_Max_iteration_level(signal_name, waveform_description):
    output_Max_iteration_level = 0
    current_iteration_level = 0
    
    for character in waveform_description:
        if (character == '('):
            current_iteration_level = current_iteration_level + 1
            output_Max_iteration_level = max(output_Max_iteration_level, current_iteration_level)
        if (character == ')'):
            current_iteration_level = current_iteration_level - 1
            
    if (current_iteration_level != 0):
        error = True
        print("[Error] The number of '(' does NOT match the number of ')' in the waveform description of the signal " + '"' + signal_name + '"')
        exit()
    return output_Max_iteration_level
    
def recursive_stage_split(f_write, signal_name, waveform_description, input_iteration_level):
    output_iteration_level = 1
    if debug_mode:
        print(signal_name+" (iteration level = "+str(input_iteration_level)+"): "+waveform_description)
    split_waveform_description_list = re.split(r'/(?!\(*[^()]*\))',waveform_description)
    for waveform_description_element in split_waveform_description_list:
        tab_multiple = "    " * input_iteration_level
        if (waveform_description_element[0] == '('):
            ##### (Found a group) #####
            split_group_list = waveform_description_element[1:].rsplit(')*', 1)
            repeat_number = int(split_group_list[1])
            
            repeat_index = signal_name + "_repeat_counter_level[" + str(input_iteration_level) + "]"
            f_write.write(tab_multiple + "for(" + repeat_index + "=0;" + repeat_index + "<" + str(repeat_number) + ";" + repeat_index + "=" + repeat_index + "-1) begin\n")
            temp_iteration_level = recursive_stage_split(f_write, signal_name, split_group_list[0], input_iteration_level+1)
            output_iteration_level = max(output_iteration_level, temp_iteration_level)
            f_write.write(tab_multiple + "end\n")
        else:
            f_write.write(tab_multiple + waveform_description_element + "\n")
            output_iteration_level = max(output_iteration_level, input_iteration_level)
    return output_iteration_level

print("[Info] Start generating testbench file (" + output_testbench_filename + ")")
with open(output_testbench_filename, 'w') as f_write:
    with open("./template/template_test_pattern_generator.v", 'r') as f_template:
        for line in f_template.readlines():
            if (line == "    // +++++ define parameters by WDF_to_Verilog.py +++++ //\n"):
                f_write.write("    // ===== generated parameter by WDF_to_Verilog.py ===== //\n")
                
                f_write.write("    parameter Total_Number_of_Signals = " + str(total_number_of_signals) + ",\n")
                f_write.write("    parameter Total_Number_of_Samples = " + str(total_number_of_samples) + "\n")
            elif(line == "// +++++ define signals by WDF_to_Verilog.py +++++ //\n"):
                f_write.write("// ===== generated signals by WDF_to_Verilog.py ===== //\n")
                # f_write.write("wire [Total_Number_of_Signals-1:0] signal_out;\n")
                f_write.write("wire [Total_Number_of_Signals:1] signal_out;\n")
                
                for signal_index, signal_name in enumerate(signal_name_list):
                    displayed_signal_index = signal_index + 1
                    if debug_mode:
                        print(str(displayed_signal_index)+". "+signal_name+" : "+waveform_description_list[signal_index])
                    
                    f_write.write("\n\n//----- " + str(displayed_signal_index) + ". " + signal_name + " -----//\n")
                    f_write.write("reg " + signal_name + ";\n")
                    
                    Max_iteration_level = count_Max_iteration_level(signal_name, waveform_description_list[signal_index])
                    if (Max_iteration_level == 0):
                        # Do nothing
                        True
                    # elif(Max_iteration_level == 1):
                    #     f_write.write("integer " + signal_name + "_repeat_counter;\n")
                    #     f_write.write("integer repeat_counter_signal_" + str(displayed_signal_index) + ";\n")
                    else:
                        f_write.write("integer " + signal_name + "_repeat_counter_level [" + str(Max_iteration_level) + ":1];\n")
                        f_write.write("integer repeat_counter_signal_" + str(displayed_signal_index) + "_level [" + str(Max_iteration_level) + ":1];\n")
                    
                    f_write.write("\nassign signal_out[" + str(displayed_signal_index) + "] = " + signal_name + ";\n")
                    if (Max_iteration_level == 0):
                        # Do nothing
                        True
                    else:
                        f_write.write("always @* begin\n")
                        for i in range(Max_iteration_level):
                            f_write.write("    repeat_counter_signal_" + str(displayed_signal_index) + "_level[" + str(i+1) + "] = " + signal_name + "_repeat_counter_level[" + str(i+1) + "];\n")
                        f_write.write("end\n")
                    
                    f_write.write("\ninitial begin\n")
                    iteration_level = recursive_stage_split(f_write, signal_name, waveform_description_list[signal_index], 1)
                    f_write.write("end\n")
                    print("[Info] Finish processing signal #" + str(displayed_signal_index) + " (" + signal_name + "): it has " + str(iteration_level) + " level of simplification")
                
                f_write.write("\n\n// ================================================== //\n")
            else:
                f_write.write(line)
                
