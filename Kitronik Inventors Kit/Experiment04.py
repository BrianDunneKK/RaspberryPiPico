'''
Kitronik Inventor's Kit Exp 4

Control motor speed via PWM control of a transistor.

All the Pico pins have PWM capability - in this experiment GP15 is used.
This is used to control the base of a transistor which actually drives the motor.
'''
import machine
import time

motorControlPin = machine.PWM(machine.Pin(15)) # Setup GP15 as the pin controlling the transistor with a PWM output

while True: 
    # First ramp up the output value - this speeds up the motor
    for outputValue in range(0, 65536, 100):
        motorControlPin.duty_u16(outputValue)
        time.sleep_ms(5)
        
    # Pause at full speed for 1 second to make it more obvious we have got here
    time.sleep(1)
    # Now ramp down the output value - this slows the motor down
    for outputValue in range(65536, 0, -100):
        motorControlPin.duty_u16(outputValue)
        time.sleep_ms(5)
    
    # Pause at stop for 1 second to make it more obvious we have got here
    time.sleep(1)