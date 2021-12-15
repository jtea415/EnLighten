import time
import board
import neopixel
from random import *


"""
********************************************************************************
LEDLighting
********************************************************************************

LEDLighting class! Utilizes the neopixel Adafruit library to implement a
lighting effects manager for strings of LEDs driven by WS2811 LED driver
chips. This class supports LED strands of 1xN LEDS.

--------------------------------------------------------------------------------
The various effects offered are:
'Merica - Alternating static sequences of Red, White, and Blue
FourthOfJuly - Dynamic sequences of Red, White, and Blue
RGB - All LEDs light up with the selected RGB values
Christmas - Alternating sequence of Red and Green

TBD - Update this list!
--------------------------------------------------------------------------------

User must specify:

pin - port to which the LED strand is connected. The Raspberry Pi does not
support bitbanging on all pins, so this must be D10, D12, D18 or D21 to work.

numLeds - the number of LEDs in the strand. This will get defaulted to 30 if
unspecified
________________________________________________________________________________

Other constants that can be changed:

Order - The order in which the LED color values are specified. This is an
AdaFruit Neopixel library item. Can be RGB, GRB, RGBW, or GRBW. Default is
RGB.

Brightness - Speaks for itself. Specified as an intensity from 0 to 1. Default
is 0.2. Higher levels of brightness may require the LED strand to also be
connected to an external power supply. 

********************************************************************************
"""

# Constants:
ORDER = neopixel.GRB

Brightness = 0.5

class LEDLighting():
    
    """
    ****************************************************************************
    Constructor
    ----------------------------------------------------------------------------
    Initializes the NeoPixel LED strand and sets all LEDs to off
    ****************************************************************************
    """
    
    def __init__(self, pin, numLEDS):
        self.LEDS = neopixel.NeoPixel(
            pin, numLEDS, brightness=Brightness, auto_write=False, pixel_order=ORDER)

        self.Num_LEDS = numLEDS

        # Turn all LEDS off!
        self.LEDS.fill((0, 0, 0))
        self.LEDS.show()
            

    """
    ****************************************************************************
    Christmas
    ----------------------------------------------------------------------------
    LEDLighting settings that displays an alternating series of Green and Red.
    Static series does not change after being set.

    Arguments:
    
    SeriesWidth - Specifies the number of LEDs making up each color band in the
    Merica light pattern. i.e. If SeriesWidth = 3, than each iteration of the
    sequence will have 3 Green LEDs and 3 Red LEDs.
    Default value is 1
    ****************************************************************************
    """

    def Christmas(self, SeriesWidth = 1):
        for led in range(self.Num_LEDS):
            if (((((led+1)/SeriesWidth)%2) == 0) or
                ((((led+1)/SeriesWidth)%2) > 1)):                
                self.LEDS[led] = (255, 0, 0)
                
            elif ((led+1)/SeriesWidth)%2 > 0:                
                self.LEDS[led] = (0, 0, 255)

            else:
                self.LEDS[led] = (0, 0, 0)

        self.LEDS.show()


    """
    ****************************************************************************
    Merica
    ----------------------------------------------------------------------------
    LEDLighting settings that displays an alternating series of Red, White, and
    Blue. Static series does not change after being set.

    Arguments:
    
    SeriesWidth - Specifies the number of LEDs making up each color band in the
    Merica light pattern. i.e. If SeriesWidth = 3, than each iteration of the
    sequence will have 3 Red LEDs, 3 White LEDs, and 3 Blue LEDs.
    Default value is 1
    ****************************************************************************
    """

    def Merica(self, SeriesWidth = 1):
        for led in range(self.Num_LEDS):
            if (((((led+1)/SeriesWidth)%3) == 0) or
                ((((led+1)/SeriesWidth)%3) > 2)):                
                self.LEDS[led] = (0, 255, 0)
                
            elif ((led+1)/SeriesWidth)%3 > 1:                
                self.LEDS[led] = (255, 255, 255)
                
            elif ((led+1)/SeriesWidth)%3 > 0:                
                self.LEDS[led] = (255, 0, 0)

            else:
                self.LEDS[led] = (0, 0, 0)

        self.LEDS.show()
        

    def Hyperloop(self, Width = 1, cycles = 10):
        for i in range(cycles):
            for LED in range(self.Num_LEDS):
                self.LEDS[LED] = (255, 0, 255)

                if LED > 0:
                    self.LEDS[LED-1] = (0, 0, 0)
                if LED == 0:
                    self.LEDS[self.Num_LEDS - 1] = (0, 0, 0)
                self.LEDS.show()
                time.sleep(0.01)

    def Alternate(self, r1, b1, g1, r2, b2, g2, delayT):
        for LED in range(self.Num_LEDS):
            if (LED%2) == 1:
                self.LEDS[LED] = (r1, b1, g1)
        self.LEDS.show()
        time.sleep(delayT)
        
        self.LEDS.fill((0, 0, 0))
        self.LEDS.show()

        for LED in range(self.Num_LEDS):
            if (LED%2) == 0:
                self.LEDS[LED] = (r2, b2, g2)
        self.LEDS.show()
        time.sleep(delayT)
        
        self.LEDS.fill((0, 0, 0))
        self.LEDS.show()
        
            
    def SingleColor(self, r, b, g):
        self.LEDS.fill((r, b, g))       

        self.LEDS.show()

    def HyperRainbow(self, Width = 1, cycles = 10, cycleDelay = 1):
        
        for i in range(cycles):
            redFactor = 255
            blueFactor = 0
            greenFactor = 0
            for LED in range(int(self.Num_LEDS/3)):
                self.LEDS[LED] = (redFactor, blueFactor, greenFactor)                

                if redFactor - (255/(self.Num_LEDS/3)) < 0:  
                    redFactor = 0
                else:                    
                    redFactor -= int(255/(self.Num_LEDS/3))

                if greenFactor + (255/(self.Num_LEDS/3)) > 255:
                    greenFactor = 255
                else:                    
                    greenFactor += int(255/(self.Num_LEDS/3))                

                if LED > 0:
                    self.LEDS[LED-1] = (0, 0, 0)
                if LED == 0:
                    self.LEDS[self.Num_LEDS - 1] = (0, 0, 0)

                self.LEDS.show()
                
                time.sleep(cycleDelay)
        
            for LED in range(int(self.Num_LEDS/3), int(self.Num_LEDS*2/3)):
                self.LEDS[LED] = (redFactor, blueFactor, greenFactor)                

                if greenFactor - (255/(self.Num_LEDS/3)) < 0:  
                    greenFactor = 0
                else:                    
                    greenFactor -= int(255/(self.Num_LEDS/3))

                if blueFactor + (255/(self.Num_LEDS/3)) > 255:
                    blueFactor = 255
                else:                    
                    blueFactor += int(255/(self.Num_LEDS/3))                

                if LED > 0:
                    self.LEDS[LED-1] = (0, 0, 0)
                if LED == 0:
                    self.LEDS[self.Num_LEDS - 1] = (0, 0, 0)

                self.LEDS.show()
                
                time.sleep(cycleDelay)
                
            for LED in range(int(self.Num_LEDS*2/3), int(self.Num_LEDS)):
                self.LEDS[LED] = (redFactor, blueFactor, greenFactor)                

                if blueFactor - (255/(self.Num_LEDS/3)) < 0:  
                    blueFactor = 0
                else:                    
                    blueFactor -= int(255/(self.Num_LEDS/3))

                if redFactor + (255/(self.Num_LEDS/3)) > 255:
                    redFactor = 255
                else:                    
                    redFactor += int(255/(self.Num_LEDS/3))                

                if LED > 0:
                    self.LEDS[LED-1] = (0, 0, 0)
                if LED == 0:
                    self.LEDS[self.Num_LEDS - 1] = (0, 0, 0)

                self.LEDS.show()
                
                time.sleep(cycleDelay)


    def StaticRainbow(self, Width = 1, cycles = 10, cycleDelay = 1):
        
        for i in range(cycles):
            redFactor = 255
            blueFactor = 0
            greenFactor = 0
            for LED in range(int(self.Num_LEDS/3)):
                self.LEDS[LED] = (redFactor, blueFactor, greenFactor)                

                if redFactor - (255/(self.Num_LEDS/3)) < 0:  
                    redFactor = 0
                else:                    
                    redFactor -= int(255/(self.Num_LEDS/3))

                if greenFactor + (255/(self.Num_LEDS/3)) > 255:
                    greenFactor = 255
                else:                    
                    greenFactor += int(255/(self.Num_LEDS/3))                

                self.LEDS.show()
                

        
            for LED in range(int(self.Num_LEDS/3), int(self.Num_LEDS*2/3)):
                self.LEDS[LED] = (redFactor, blueFactor, greenFactor)                

                if greenFactor - (255/(self.Num_LEDS/3)) < 0:  
                    greenFactor = 0
                else:                    
                    greenFactor -= int(255/(self.Num_LEDS/3))

                if blueFactor + (255/(self.Num_LEDS/3)) > 255:
                    blueFactor = 255
                else:                    
                    blueFactor += int(255/(self.Num_LEDS/3))                

                self.LEDS.show()
                

                
            for LED in range(int(self.Num_LEDS*2/3), int(self.Num_LEDS)):
                self.LEDS[LED] = (redFactor, blueFactor, greenFactor)                

                if blueFactor - (255/(self.Num_LEDS/3)) < 0:  
                    blueFactor = 0
                else:                    
                    blueFactor -= int(255/(self.Num_LEDS/3))

                if redFactor + (255/(self.Num_LEDS/3)) > 255:
                    redFactor = 255
                else:                    
                    redFactor += int(255/(self.Num_LEDS/3))                

                self.LEDS.show()
                

    def Twinkle(self, red, green, blue, delay = 100, cycles = 10, width = 1):

        color = (red, blue, green)
        onLights = []
        
        self.LEDS.fill((0, 0, 0))

        for x in range(int(self.Num_LEDS/3)):
            startLED = randint(0, self.Num_LEDS - 1)
            
            self.LEDS[startLED] = color

            onLights.append(startLED)

        self.LEDS.show()

        for i in range(cycles):                   

            for t in range(width):
                
                onLED = randint(0, self.Num_LEDS - 1)

                if (onLED not in onLights):
                    onLights.append(onLED)
                    self.LEDS[onLED] = color
                    
            for j in range(width):
                
                if (len(onLights) > int(self.Num_LEDS/3)):
                    offNum = randint(0, len(onLights) - 1)
                    offLED = onLights[offNum]

                    self.LEDS[offLED] = (0, 0, 0)

                    del onLights[offNum]

            self.LEDS.show()

            time.sleep(delay)
            
            
       
