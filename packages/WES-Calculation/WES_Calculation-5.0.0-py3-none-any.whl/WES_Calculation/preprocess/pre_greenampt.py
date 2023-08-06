'''
Date         : 2023-01-17 10:50:35
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-01-30 14:03:33
LastEditors  : BDFD
Description  : 
FilePath     : \WES_Calculation\preprocess\pre_greenampt.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
from execdata import convint as s2int, convfloat as s2dec
from ..greenampt import greenampt

# def gumbel_calculation():
def pre_greenampt(original_input):
    """
        function name:Waterfront Engineering Studio Gumbel
        input function:wes.greenampt(thetai, thetas, Psi, K, dti, nin, dd, i, iyesno, ss1, ss2, ss3)
        Keyword arguments:thetai, thetas, Psi, K, dti, nin, dd, i, iyesno, ss1, ss2, ss3
        argument -- description
        Return Description: plot_url, data, eff, note, note2
    """ 
    # print("original_input before process",original_input)
    thetai = float(0.28)# Initial soil moisture content
    thetas = float(0.4)# Soil moisture content at saturation (i.e. porosity)
    Psi = float(0.22) # Suction head (m)
    K = float(0.3) # Saturated hydraulic conductivity (cm/h)
    dti= float(5) #6 time interval in the analysis, normally that used in hyetograph (min)
    nin= int(12)# The number of time intervals to be considered in the anlysis
    iyesno = int(0) # Whether to generate an effective hyetograph (0: No; 1: Yes)
    ss1=0#Special Scenario 1#20220313
    ss2=0#Special Scenario 2#20220313
    ss3=0#Special Scenario 2#20220313
    dd=0
    i=[0 for k in range(nin)]# Hyetograph (mm/h) (The first value covers the period between time 0 and time 0+dti.)
    headings = []
    ending = "---结果展示结束---"

    result = greenampt(thetai, thetas, Psi, K, dti, nin, dd, i, iyesno, ss1, ss2, ss3)
    
    plot_url = result[0]
    data = result[1]
    eff = result[2]
    note = result[3]
    note2 = result[4]

    return headings, ending, plot_url, data, eff, note, note2