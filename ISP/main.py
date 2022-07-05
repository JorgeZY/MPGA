 # -*- coding:UTF-8 -*-
 ##
 # | file       :   main.py
 # | version    :   V1.0
 # | date       :   2017-12-08
 # | function   :   1.5inch OLED 
 #					import subprocess
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 #
 
import DEV_Config
import OLED_Driver

import subprocess # for stats

from PIL import Image,ImageDraw,ImageFont
x = 5
top = 5
#try:
def main():
    OLED = OLED_Driver.OLED()

    print ("**********Init OLED**********")
    OLED_ScanDir = OLED_Driver.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
    OLED.OLED_Init(OLED_ScanDir)

     #OLED.OLED_Clear()
    DEV_Config.Driver_Delay_ms(5000)
    image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)# grayscale (luminance)
    draw = ImageDraw.Draw(image)
    #font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', "White")
    # Load default font.
    font = ImageFont.load_default()

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
    draw.line([(0,0),(127,0)], fill = "White",width = 1)
    draw.line([(127,0),(127,127)], fill = "White",width = 1)
    draw.line([(127,127),(0,127)], fill = "White",width = 1)
    draw.line([(0,127),(0,0)], fill = "White",width = 1)
    #print ("***draw rectangle")
    #draw.rectangle([(18,10),(110,20)],fill = "White")

    print ("***draw text")
    #draw.text((33, 22), 'WaveShare ', fill = "White")
    #draw.text((32, 36), 'Electronic ', fill = "White")
    #draw.text((28, 48), '1.5inch OLED ', fill = "White")
    
    # display stats
    draw.text((x, top), "IP: " + str(IP,'utf-8'), font=font, fill=255)
    draw.text((x, top+15), str(CPU,'utf-8'), font=font, fill=255)
    draw.text((x, top+30), str(MemUsage,'utf-8'), font=font, fill=255)
    draw.text((x, top+45), str(Disk,'utf-8'), font=font, fill=255)
    draw.text((x, top+60), "CPU Temp.: " + str(Temperature,'utf-8'),  font=font, fill=255)
        
    OLED.OLED_ShowImage(image,0,0)
    DEV_Config.Driver_Delay_ms(5000)

    image = Image.open('flower.bmp')#this pis is small ,Will trigger an exception,but you can show
    OLED.OLED_ShowImage(image,0,0)
    
    
	
if __name__ == '__main__':
    main()

#except:
#	print("except")
#	GPIO.cleanup()
