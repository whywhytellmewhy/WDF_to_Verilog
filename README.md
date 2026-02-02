# WDF_to_Verilog
This repository is created on 2025.12.9.
<br/>

## For the file `waveform_description.txt`
撰寫時注意事項：
- 非空白行的**第一行務必要填入「最終DWE的總 sample 數」**，例如若總sample數設計為「500000」，則填入：
    ```
    Total number of samples: 500000
    ```
    名稱務必要取作「`Total number of samples`」
- 訊號的部分以`<訊號名>:<waveform_description>`的格式撰寫，例如：
    ```
    signal1:  L5/(H2/L5/H1/L3)*10/L20/H3/L5
    signal2:  H10/L50/H20
    signal3:  L100
    ```
    - 注意：需為半形冒號（`:`）而**不能用全形冒號（`：`）**
    - 注意：訊號名稱**不能含有空格**
- 可以有空白行（python中會自動刪除）
- 可以有空格（python中會自動刪除）
- 可用井字號（`#`）作為註解，可為「單行註解」或「行末註解」，例如：
    ```
    ### 此為單行註解 ###
    signal1:  L5/(H2/L5/H1/L3)*10/L20/H3/L5 # 此為行末註解: 可用來說明此訊號
    signal2:  H10/L50/H20
    signal3:  L100 #此為行末註解
    ```
    註解中可以包含半形冒號（`:`），也可以包含空格
<br/>

## For the file `hdl.f`
- 可在此檔案中修改`SAMPLING_CLOCK_PERIOD`的值，例如當設定
    ```
    +define+SAMPLING_CLOCK_PERIOD=5
    ```
    則代表「1個sample長度為5ns」
- 可在此檔案中修改`CURRENT_SAMPLE_COUNTER_START_FROM`的值，例如當設定
    ```
    +define+CURRENT_SAMPLE_COUNTER_START_FROM=0
    ```
    則代表`current_sample_counter`這個訊號會從「0」開始數，數到「Total number of samples - 1」；當設定為`1`時則代表`current_sample_counter`這個訊號會從「1」開始數，數到「Total number of samples」。建議依照使用者喜好設定為「0」或「1」。
<br/>

## How to run WDF_to_Verilog
1. 將此 repository 的內容上傳至電機系工作站
2. 撰寫 Waveform Description File (WDF) 檔
3. 在terminal依序執行：
    ```=1
    cd WDF_to_Verilog
    sh run_WDF_to_Verilog.sh <WDF>
    sh run_sim.sh
    ```
    例如當Waveform Description File (WDF)檔名為`waveform_description.txt`，則：
    ```=1
    cd WDF_to_Verilog
    sh run_WDF_to_Verilog.sh waveform_description.txt
    sh run_sim.sh
    ```
    上述第2行是將WDF透過python轉換為Verilog testbench `test_pattern_generator.v`；第3行是將testbench執行RTL simulation得到VCD檔`test_pattern_generator.vcd`（另外也會產生FSDB檔`test_pattern_generator.fsdb`以供使用`nWave`查看波形）
4. 將VCD檔（`test_pattern_generator.vcd`）匯入至DWE 3.0軟體
<br/>

## Reference
1. `/Handover/compiler_pat_gen/run_hdl_sim_gen.sh` from「CIS compiler 交接資料」from 呂老師實驗室
2. `/Handover/compiler_pat_gen/hdl_sim_gen.py` from「CIS compiler 交接資料」from 呂老師實驗室
3. `/Handover/compiler_pat_gen/description_to_spec.py` from「CIS compiler 交接資料」from 呂老師實驗室
4. `/VLSI/midterm/check_results/run_sim_VLSI_TA_midterm.py` on EE workstation
