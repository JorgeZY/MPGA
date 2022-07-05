#from luma.core.interface.serial import i2c
#from luma.core.render import canvas
#from luma.oled.device import sh1106
import sys #for adding paths
sys.path.append('/home/pi/program/python_files/waveshare/1.5inch_OLED_Moudle/Raspberry/python/')
import DEV_Config
import OLED_Driver
import time
import bme680
from PIL import Image,ImageDraw,ImageFont
from luma.core.render import canvas

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)


# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

#device = sh1106(i2c(port=1, address=0x3C), rotate = 2)

sensor.data.temperature = 0
sensor.data.pressure = 0
sensor.data.humidity = 0

 

#subprograms
def temp():
    return " %.2f C" \
        % (sensor.data.temperature)

def humi():
    return " %.2f %%" \
        % (sensor.data.humidity)

def pres():
    return "%.2f hPa" \
        % (sensor.data.pressure)
    
def main():
    
    OLED = OLED_Driver.OLED()    
    print ("**********Init OLED**********")
    OLED_ScanDir = OLED_Driver.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
    OLED.OLED_Init(OLED_ScanDir)


#main program
count = 0
while (count < 10):
    count = count + 1
    '''
    if sensor.get_sensor_data():
        output = '{0:.2f} C,  {1:.2f} hPa,  {2:.3f} %RH'.format(
            sensor.data.temperature,
            sensor.data.pressure,
            sensor.data.humidity)
        print(output)
    '''    
    sensor.get_sensor_data()    

    #OLED.OLED_Clear()
    DEV_Config.Driver_Delay_ms(0.1)
    image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)# grayscale (luminance)
    draw = ImageDraw.Draw(image)
    #print ("***draw rectangle")
    #draw.rectangle([(0,0),(128,128)],fill = 0)

    #draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((10, 5), "TEMP : ", fill="white")
    draw.text((50, 5), temp(), fill="white")
        
    draw.text((10, 25), "HUMI : ", fill="white")
    draw.text((50, 25), humi(), fill="white")

    draw.text((10, 45), "PRES : ", fill="white")
    draw.text((50, 45), pres(), fill="white")
        
        
    time.sleep(1)
    
      
   
	
if __name__ == '__main__':
    main()    