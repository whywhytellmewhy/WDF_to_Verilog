# WDF_to_Verilog
This repository is created on 2025.12.9.
<br/>

## For the file `waveform_description.txt`
撰寫時注意事項：
- 以`<訊號名>:<waveform_description>`的格式撰寫，例如：
    ```
    signal1:  L5/(H2/L5/H1/L3)*10/L20/H3/L5
    signal2:  H10/L50/H20
    signal3:  L100
    ```
    注意：需為半形冒號（`:`）而**不能用全形冒號（`：`）**
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

## Reference
1. `/Handover/compiler_pat_gen/run_hdl_sim_gen.sh` from「CIS compiler 交接資料」from 呂老師實驗室
2. `/Handover/compiler_pat_gen/hdl_sim_gen.py` from「CIS compiler 交接資料」from 呂老師實驗室
3. `/Handover/compiler_pat_gen/description_to_spec.py` from「CIS compiler 交接資料」from 呂老師實驗室
4. `/VLSI/midterm/check_results/run_sim_VLSI_TA_midterm.py` on EE workstation
