'''
Kitronik Inventor's Kit Exp 3
Switch on and off an LED via an interrupt, and change its brightness in relation to a variable resistor input.

A switch is connected to 3V3 Out and GP15. 
This triggers an interrupt on the falling edge (i.e. when it has been pressed and released).
The interrupt toggles a variable which is used to turn on or off the PWM output on GP16.

The LED brightness is controlled by PWM on GP16. The variable resistor is read into Analogue input A0,
and its value is transferred to the PWM output.
'''
import machine

switchInput = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN) # Setup GP15 as the button input pin
LED = machine.PWM(machine.Pin(16)) # Setup GP16 as the LED pin with a PWM output
pot = machine.ADC(26) # Setup the analogue (A0) on GP26 with a human-readable name

buttonState = False # This variable tracks the button clicks.

# This is the interrupt routine that is attached to GP15 and triggers when the button is released.
def switch_IRQHandler(pin):
    global buttonState
    buttonState = not(buttonState)

# Attach the interrupt routine to the switch input
switchInput.irq(trigger=machine.Pin.IRQ_FALLING, handler=switch_IRQHandler)

while True:
    potValue = pot.read_u16() # This variable reads the voltage that the potentiometer is adjusted to
    # Now decide what to do.
    if (buttonState): # Then we want to turn on the LED
        LED.duty_u16(potValue) # Turn the LED on to the value of the potentiometer
    else:
        LED.duty_u16(0) # Turn the LED off