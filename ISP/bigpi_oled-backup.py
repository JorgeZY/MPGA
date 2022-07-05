# https://api.openweathermap.org/data/2.5/weather?appid=f9668e84e5d16c37240685ad25a25a9f&q=Shanghai
# API = f9668e84e5d16c37240685ad25a25a9f

 #importing modules
import sys #for adding paths
sys.path.append('/home/pi/code/python_files/waveshare/1.5inch_OLED_Moudle/Raspberry/python/')
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
from pprint import pprint


x = 5
top = 5

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
     
    #OLED.OLED_Clear()
    DEV_Config.Driver_Delay_ms(0.1)
    image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)# grayscale (luminance)
    draw = ImageDraw.Draw(image)
    #font3 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', "White")
    #font2 = ImageFont.truetype('/usr/share/fonts/truetype/ttf-bitstream-vera/VeraMoBd.ttf', 11)
    # Load default font.
    font = ImageFont.load_default()    
    
    print ("********** boot waiting time 60s **********")
    #second page on display
    image = Image.open('/home/pi/code/python/OLED/ISP/flower.bmp')
    #this pis is small ,Will trigger an exception,but you can show
    OLED.OLED_ShowImage(image,0,0)

    # adding 60 seconds delay
    time.sleep(1)    
       
    while True:        
                         
        #OLED.OLED_Clear()
        DEV_Config.Driver_Delay_ms(0.1)
        image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)# grayscale (luminance)
        draw = ImageDraw.Draw(image)
        #print ("***draw rectangle")
        #draw.rectangle([(0,0),(128,128)],fill = 0)
        
      
        
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
            #d1 = today.strftime("%d/%m/%Y")
            d2 = today.strftime("%B %d, %Y")
            #env SUDO_ASKPASS=/usr/lib/piclone/pwdpic.sh sudo -AE dbus-launch piclone
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
                

        #print ("********** Page 2 **********")
        #image = Image.open('/home/pi/program/python/OLED/ISP/flower.bmp')
        ##this pis is small ,Will trigger an exception,but you can show
        #OLED.OLED_ShowImage(image,0,0)

        ## adding 0.5 seconds delay
        #time.sleep(0.5)

        print("*********** page 2: sensor ************")
        #print("""temperature-pressure-humidity.py - Displays temperature, pressure, and humidity.
        #If you don't need gas readings, then you can read temperature, pressure and humidity quickly.
        #Press Ctrl+C to exit
        #""") 
        
        count = 0
        while (count < 10):
            count = count + 1
            
            #OLED.OLED_Clear()
            DEV_Config.Driver_Delay_ms(0.1)
            image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)# grayscale (luminance)
            draw = ImageDraw.Draw(image)

            # date and time
            today = date.today()
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            #d1 = today.strftime("%d/%m/%Y")
            d2 = today.strftime("%B %d, %Y")
            
            '''
            if sensor.get_sensor_data():
                output = '{0:.2f} C,  {1:.2f} hPa,  {2:.3f} %RH'.format(
                    sensor.data.temperature,
                    sensor.data.pressure,
                    sensor.data.humidity)
                print(output)
            '''    
            sensor.get_sensor_data()    
            print ("***draw line")
            draw.line([(x,top+36),(x+127,top+36)], fill = "White",width = 1)
     
            # display sdate and stats
            print ("***draw date")
            draw.text((x, top), d2, font=font, fill=255)
            draw.text((x, top+15), dt_string, font=font, fill=255)

            print("***temperature")
            #draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((x, top+45), "RT.: ", fill="white")
            draw.text((x+50, top+45), temp(), fill="white")
        
            print("***humidity")
            draw.text((x, top+65), "Humi.: ", font=font, size=14, fill="white")
            draw.text((x+50, top+65), humi(), font=font, size=14, fill="white")
            
            print("***pressure")
            draw.text((x, top+85), "Pres.: ", font=font, size=14, fill="white")
            draw.text((x+50, top+85), pres(), font=font, size=14, fill="white")
        
        
            time.sleep(0.5)
        
                     
            OLED.OLED_ShowImage(image,0,0)
            draw = ImageDraw.Draw(image)
            time.sleep(0.1)
            #DEV_Config.Driver_Delay_ms(0.1)        

        print ("********** Page 3: weather **********")    
        # count = 0
        #while (count < 1):
        #   count = count + 1
           
        #OLED.OLED_Clear()
        DEV_Config.Driver_Delay_ms(0.1)
        image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)# grayscale (luminance)
        draw = ImageDraw.Draw(image)
     
        # API KEY
        API_key = "f9668e84e5d16c37240685ad25a25a9f"
           
        # This stores the url
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
 
        # This will ask the user to enter city ID
        #city_name = input("Enter a city Name : ")
        city_name = "Shanghai" 
            
        units = "&units=metric"
 
        # This is final url. This is concatenation of base_url, API_key and city_id
        Final_url = base_url + "appid=" + API_key + "&q=" + city_name + units
 
        # this variable contain the JSON data which the API returns
        weather_data = requests.get(Final_url).json()
 
        #JSON data is difficult to visualize, so you need to pretty print 
        #print("\nCurrent Weather Data Of " + city_name +":\n")
        pprint(weather_data)

        # JSON data works just similar to python dictionary and you can access the value using [].
        # Accessing Temperature, temperature resides in main and its key is temp 
        temp_out = weather_data['main']['temp']
        humi_out = weather_data['main']['humidity']
        temp_max = weather_data['main']['temp_max']
        temp_min = weather_data['main']['temp_min']
 
        #Accessing wind speed, it resides in wind and its key is speed
        wind_speed = weather_data['wind']['speed']
 
        # Accessing Description, it resides in weather and its key is description 
        description = weather_data['weather'][0]['description']
 
        # Accessing Latitude, it resides in coord and its key is lat 
        #latitude = weather_data['coord']['lat']
 
        # Accessing Longitude, it resides in coord and its key is lon 
        #longitude = weather_data['coord']['lon']
            
        print ("***draw line")
        draw.line([(x,top+36),(x+127,top+36)], fill = "White",width = 1)
 
        # Printing Data
        print('Shanghai Weather')
        draw.text((x, top+15), "Shanghai weather", font=font, fill=255)
        draw.text((x, top), d2, font=font, fill=255)
                   
        print('\nTemperature : ',temp_out)
        draw.text((x, top+45), "Outside T.: " + str(temp_out) + "'C" ,  font=font, fill=255)
        draw.text((x, top+55), str(temp_min) + "C to " + str(temp_max) + "C",  font=font, fill=255)
           
           
        print('\nHumidity : ',humi_out)
        draw.text((x, top+70), "Humidity: " + str(humi_out) + " %",  font=font, fill=255)
 
        print('\nWind Speed : ',wind_speed)
        draw.text((x, top+85), "Wind speed: " + str(wind_speed), font=font, fill=255)
            
        print('\nDescription : ',description)
        draw.text((x, top+100), str(description), font=font, fill=255)
            
        #print('\nLatitude : ',latitude)
        #draw.text((x, top+90), "latitude: " + str(latitude), font=font, fill=255)
           
        #print('\nLongitude : ',longitude)
        #draw.text((x, top+105), "longitude: " + str(longitude), font=font, fill=255)
        
        print("wait 1 seconds")    
        time.sleep(1)
        
                     
        OLED.OLED_ShowImage(image,0,0)
        draw = ImageDraw.Draw(image)
        time.sleep(10)
        #DEV_Config.Driver_Delay_ms(0.1) 
        
        
        print ("********** Page 4 **********")
        
        #OLED.OLED_Clear()
        DEV_Config.Driver_Delay_ms(0.1)
        image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)# grayscale (luminance)
        draw = ImageDraw.Draw(image)
        
        city = 'Shanghai'
        # Display the message
        #print('Displaying Weather report for: ' + city)
        #fetch the weather details
        url = 'https://wttr.in/{}?0'.format(city)
        #for weekly preview use url = 'https://wttr.in/{}'.format(city)
        res = requests.get(url)

        #display the results
        print(res.text)
        print("wait 2 seconds")    
        time.sleep(2)
        
        print ("********** Page 5**********")
        
        image = Image.open('/home/pi/code/python/OLED/ISP/flower.bmp')
        #this pis is small ,Will trigger an exception,but you can show
        OLED.OLED_ShowImage(image,0,0)

        # adding 1 seconds delay
        time.sleep(1)

if __name__ == '__main__':
    main()

#except:
#print("except")
#GPIO.cleanup()



 
