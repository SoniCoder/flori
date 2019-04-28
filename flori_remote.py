from time import sleep
import pigpio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

try:

    pi = pigpio.pi()

    ESC_GPIO = 13

    BASE_WIDTH = 1000
    MAX_WIDTH = 2000

    pi.set_servo_pulsewidth(ESC_GPIO, 2000)
    sleep(2)
    pi.set_servo_pulsewidth(ESC_GPIO, BASE_WIDTH)
    sleep(2)

    cur_width = BASE_WIDTH

    import sys, termios, tty, os, time
     
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
     
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
     
    button_delay = 0.00000
    WIDTH_DELTA = 10 

    while True:
        char = getch()
     
        if (char == "p"):
            print("Stop!")
            break
     
        if (char == "a"):
            print("Left pressed")
            time.sleep(button_delay)
     
        elif (char == "d"):
            print("Right pressed")
            time.sleep(button_delay)
     
        elif (char == "w"):
            if cur_width + WIDTH_DELTA > MAX_WIDTH:
                cur_width = MAX_WIDTH
                print("Warning: Reached BASE_WIDTH")
            else:
                cur_width += WIDTH_DELTA
                print("New width", cur_width)
            pi.set_servo_pulsewidth(ESC_GPIO, cur_width)
            time.sleep(button_delay)
     
        elif (char == "s"):
            print("Down pressed")
            if cur_width - WIDTH_DELTA >= BASE_WIDTH:
                cur_width -= 10
                print("New width", cur_width)
            else:
                cur_width = BASE_WIDTH
                print("Warning: Reached BASE_WIDTH")
            pi.set_servo_pulsewidth(ESC_GPIO, cur_width) 
            time.sleep(button_delay)
     
        elif (char == "1"):
            print("Number 1 pressed")
            pi.set_servo_pulsewidth(ESC_GPIO, BASE_WIDTH)
            cur_width = BASE_WIDTH
            time.sleep(button_delay)
finally:
    pi.set_servo_pulsewidth(ESC_GPIO, 0)
    pi.stop()
