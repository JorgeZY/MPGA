#importing modules
import sys #for adding paths
sys.path.append('/home/pi/program/python_files/waveshare/1.5inch_OLED_Moudle/Raspberry/python/')
import time
from datetime import date
from datetime import datetime
# module for bme680 environmentla sendor
import bme680
# module for weather
import requests
# modules for OLED
import DEV_Config
import OLED_Driver
import subprocess # for stats
from PIL import Image,ImageDraw,ImageFont

x = 5
top = 5

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

def main():

    OLED = OLED_Driver.OLED()

    print ("**********Init OLED**********")
    OLED_ScanDir = OLED_Driver.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
    OLED.OLED_Init(OLED_ScanDir)
     
    #OLED.OLED_Clear()
    DEV_Config.Driver_Delay_ms(0.1)
    image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)# grayscale (luminance)
    draw = ImageDraw.Draw(image)
    #font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', "White")
    #font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
    # Load default font.
    font = ImageFont.load_default()    
       
    while True:        
                         
        #OLED.OLED_Clear()
        DEV_Config.Driver_Delay_ms(0.1)
        image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)# grayscale (luminance)
        draw = ImageDraw.Draw(image)
        #print ("***draw rectangle")
        #draw.rectangle([(0,0),(128,128)],fill = 0)
        
        #print('Polling:')
        #if sensor.get_sensor_data():
        #            output = '{0:.2f} C,{1:.2f} hPa,{2:.3f} %RH'.format(
        #                sensor.data.temperature,
        #                sensor.data.pressure,
        #                sensor.data.humidity)
        #            #print(output)
        #except KeyboardInterrupt:
        #    pass
        
        
        
        print("*********** page 1: stats ************")
        count = 0
        while (count < 20):
            count = count + 1
            #OLED.OLED_Clear()
            DEV_Config.Driver_Delay_ms(0.1)
            image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)# grayscale (luminance)
            draw = ImageDraw.Draw(image)
            
            # date and time
            today = date.today()
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            d1 = today.strftime("%d/%m/%Y")
            d2 = today.strftime("%B %d, %Y")
        
            # get stats
            cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
            IP = subprocess.check_output(cmd, shell = True )
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell = True )
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
            MemUsage = subprocess.check_output(cmd, shell = True )
            cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
            Disk = subprocess.check_output(cmd, shell = True )
            cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
            Temperature = subprocess.check_output(cmd, shell = True )
        
            print ("***draw line")
            draw.line([(x,top+36),(x+127,top+36)], fill = "White",width = 1)
     
            # display sdate and stats
            print ("***draw text")
            draw.text((x, top), d2, font=font, fill=255)
            draw.text((x, top+15), dt_string, font=font, fill=255)
            draw.text((x, top+45), "IP: " + str(IP,'utf-8'), font=font, fill=255)
            draw.text((x, top+60), "CPU Temp.: " + str(Temperature,'utf-8'),  font=font, fill=255)
            draw.text((x, top+75), str(CPU,'utf-8'), font=font, fill=255)
            draw.text((x, top+90), str(MemUsage,'utf-8'), font=font, fill=255)
            draw.text((x, top+105), str(Disk,'utf-8'), font=font, fill=255)

            # adding 10 seconds delay
            #time.sleep(1)
        
            OLED.OLED_ShowImage(image,0,0)
            draw = ImageDraw.Draw(image)
            time.sleep(0.1)
            #DEV_Config.Driver_Delay_ms(0.1)
                

        print ("********** Page 2 **********")
        #second page on display
        image = Image.open('/home/pi/program/python/OLED/ISP/flower.bmp')
        #this pis is small ,Will trigger an exception,but you can show
        OLED.OLED_ShowImage(image,0,0)

        # adding 2 seconds delay
        time.sleep(2)

        print ("********** Page 3: sensor **********")    
        #print("""temperature-pressure-humidity.py - Displays temperature, pressure, and humidity.
        #If you don't need gas readings, then you can read temperature, pressure and humidity quickly.
        #Press Ctrl+C to exit
        #""")      
        
        
        
        #second page on display
        image = Image.open('/home/pi/program/python/OLED/ISP/flower.bmp')
        #this pis is small ,Will trigger an exception,but you can show
        OLED.OLED_ShowImage(image,0,0)

        # adding 2 seconds delay
        time.sleep(2)

if __name__ == '__main__':
    main()

#except:
#print("except")
#GPIO.cleanup()

