import machine
import time
import ustruct

import ssd1306
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 32

ADXL345_REG_DEVID = 0x00
ADXL345_REG_DATAX0 =(0x32)
ADXL345_REG_DATAY0  = (0x34)
ADXL345_REG_POWER_CTL = (0x2D)
ADXL345_MG2G_MULTIPLIER  = (0.004)  
SENSORS_GRAVITY_EARTH    =  (9.80665) 


cs = machine.Pin(15, machine.Pin.OUT)
cs.on()
spi = machine.SPI(1, baudrate=400000, polarity=1, phase=1)


def regread(reg_add):
    reg_add = reg_add|0x80
    reg_add = ustruct.pack('B',reg_add)
    cs.off()
    spi.write(reg_add)
    readout = spi.read(1)
    cs.on()
    print(readout)
    

def regread16(reg_add):
    reg_add = reg_add|0x80
    reg_add = reg_add|0x40
    reg_add = ustruct.pack('B',reg_add)
    cs.off()
    spi.write(reg_add)
    readout = spi.read(2)
    cs.on()
    return readout

def regwrite(reg_add,value):
    #reg_add = reg_add & 0x7f
    reg_add = ustruct.pack('B',reg_add)
    value = ustruct.pack('B',value)
    cs.off()
    spi.write(reg_add)
    spi.write(value)
    cs.on()
    
def init():
    regread(ADXL345_REG_DEVID)
    regread(ADXL345_REG_POWER_CTL)
    regread(0x31)
    regwrite(ADXL345_REG_POWER_CTL,0x08)
    regread(ADXL345_REG_POWER_CTL)

def getx():
    readout = regread16(ADXL345_REG_DATAX0)
    #print(readout)
    readout =  ustruct.unpack('h',readout)
    #print(readout)
    return readout[0]*ADXL345_MG2G_MULTIPLIER*SENSORS_GRAVITY_EARTH

def gety():
    readout = regread16(ADXL345_REG_DATAY0)
    #print(readout)
    readout =  ustruct.unpack('h',readout)
    #print(readout)
    return readout[0]*ADXL345_MG2G_MULTIPLIER*SENSORS_GRAVITY_EARTH

outx = getx()
outy = gety()
x_pos = 0
y_pos = 0

def detect_move_X():
    global outx
    global x_pos
    new_outx = getx()
    deltax = new_outx - outx
    outx = new_outx
    print ("x:" + str(deltax))

    if deltax > 0.8:
        x_pos = x_pos - 16
    elif deltax > 0.5:
        x_pos = x_pos - 4
    elif deltax < -1:
        x_pos = x_pos + 16
    elif deltax <-0.8:
        x_pos = x_pos + 4

    if x_pos < 0:
        x_pos = 0
    if x_pos > SCREEN_WIDTH:
        x_pos = SCREEN_WIDTH

def detect_move_Y():
    global outy
    global y_pos
    new_outy = gety()
    deltay = new_outy - outy
    outy = new_outy
    print ("y:" + str(deltay))

    if deltay > 0.8:
        y_pos = y_pos - 4
    elif deltay > 0.5:
        y_pos = y_pos - 2
    elif deltay < -1:
        y_pos = y_pos + 4
    elif deltay <-0.8:
        y_pos = y_pos + 2

    if y_pos < 0:
        y_pos = 0
    if y_pos > SCREEN_HEIGHT:
        y_pos = SCREEN_HEIGHT

def show_text(x,y):
    oled.text("cn dota",x,y)
    oled.text("best dota",x,y+10)
    
init()


while(1):
    oled.fill(0)
    detect_move_X()
    detect_move_Y()
    show_text(x_pos,y_pos)
    oled.show()
#    time.sleep(.2)
#    print(getx())
#    time.sleep(2)
