'''
Kitronik Inventor's Kit Exp 8

Control a seven segment display to show how much 'power' is generated from a 'wind turbine'
'''
import machine
import time
import math

# Setup the pins controlling the individual 7-segment display segments
segA = machine.Pin(18, machine.Pin.OUT)
segB = machine.Pin(17, machine.Pin.OUT)
segC = machine.Pin(16, machine.Pin.OUT)
segD = machine.Pin(15, machine.Pin.OUT)
segE = machine.Pin(14, machine.Pin.OUT)
segF = machine.Pin(13, machine.Pin.OUT)
segG = machine.Pin(12, machine.Pin.OUT)

pins = [segA, segB, segC, segD, segE, segF, segG] # Store the segment pins in a list for easy access

turbine = machine.ADC(26) # Setup the analogue (A0) on GP26 with a human-readable name
 
''' 
This list of 10 numbers shows the states of the pins for the segments 
to display the appropriate number. This is used to simplify the code
later - we can index the list to display the correct number.
'''
# numbers = [zero, one, two, three, four, five, six, seven, eight, nine, clear display]
numbers = [[1,1,1,1,1,1,0], 
          [0,1,1,0,0,0,0], 
          [1,1,0,1,1,0,1], 
          [1,1,1,1,0,0,1], 
          [0,1,1,0,0,1,1], 
          [1,0,1,1,0,1,1], 
          [1,0,1,1,1,1,1], 
          [1,1,1,0,0,0,0], 
          [1,1,1,1,1,1,1], 
          [1,1,1,0,0,1,1], 
          [0,0,0,0,0,0,0]]

clearDisplay = 10 # The position in the numbers list of the clear display setup

# This function takes in which number should be displayed, and then selects the correct pin/segment setup from the numbers list to control the output pins
def displayNumber(numberToDisplay):
    pin = 0
    for segment in range (7):
        pins[pin].value(numbers[numberToDisplay][segment])
        pin += 1
    
    return numberToDisplay

# Convert a value proportionally from one range to another
def scale(value, fromMin, fromMax, toMin, toMax):
    return toMin + ((value - fromMin) * ((toMax - toMin) / (fromMax - fromMin)))

displayNumber(clearDisplay) # Make sure the display is off

while True:
    # First read in the generated voltage
    generatedValue = turbine.read_u16()
    # Now we scale it to a much smaller range, as we only have a single 0-9 display
    # The ADC input ranges from 0 to 65535, but due to the voltage divider in the circuit, the maximum seen will only ever be 40000
    displayValue = scale(generatedValue, 0, 40000, 0, 9)
    # And finally display it
    displayNumber(math.trunc(displayValue))
    
    # Add a small delay so that the number doesnt change to rapidly to read.
    time.sleep_ms(100)