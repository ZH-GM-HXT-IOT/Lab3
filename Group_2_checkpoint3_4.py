import machine
import ssd1306
import time
from machine import PWM, Pin
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
pin1=machine.Pin(2,machine.Pin.IN)
pin2=machine.Pin(14,machine.Pin.IN,machine.Pin.PULL_UP)
pin3=machine.Pin(0,machine.Pin.IN)
pwm1=PWM(machine.Pin(13))
pwm1.freq(60)
adc=machine.ADC(0)
i=0
j=0

ala=0

def digitchange(p):
    global i
    global j
    global ala
    if ala == 0:
        i=i+1
        i=i%7
    if ala == 1:
        j=j+1
        j=j%3
def addmins(p):
    global i
    global j
    global ala
    global ala_time
    if ala == 0:
        rtc_datetime_list = list(rtc.datetime())
        rtc_datetime_list[i] = rtc_datetime_list[i]+1
        rtc.datetime(tuple(rtc_datetime_list))
    if ala == 1:
        ala_time_list=list(ala_time)
        print (j)
        ala_time_list[j+4]=ala_time_list[j+4]+1
        ala_time = tuple(ala_time_list)
def minusmins(p):
    global i
    rtc_datetime_list = list(rtc.datetime())
    rtc_datetime_list[i] = rtc_datetime_list[i]-1
    rtc.datetime(tuple(rtc_datetime_list))

def alarmmode(p):
    global i
    global ala
    global ala_time
    global stat_first_time
    #print('in ala mode')
    if ala == 0:
        ala_time = (0,0,0,0,0,0,0,0)
        ala=1
    elif ala == 1:
        ala=0 

pin1.irq(trigger=machine.Pin.IRQ_RISING,handler=digitchange)
pin2.irq(trigger=machine.Pin.IRQ_RISING,handler=addmins)
pin3.irq(trigger=machine.Pin.IRQ_RISING,handler=alarmmode)

rtc=machine.RTC()
ala_time = (-1,-1,-1,-1,-1,-1,-1,-1)

while(1):
    oled.fill(0)
    a=(rtc.datetime()[0],rtc.datetime()[1],rtc.datetime()[2])
    b=(rtc.datetime()[4],rtc.datetime()[5],rtc.datetime()[6])
    c=str(a)
    d=str(b)
    m=str(i)
    e=(ala_time[4],ala_time[5],ala_time[6])
    f=str(e)
    
    if ala == 1:
       oled.text(str(j),110,20)
        
        

    elif ala == 0:
        pwm1.duty(0)
        buffer_time = rtc.datetime()

        if ala_time[4:7] == buffer_time[4:7]:
            print ("in if")
            pwm1.duty(500)
            time.sleep(5)
            pwm1.duty(0)
            ala=0
#            break

    oled.text(f,20,20)
    sen=adc.read()
    oled.contrast(sen)
    oled.text(c,0,0)
    oled.text(d,0,10)
    oled.text(m,0,20)
    oled.show()
    
   # time.sleep(.5)
    
        

    
