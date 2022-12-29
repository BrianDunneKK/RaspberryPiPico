'''
Kitronik Inventor's Kit Exp 10

Control a ZIP Stick (addressable RGB LEDs)
'''
import machine
import array
import time
from rp2 import PIO, StateMachine, asm_pio

numLEDs = 5 # Set the number of ZIP LEDs (5 on a ZIP Stick)

# Setup a PIO state machine to drive the ZIP LEDs       
@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ZIPLEDOutput():
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [2]
    jmp(not_x, "do_zero")   .side(1)    [1]
    jmp("bitloop")          .side(1)    [4]
    label("do_zero")
    nop()                   .side(0)    [4]
    wrap()
    
ZIPStick = StateMachine(0, ZIPLEDOutput, freq=8000000, sideset_base=machine.Pin(16)) # Create the state machine on GP16

ZIPStick.active(1) # Start the state machine, ready to receive data

LEDs = array.array("I", [0 for _ in range(numLEDs)]) # Create array containing all the ZIP LEDs - "I" at start to indicate 32-bit number, then all 0s

buttonR = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN) # Setup an input button on GP13 with a human-readable name
buttonG = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN) # Setup an input button on GP14 with a human-readable name
buttonB = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN) # Setup an input button on GP15 with a human-readable name

# Initial states for the buttons are all False
buttonRState = False
buttonGState = False
buttonBState = False

# Interrupt handlers the RGB control buttons
def buttonR_IRQHandler(pin):
    global buttonRState
    buttonRState = True
    
def buttonG_IRQHandler(pin):
    global buttonGState
    buttonGState = True
    
def buttonB_IRQHandler(pin):
    global buttonBState
    buttonBState = True
    
buttonR.irq(trigger=machine.Pin.IRQ_FALLING, handler=buttonR_IRQHandler)
buttonG.irq(trigger=machine.Pin.IRQ_FALLING, handler=buttonG_IRQHandler)
buttonB.irq(trigger=machine.Pin.IRQ_FALLING, handler=buttonB_IRQHandler)

# Set the initial colours to have the ZIP LEDs all off, i.e. all colours at 0
r = 0
g = 0
b = 0

# Loop which continually checks for colour setting changes and sends these to the ZIP LEDs
while True:
    # Change the colour setting for red - cycles back to 0 if 255 is reached
    if (buttonRState):
        if (r >= 255):
            r = 0
        else:
            r += 5
        buttonRState = False
        time.sleep_ms(100)
    
    # Change the colour setting for green - cycles back to 0 if 255 is reached
    if (buttonGState):
        if (g >= 255):
            g = 0
        else:
            g += 5
        buttonGState = False
        time.sleep_ms(100)
    
    # Change the colour setting for blue - cycles back to 0 if 255 is reached
    if (buttonBState):
        if (b >= 255):
            b = 0
        else:
            b += 5
        buttonBState = False
        time.sleep_ms(100)
    
    # Send the RGB colour settings to the ZIP LEDs
    for i in range(numLEDs):
        LEDs[i] = (g<<16) + (r<<8) + b # Order is GRB
    ZIPStick.put(LEDs, 8) # RGB is only 24 bits, so get rid of unnecessary 8 bits