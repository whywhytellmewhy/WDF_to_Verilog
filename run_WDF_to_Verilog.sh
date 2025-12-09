
if [ $# -eq 0 ];
then
  echo "Error: You should provide 1 input argument that specifies the name of the WDF file"
  echo "ex.: sh run_WDF_to_Verilog.sh waveform_description.txt"
  exit 1
elif [ $# -gt 1 ];
then
  echo "Error: Too many input arguments !!"
  exit 1
else
  python3 ./script/WDF_to_Verilog.py $1
fi
