'''
Date         : 2023-01-17 19:23:01
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-01-30 13:43:52
LastEditors  : BDFD
Description  : 
FilePath     : \WES_Calculation\preprocess\pre_gumbel.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
from execdata import convint as s2int, convfloat as s2dec
from ..gumbel import gumbel

# def gumbel_calculation():
def pre_gumbel(original_input):
    """
        function name:Waterfront Engineering Studio Gumbel
        input function:wes.gumbel(pq, unitt, unitx, i1, i2, i3, meanx, sdx, n, dataolist)
        Keyword arguments:pq, unitt, unitx, i1, i2, i3, meanx, sdx, n, dataolist
        argument -- description
        Return Description: plot_url, nCl2, nlen, note1, note2, note3, data3, note4, data4, note5, data5, data6, heading1, heading2, ending
    """ 
    # print("original_input before process",original_input)
    pq = "物理量"
    unitx = "无单位"
    unitt = "单位时段"
    i1 = 2
    i2 = 1
    i3 = ''
    meanx = 1130.29
    sdx = 8.42
    n =24
    dataolist = ''

    result = gumbel(pq, unitt, unitx, i1, i2, i3, meanx, sdx, n, dataolist)

    plot_url = result[0]
    nCl2 = result[1]
    nlen = result[2]
    note1 = result[3]
    note2 = result[4]
    note3 = result[5]
    data3 = result[6]
    note4 = result[7]
    data4 = result[8]
    note5 = result[9]
    data5 = result[10]
    data6 = result[11]
    heading1 = result[12]
    heading2 = result[13]
    ending = result[14]

    return plot_url, nCl2, nlen, note1, note2, note3, data3, note4, data4, note5, data5, data6, heading1, heading2, ending
