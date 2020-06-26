import RPi.GPIO as GPIO
import os, datetime
# Sensors
LDR=1
TEMP=2
PIR=3

#LEDs for Light and Fan
LIGHT=4
FAN=5

#Status of Light and Fan
LIGHT_STATUS=False
FAN_STATUS=False

TEMP_MAXLIMIT=23 # Default Temp to 23 degrees
daily_light_time=datetime.time(18,00,00)# The lights to be switched on daily at 1800 hrs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LDR, GPIO.IN)
GPIO.setup(TEMP, GPIO.IN)
GPIO.setup(PIR, GPIO.IN)

GPIO.setup(LIGHT, GPIO.OUT)
GPIO.setup(FAN, GPIO.OUT)
try:

    while True:
        #Reading the values from all the sensors
        PIR_VALUE=GPIO.INPUT(PIR)
        LDR_VALUE=GPIO.INPUT(LDR)
        TEMP_VALUE=GPIO.INPUT(TEMP)
        current_time=datetime.datetime.now().time()

        if PIR_VALUE == 1:
            print("Human Motion Detected")
            #GPIO.OUTPUT(LIGHT, 1)
            if TEMP_VALUE > TEMP_MAXLIMIT:
                print('Room Temperature is more than 23 Degrees...So Fan is switched ON')
                GPIO.OUTPUT(FAN, 1)
                FAN_STATUS=True
            else:
                print('Room Temperature is less than 23 Degrees...So Fan is switched OFF')
                GPIO.OUTPUT(FAN, 0)
                FAN_STATUS=False
        else:
            print("Human Motion NOT Detected")
            GPIO.OUTPUT(FAN, 0)
            FAN_STATUS=False
            print("No Human so FAN is switched off")

        # LIGHTS are ON if the room is dark or the time is greater than 1800 hrs.
        if LDR_VALUE < 10 or current_time > daily_light_time:
            print("Either LDR value is less or current time is greater than 1800 Hrs...So LIGHT is ON")
            GPIO.OUTPUT(LIGHT, 1)
            LIGHT_STATUS=True
        else:
            print("LDR value is more AND current time is lesser than 1800 Hrs...So LIGHT is OFF")
            GPIO.OUTPUT(LIGHT, 0)
            LIGHT_STATUS=False
except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()  # cleanup all GPIO


