import numpy as np
from argparse import ArgumentParser

output_testbench_filename = "test_pattern_generator.v"


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
        
if error:
    exit()

# print(signal_name_list)
# print(waveform_description_list)

print("[Info] Finish reading WDF (" + args.input_WDF_filename + ")")


#-------------- Generate testbench --------------#
print("[Info] Start generating testbench file (" + output_testbench_filename + ")")
# with open(output_testbench_filename, 'w') as f_write:
#     with open("./template/template_test_pattern_generator.v", 'r') as f_template:
#         for line in f_template.readlines():
            
