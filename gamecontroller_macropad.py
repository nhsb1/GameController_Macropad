#Macropad game controller for Windows 10


import pygame
from pygame.locals import *
import subprocess
import sys
import re
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume,ISimpleAudioVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def Convert(string):
    li = list(string.split(","))
    return li

def get_dpad_press(buttonEvent):
        button_press = Convert(buttonEvent)
        strAxis = button_press[2]
        strButtonPress = (button_press[3])
        strAxis = re.findall(r'[\d\.\d]+', strAxis)
        strButtonPress = re.findall(r'[\d\.\d]+', strButtonPress)
        return strAxis, strButtonPress
    
motion = [0, 0]

while True:

    pygame.init()
    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN:
                print("Something happened...")
        if event.type == JOYBUTTONUP:
            #This section detects non-Dpad button presses (A,B,X,Y,L,R,S/S,) and reports the "value" of the button (e.g. 1-9)
            buttonEvent = str(event)
            button_press = Convert(buttonEvent)
            strButtonPress= str(button_press[2])
            strButtonPress = int(''.join(filter(str.isdigit, strButtonPress)))
            print(strButtonPress)
            print(volume)
            if strButtonPress == 1: #1 = A
                print("MUTE!") 
                
                if volume.GetMute() ==0: 
                    volume.SetMute(1,None)
                else:
                    volume.SetMute(0, None)
            if strButtonPress == 9: #9 = Start
                subprocess.Popen("cmd.exe", creationflags=subprocess.CREATE_NEW_CONSOLE)

        if event.type == JOYAXISMOTION:
            #This section is where D-pad events occur (Up, Down, Left, Right)
            dpadEvent = str(event)
            lsAxis, lsButton = get_dpad_press(dpadEvent)
            #print(lsAxis[0], lsButton[0])
            strAxis = ""
            strDpadButton = ""
            for f in lsAxis:
                strAxis = strAxis + f
            
            for f in lsButton:
                strDpadButton = strDpadButton + f
            
            if strAxis == "1" and strDpadButton == "1.0":
                print("DOWN!")
            if strAxis == "1" and strDpadButton > "1.0":
                print("UP!")
            if strAxis == "0" and strDpadButton == "1.0":
                print("RIGHT!")
                sessions = AudioUtilities.GetAllSessions()
                for session in sessions:
                    currentVolumeDb = volume.GetMasterVolumeLevel()
                    try:
                        volume.SetMasterVolumeLevel(currentVolumeDb + 0.25, None)
                    except:
                        print("error")
                    
            if strAxis == "0" and strDpadButton > "1.0":
                print("LEFT!") 
                sessions = AudioUtilities.GetAllSessions()
                for session in sessions:
                    currentVolumeDb = volume.GetMasterVolumeLevel()
                    try:
                        volume.SetMasterVolumeLevel(currentVolumeDb - 0.25, None)
                    except:
                        print("error")
                                     
            if event.axis < 2:
                motion[event.axis] = event.value
        if event.type == JOYHATMOTION:
            print(event)
        if event.type == JOYDEVICEADDED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            for joystick in joysticks:
                print(joystick.get_name())
        if event.type == JOYDEVICEREMOVED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()