import machine
import ssd1306
import time
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

pin1=machine.Pin(2,machine.Pin.IN)
pin2=machine.Pin(14,machine.Pin.IN,machine.Pin.PULL_UP)
pin3=machine.Pin(0,machine.Pin.IN)

i=0
def digitchange(p):
    global i
    i=i+1
    i=i%7
def addmins(p):
    global i
    rtc_datetime_list = list(rtc.datetime())
    rtc_datetime_list[i] = rtc_datetime_list[i]+1
    rtc.datetime(tuple(rtc_datetime_list)) 
def minusmins(p):
    global i
    rtc_datetime_list = list(rtc.datetime())
    rtc_datetime_list[i] = rtc_datetime_list[i]-1
    rtc.datetime(tuple(rtc_datetime_list)) 

pin1.irq(trigger=machine.Pin.IRQ_RISING,handler=digitchange)
pin2.irq(trigger=machine.Pin.IRQ_RISING,handler=addmins)
pin3.irq(trigger=machine.Pin.IRQ_RISING,handler=minusmins)

rtc=machine.RTC()
while(1):
    oled.fill(0)
    a=(rtc.datetime()[0],rtc.datetime()[1],rtc.datetime()[2])
    b=(rtc.datetime()[4],rtc.datetime()[5],rtc.datetime()[6])
    c=str(a)
    d=str(b)
    m=str(i)
    oled.text(c,0,0)
    oled.text(d,0,10)
    oled.text(m,0,20)
    oled.show()
    
        

    
