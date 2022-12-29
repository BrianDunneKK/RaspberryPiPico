'''
Kitronik Inventor's Kit Exp 5

Control the angle of a servo from a variable resistor

We read the value of the input analog, then use the scale function to rescale it to a different range.
The input is 0 - 65535, the output is scaled from 0 to 180 degrees.
'''
import machine
import time
import math

servo = machine.PWM(machine.Pin(15)) # Setup GP15 as the pin controlling the servo with a PWM output
pot = machine.ADC(26) # Setup the analogue (A0) on GP26 with a human-readable name

servo.freq(50) # Servo pulses need to repeat every 20ms, which is a 50Hz frequency

# Convert a value proportionally from one range to another
def scale(value, fromMin, fromMax, toMin, toMax):
    return toMin + ((value - fromMin) * ((toMax - toMin) / (fromMax - fromMin)))

while True:
    potValue = pot.read_u16() # This variable reads the voltage that the potentiometer is adjusted to
    # Convert analogue input to correct pulse width for servo control (1638 = 0.5ms & 8192 = 2.5ms, this is standard for 0 to 180 degrees)
    scaledValue = scale(potValue, 0, 65535, 1638, 8192)
    servo.duty_u16(math.trunc(scaledValue)) # Turn the servo to the value indicated by the potentiometer
    time.sleep_ms(100)