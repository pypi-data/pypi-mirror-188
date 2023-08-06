'''
Date         : 2023-01-17 19:23:01
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-01-30 13:59:43
LastEditors  : BDFD
Description  : 
FilePath     : \WES_Calculation\preprocess\pre_windspeed.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
from execdata import convint as s2int, convfloat as s2dec
from ..windspeed import windspeed

# def windspeed_calculation():
def pre_windspeed(original_input):
    """
        function name:Waterfront Engineering Studio Windspeed
        input function:wes.windspeed(o2, input_zw, input_Xlat, input_X, input_Rg, input_beta, input_atm, input_Ta, input_zt, input_Tw, input_Taa, input_wdu, input_zu)
        Keyword arguments:o2, input_zw, input_Xlat, input_X, input_Rg, input_beta, input_atm, input_Ta, input_zt, input_Tw, input_Taa, input_wdu, input_zu
        argument -- description
        Return Description: img_stream, heading, section1, section2, section2_note, section3, section4, section5, section6, section7, ending
    """ 
    o2=3# catagory of known windspeed: #1) low-level overwater wind; 2) low-level overland wind (onshore wind at an anemometer immediately adjacent to water);
    #3) low-level overland wind (other scenarios); 4) geostrophic winds
    zw=12# the elevation of known windspeed above water/ground level (m)
    Xlat=45
    X=25
    Rg=None

    U=21# known average wind speed at zw(m/s)
    atm=3 # averaging time of known windspped (min)
    Ta=18 # known air temperature at zt (C Degrees)
    zt=10 # the elevation of known temperture above water/ground level (m)
    Tw=15 # known water surface temperature at C Degrees 
    TaaC=16# known mean air temperature of the constant-stress layer (C Degrees)
    wdu=10 # required averaging time for windspped (min) (A wanrning will show if wdu<=1/60 or wdu>=600!!)
    zu=50 # the maximum height for profile illustration (<=zcsy)

    result = windspeed(o2, zw, Xlat, X, Rg, U, atm, Ta, zt, Tw, TaaC, wdu, zu)
    
    plot_url = result[0]
    heading = result[1]
    section1 = result[2]
    section2 = result[3]
    section2_note = result[4]
    section3 = result[5] 
    section4 = result[6] 
    section5 = result[7]
    section6 = result[8]
    section7 = result[9]
    ending = result[10] 
    return plot_url, heading, section1, section2, section2_note, section3, section4, section5, section6, section7, ending