#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 15:05:18 2022

@author: RSCHWIED
"""
import sys #for adding paths
sys.path.append('/home/pi/code/python_files/waveshare/1.5inch_OLED_Moudle/Raspberry/python/')
import time
import DEV_Config
import OLED_Driver
from PIL import Image,ImageDraw,ImageFont
import requests

def main():

    OLED = OLED_Driver.OLED()

    print ("**********Init OLED**********")
    OLED_ScanDir = OLED_Driver.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
    OLED.OLED_Init(OLED_ScanDir)
     
    #OLED.OLED_Clear()
    DEV_Config.Driver_Delay_ms(0.1)
    image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)# grayscale (luminance)
    draw = ImageDraw.Draw(image)
        # Load default font.
    font = ImageFont.load_default()    
    
    print ("********** boot waiting time 1s **********")
    #second page on display
    image = Image.open('/home/pi/code/python/OLED/ISP/flower.bmp')
    #this pis is small ,Will trigger an exception,but you can show
    OLED.OLED_ShowImage(image,0,0)

    # adding 60 seconds delay
    time.sleep(1)   
    
    #OLED.OLED_Clear()
    DEV_Config.Driver_Delay_ms(0.1)
    image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)# grayscale (luminance)
    draw = ImageDraw.Draw(image)
    

    #city = input('input the city name')
    #print(city)
    city = 'Shanghai'

    # Display the message
    #print('Displaying Weather report for: ' + city)

    #fetch the weather details
    url = 'https://wttr.in/{}?0'.format(city)
    #for weekly preview use url = 'https://wttr.in/{}'.format(city)
    res = requests.get(url)

    #display the results
    draw.text((0,0),str(res.text), fill=255)

if __name__ == '__main__':
    main()

#except:
#print("except")
#GPIO.cleanup()    