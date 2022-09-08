# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 22:41:23 2022

@author: anddy
"""

import ctypes

def update_Background():
    SPI_SETDESKWALLPAPER = 20 
    ctypes.windll.user32.SystemParametersInfoW(20, 
                                               0, 
                                               r"C:\NotionUpdate\progress\jpg files\Monthly Evaluation\month.jpg" 
                                               , 0)


