'''
Kitronik Inventor's Kit Exp 9

Control a set of LEDs to show the charge in a capacitor.
'''
import machine
import time
import math

# Setup the pins controlling the LEDs with human-readable names
red = machine.Pin(14, machine.Pin.OUT)
orange = machine.Pin(15, machine.Pin.OUT)
yellow = machine.Pin(16, machine.Pin.OUT)
green = machine.Pin(17, machine.Pin.OUT)

pot = machine.ADC(26) # Setup the analogue (A0) on GP26 with a human-readable name

while True:
    # First read in the capacitor voltage
    capVoltage = pot.read_u16()
    
    # Do a quick conversion to percentage (65535/655.35 => 100% full scale)
    capPercent = math.trunc(capVoltage/655.35)
    
    # Now we decide which LEDs to turn on
    if ((capPercent > 25) and (capPercent <= 50)): # Red at 25% and up
        red.value(1)
    elif ((capPercent > 50) and (capPercent <= 75)): # Red and Orange at 50% and up
        red.value(1)
        orange.value(1)
    elif ((capPercent > 75) and (capPercent <= 90)): # Red, Orange and Yellow at 75% and up
        red.value(1)
        orange.value(1)
        yellow.value(1)
    elif (capPercent > 90): # All 4 when we get over 90%
        red.value(1)
        orange.value(1)
        yellow.value(1)
        green.value(1)
    else: # Must be below 25%, so turn off all the LEDs
        red.value(0)
        orange.value(0)
        yellow.value(0)
        green.value(0)