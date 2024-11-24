import time
from machine import I2C, Pin

# I2C address and command bit
TCS34725_ADDRESS = 0x29
TCS34725_COMMAND_BIT = 0x80

# Interrupt Enable register
TCS34725_ENABLE = 0x00
TCS34725_ENABLE_AIEN = 0x10
TCS34725_ENABLE_WEN = 0x08
TCS34725_ENABLE_AEN = 0x02
TCS34725_ENABLE_PON = 0x01

# Integration time
TCS34725_ATIME = 0x01

# Wait time
TCS34725_WTIME = 0x03
TCS34725_WTIME_2_4MS = 0xFF
TCS34725_WTIME_204MS = 0xAB
TCS34725_WTIME_614MS = 0x00

# Interrupt thresholds
TCS34725_AILTL = 0x04
TCS34725_AILTH = 0x05
TCS34725_AIHTL = 0x06
TCS34725_AIHTH = 0x07

# Persistence register
TCS34725_PERS = 0x0C
TCS34725_PERS_NONE = 0b0000
TCS34725_PERS_1_CYCLE = 0b0001
TCS34725_PERS_2_CYCLE = 0b0010
TCS34725_PERS_3_CYCLE = 0b0011
TCS34725_PERS_5_CYCLE = 0b0100
TCS34725_PERS_10_CYCLE = 0b0101
TCS34725_PERS_15_CYCLE = 0b0110
TCS34725_PERS_20_CYCLE = 0b0111
TCS34725_PERS_25_CYCLE = 0b1000
TCS34725_PERS_30_CYCLE = 0b1001
TCS34725_PERS_35_CYCLE = 0b1010
TCS34725_PERS_40_CYCLE = 0b1011
TCS34725_PERS_45_CYCLE = 0b1100
TCS34725_PERS_50_CYCLE = 0b1101
TCS34725_PERS_55_CYCLE = 0b1110
TCS34725_PERS_60_CYCLE = 0b1111

# Configuration register
TCS34725_CONFIG = 0x0D
TCS34725_CONFIG_WLONG = 0x02

# Gain level for the sensor
TCS34725_CONTROL = 0x0F

# Device ID
TCS34725_ID = 0x12

# Device status
TCS34725_STATUS = 0x13
TCS34725_STATUS_AINT = 0x10
TCS34725_STATUS_AVALID = 0x01

# Channel data registers
TCS34725_CDATAL = 0x14
TCS34725_CDATAH = 0x15
TCS34725_RDATAL = 0x16
TCS34725_RDATAH = 0x17
TCS34725_GDATAL = 0x18
TCS34725_GDATAH = 0x19
TCS34725_BDATAL = 0x1A
TCS34725_BDATAH = 0x1B

# Integration time settings
TCS34725_INTEGRATIONTIME_2_4MS = 0xFF
TCS34725_INTEGRATIONTIME_24MS = 0xF6
TCS34725_INTEGRATIONTIME_50MS = 0xEB
TCS34725_INTEGRATIONTIME_60MS = 0xE7
TCS34725_INTEGRATIONTIME_101MS = 0xD6
TCS34725_INTEGRATIONTIME_120MS = 0xCE
TCS34725_INTEGRATIONTIME_154MS = 0xC0
TCS34725_INTEGRATIONTIME_180MS = 0xB5
TCS34725_INTEGRATIONTIME_199MS = 0xAD
TCS34725_INTEGRATIONTIME_240MS = 0x9C
TCS34725_INTEGRATIONTIME_300MS = 0x83
TCS34725_INTEGRATIONTIME_360MS = 0x6A
TCS34725_INTEGRATIONTIME_401MS = 0x59
TCS34725_INTEGRATIONTIME_420MS = 0x51
TCS34725_INTEGRATIONTIME_480MS = 0x38
TCS34725_INTEGRATIONTIME_499MS = 0x30
TCS34725_INTEGRATIONTIME_540MS = 0x1F
TCS34725_INTEGRATIONTIME_600MS = 0x06
TCS34725_INTEGRATIONTIME_614MS = 0x00

TCS34725_GAIN_1X = 0x00
TCS34725_GAIN_4X = 0x01
TCS34725_GAIN_16X = 0x02
TCS34725_GAIN_60X = 0x03

class Adafruit_TCS34725:
    def __init__(self, i2c, addr=TCS34725_ADDRESS):
        self.i2c = i2c
        self.addr = addr
        self._tcs34725IntegrationTime = TCS34725_INTEGRATIONTIME_614MS
        self._tcs34725Gain = TCS34725_GAIN_4X
        self._tcs34725Initialised = False
    
    def write8(self, reg, value):
        self.i2c.writeto_mem(self.addr, TCS34725_COMMAND_BIT | reg, bytearray([value]))
    
    def read8(self, reg):
        return self.i2c.readfrom_mem(self.addr, TCS34725_COMMAND_BIT | reg, 1)[0]
    
    def read16(self, reg):
        data = self.i2c.readfrom_mem(self.addr, TCS34725_COMMAND_BIT | reg, 2)
        return (data[1] << 8) | data[0]
    
    def enable(self):
        self.write8(TCS34725_ENABLE, TCS34725_ENABLE_PON)
        time.sleep_ms(3)
        self.write8(TCS34725_ENABLE, TCS34725_ENABLE_PON | TCS34725_ENABLE_AEN)
        time.sleep_ms(int((256 - self._tcs34725IntegrationTime) * 12 / 5 + 1))
    
    def disable(self):
        reg = self.read8(TCS34725_ENABLE)
        self.write8(TCS34725_ENABLE, reg & ~(TCS34725_ENABLE_PON | TCS34725_ENABLE_AEN))
    
    def begin(self):
        print("Beginning initialization")
        self._tcs34725Initialised = True
        x = self.read8(TCS34725_ID)
        print(f"ID read: {x}")
        if x not in [0x4D, 0x44, 0x10]:
            print("Sensor ID mismatch")
            return False
        self.setIntegrationTime(self._tcs34725IntegrationTime)
        self.setGain(self._tcs34725Gain)
        self.enable()
        print("Initialization complete")
        return True

    
    def setIntegrationTime(self, it):
        print("Setting integration time:", it)
        if not self._tcs34725Initialised:
            print("Sensor not initialized, calling begin()")
            self.begin()
        print(f"Writing integration time {it} to register")
        self.write8(TCS34725_ATIME, it)
        self._tcs34725IntegrationTime = it
        print(f"Integration time set to {self._tcs34725IntegrationTime}")

    
    def setGain(self, gain):
        if not self._tcs34725Initialised:
            self.begin()
        self.write8(TCS34725_CONTROL, gain)
        self._tcs34725Gain = gain
    
    def setInterrupt(self, i):
        r = self.read8(TCS34725_ENABLE)
        if i:
            r |= TCS34725_ENABLE_AIEN
        else:
            r &= ~TCS34725_ENABLE_AIEN
        self.write8(TCS34725_ENABLE, r)
    
    def clearInterrupt(self):
        self.i2c.writeto(self.addr, bytearray([TCS34725_COMMAND_BIT | 0x66]))
    
    def setIntLimits(self, low, high):
        self.write8(0x04, low & 0xFF)
        self.write8(0x05, low >> 8)
        self.write8(0x06, high & 0xFF)
        self.write8(0x07, high >> 8)

    def getRGB(self):
        red, green, blue, clear = self.getRawData()
        sum = clear

        # Avoid divide by zero errors ... if clear = 0 return black
        if sum == 0:
            return 0.0, 0.0, 0.0

        r = float(red) / sum * 255.0
        g = float(green) / sum * 255.0
        b = float(blue) / sum * 255.0
        return r, g, b

    def getRawData(self): 
        if not self._tcs34725Initialised: 
            self.begin() 

        clear = self.read16(TCS34725_CDATAL)
        red = self.read16(TCS34725_RDATAL)
        green = self.read16(TCS34725_GDATAL)
        blue = self.read16(TCS34725_BDATAL)
        # Set a delay for the integration time
        time.sleep_ms((256 - self._tcs34725IntegrationTime) * 12 // 5 + 1)
        return red, green, blue, clear


def demo():
    print("Setup i2c")
    i2c = I2C(0, scl=Pin(5), sda=Pin(4))
    print("Create sensor")
    sensor = Adafruit_TCS34725(i2c)
    print("Begin")
    if not sensor.begin():
        print("Error")
    print("Begin completed")

    print("Enabling light")
    sensor.setInterrupt(False)

    print("Wait for module to settle")
    time.sleep_ms(200)

    print("Read RGB from module")
    red, green, blue = sensor.getRGB()

    sensor.setInterrupt(True)

    print(f"R: {red}, G: {green}, B: {blue}")




if __name__ == "__main__":
    demo()

# Example usage:
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# sensor = Adafruit_TCS34725(i2c)
# sensor.begin()
