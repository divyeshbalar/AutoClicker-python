##@Author Divyeshkumar Balar
##@Email Divyeshkumar_balar@outlook.com
##Base code is taken from https://github.com/isaychris
##

import pyautogui
import threading
import time
import sys
#from goto import goto, comefrom, label
from pynput.keyboard import *

#  ======== settings ========
delay = 10  # in seconds
delay2 = 30
resume_key = Key.f1
pause_key = Key.f2
reset_key = Key.f4
exit_key = Key.f3
#  ==========================

pause = True
running = True
reset_flag = False
inturrupt_flag = False

def on_press(key):
    global running, pause, reset_flag, inturrupt_flag

    if key == resume_key:
        #start or Resumed
        running = True
        pause = False
        reset_flag = False
        print("[Resumed]")
    elif key == pause_key:
        pause = True
        reset_flag = False
        print("[Paused]")
    elif key == exit_key:
        running = False
        inturrupt_flag = True
        print("[Exit]")
        sys.exit()
        # pause = True
        # reset_flag = False
    elif key == reset_key:
        reset_flag = True
        inturrupt_flag = True
        print("[RESET]")



def display_controls():
    print("// AutoClicker by iSayChris")
    print("// - Settings: ")
    print("\t first delay = " + str(delay) + ' sec and second delay =' + str(delay2) +'\n')
    print("// - Controls:")
    print("\t F1 = Resume")
    print("\t F2 = Pause")
    print("\t F3 = Exit")
    print("\t F4 = reset the cycle")
    print("-----------------------------------------------------")
    print("'Press F1 to start ...")

def checkIfIShouldInterruptSleep():
    return inturrupt_flag

def main():
    global running, pause, reset_flag, inturrupt_flag
    lis = Listener(on_press=on_press)
    display_controls()
    start_clicker(lis)

def start_clicker(lis):
    global running, pause, reset_flag, inturrupt_flag
    lis.start()
    while running:
        if not pause and reset_flag == False:
            #normally running F1
            temp = 0
            for i in range(delay):
                temp = i
                if checkIfIShouldInterruptSleep():
                     break
                time.sleep(1)
            print("Finished Sleeping1! for sec"+str(temp))
            if not inturrupt_flag:
                pyautogui.click(pyautogui.position())
            for i in range(delay2):
                if checkIfIShouldInterruptSleep():
                     break
                temp = i
                time.sleep(1)
            print("Finished Sleeping2! for sec"+str(temp))
            if not inturrupt_flag:
                pyautogui.click(pyautogui.position())

        elif not pause and reset_flag == True:
            #reset pressed in the middle of ongoing cycle
            temp = 0
            reset_flag = False
            inturrupt_flag = False
            #pyautogui.PAUSE = delay
            for i in range(delay):
                temp = i
                if checkIfIShouldInterruptSleep():
                     break
                time.sleep(1)
            print("Finished Sleeping!1 under reset for sec"+str(temp))
            if not inturrupt_flag:
                pyautogui.click(pyautogui.position())
            for i in range(delay2):
                temp = i
                if checkIfIShouldInterruptSleep():
                     break
                time.sleep(1)
            print("Finished Sleeping!2 under reset for sec"+str(temp))
            if not inturrupt_flag:
                pyautogui.click(pyautogui.position())
            lis.stop()
            lis1 = Listener(on_press=on_press)
            start_clicker(lis1)

        elif pause and reset_flag == True:
            #ongoing cycle is paused and reset button pressed
            lis.stop()
            pause = False
            reset_flag = False
            lis1 = Listener(on_press=on_press)
            start_clicker(lis1)

        elif pause and reset_flag == False:
            #Timer is paused and reset is NOT pressed(System is in idle condition)
            if running:
                ask = input("do you want to continueu?(y/n)")
                if ask == 'y' or ask == 'Y':
                    pause = False
                    reset_flag = False
                    running = True
                else:
                    running = False
                    pause = True
                    reset_flag = False
                    lis.stop();
            else:
                lis.stop();


if __name__ == '__main__':
    main()
