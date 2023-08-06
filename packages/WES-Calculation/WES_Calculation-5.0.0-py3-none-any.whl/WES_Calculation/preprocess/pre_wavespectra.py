'''
Date         : 2023-01-17 19:23:01
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-01-30 13:53:45
LastEditors  : BDFD
Description  : 
FilePath     : \WES_Calculation\preprocess\pre_wavespectra.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
from execdata import convint as s2int, convfloat as s2dec
from ..wavespectra import wave

# def gumbel_calculation():
def pre_wavespectra(original_input):
    """
        function name:Waterfront Engineering Studio WaveSpectra
        input function: wes.wave(c1, d, X, U, el, gamma, Hs, Tz, Ts, Tp)
        Keyword arguments:c1, d, X, U, el, gamma, Hs, Tz, Ts, Tp
        argument -- description
        Return Description: img_stream, heading, data1, data1_heading, data2, data2_heading, content, ending
    """ 
    # print("original_input before process",original_input)
    c1 = 2
    d = 0
    X = 370000
    U = 10
    el = 12
    gamma = 3.3 
    Hs = 2
    Tz = 5 
    Ts = 5.5
    Tp = 6
    
    result = wave(c1, d, X, U, el, gamma, Hs, Tz, Ts, Tp)
 
    plot_url = result[0]
    heading = result[1]
    data1 = result[2]
    data1_heading = result[3]
    data2 = result[4] 
    data2_heading = result[5] 
    content = result[6] 
    ending = result[7]
    return plot_url, heading, data1, data1_heading, data2, data2_heading, content, ending