import userinfo
import keyboard
import pydirectinput
from time import sleep
from socket import socket
from mouse import click, press, release
from random import randint
from keyboard import is_pressed
from threading import Thread
from pydirectinput import moveTo

message, user = ' ', ' '

#       direction, stop, camera, ran, mask, music box
main = [        2,    1,      0,   0,    0,         0]

#           Llight, Rlight, Light, Cameras, boop, mask
controls = [     0,      0,     0,       0,    0,    0]

#          cam1, cam2, cam3, cam4, cam5, cam6, cam7, cam8, cam9, cam10, cam11, cam12
cameras = [   0,    0,    0,    0,    0,    0,    0,    0,    0,     0,     0,     0]

pydirectinput.FAILSAFE = False

# -----------------------------------------------------------------------------------------------------------------------

SERVER = "irc.twitch.tv"
PORT = 6667
PASS = userinfo.PASS
BOT = userinfo.BOT
CHANNEL = userinfo.CHANNEL
OWNER = userinfo.OWNER
irc = socket()
irc.connect((SERVER, PORT))
irc.send(("PASS " + PASS + "\n" +
          "NICK " + BOT + "\n" +
          "JOIN #" + CHANNEL + "\n").encode())

# -----------------------------------------------------------------------------------------------------------------------
# twitch

def twitch():

    global user
    global message

    def joinchat():
        Loading = True
        while Loading:
            readbuffer_join = irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                Loading = loadingComplete(line)

    def loadingComplete(line):
        if ("End of /NAMES list" in line):
            return False
        else:
            return True
    global sendMessage

    def sendMessage(irc, message):
        messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
        irc.send((messageTemp + "\n").encode())

    def getUser(line):
        global user
        colons = line.count(":")
        colonless = colons-1
        separate = line.split(":", colons)
        user = separate[colonless].split("!", 1)[0]
        return user

    def getMessage(line):
        global message
        try:
            colons = line.count(":")
            message = (line.split(":", colons))[colons]
        except:
            message = ""
        return message

    def console(line):
        if "PRIVMSG" in line:
            return False
        else:
            return True
    while True:
        try:
            readbuffer = irc.recv(1024).decode()
        except:
            readbuffer = ""
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
            if "PING :tmi.twitch.tv" in line:
                msgg = "PONG :tmi.twitch.tv\r\n".encode()
                irc.send(msgg)
                continue
            else:
                global user
                user = getUser(line)
                message = getMessage(line)
                if user == "" or user == " ":
                    continue
                print(user.title() + " : " + message)
                process_input(message)

# -----------------------------------------------------------------------------------------------------------------------
# functions

def toggle(var, text, val, a, b):
    if var == a:
        print(text + ' disabled')
        sleep(val)
        return b
    else:
        print(text + ' enabled')
        sleep(val)
        return a

def ActionChance(x,y):
    if main[3] == 1:
        return randint(x,y)
    else:
        return 4

def control(com1, com2, x1, y1, x2, y2):
    if com1 == 1 and com2 == 0:
            moveTo(x1, y1)
            sleep(0.5)
            click('left')
            moveTo(x2, y2)

def camera(com1, com2, x1, y1):
    if com1 == 1 and com2 == 1:
        moveTo(x1, y1)
        click('left')

def cams(z, x, y, x1, y1):
    moveTo(x, y)
    moveTo(x1,y1)
    moveTo(x, y)
    return z

def hold(button, time):
    press(button)
    sleep(time)
    release(button)

# -----------------------------------------------------------------------------------------------------------------------
# hotkey

def hotkey():
    while True:

        if is_pressed('L'):
            main[1] = toggle(main[1], 'Commands', 0.2, 0, 1)

        if is_pressed('1'):
            controls[0] = toggle(controls[0], 'Left light', 0.2, 1, 0)
        if is_pressed('2'):
            controls[1] = toggle(controls[1], 'Right light', 0.2, 1, 0)
        if is_pressed('3'):
            controls[2] = toggle(controls[2], 'Main light', 0.2, 1, 0)
        if is_pressed('4'):
            controls[3] = toggle(controls[3], 'Cameras', 0.2, 1, 0)
        if is_pressed('5'):
            controls[4] = toggle(controls[4], 'boop', 0.2, 1, 0)
        if is_pressed('6'):
            controls[5] = toggle(controls[5], 'Mask', 0.2, 1, 0)
        if is_pressed('7'):
            main[3] = toggle(main[3], 'Chance', 0.2, 1, 0)

# -----------------------------------------------------------------------------------------------------------------------
# process input

def process_input(message):
    global cameras
    if user.lower() == 'blanana_m' or 'astralspiff':
        match str(message).lower():

            case "t_cam1":
                cameras[0]  = toggle(cameras[0], 'Camera 1', 0, 1, 0)
            case "t_cam2":
                cameras[1]  = toggle(cameras[0], 'Camera 2', 0, 1, 0)
            case "t_cam3":
                cameras[2]  = toggle(cameras[0], 'Camera 3', 0, 1, 0)
            case "t_cam4":
                cameras[3]  = toggle(cameras[0], 'Camera 4', 0, 1, 0)
            case "t_cam5":
                cameras[4]  = toggle(cameras[0], 'Camera 5', 0, 1, 0)
            case "t_cam6":
                cameras[5]  = toggle(cameras[0], 'Camera 6', 0, 1, 0)
            case "t_cam7":
                cameras[6]  = toggle(cameras[0], 'Camera 7', 0, 1, 0)
            case "t_cam8":
                cameras[7]  = toggle(cameras[0], 'Camera 8', 0, 1, 0)
            case "t_cam9":
                cameras[8]  = toggle(cameras[0], 'Camera 9', 0, 1, 0)
            case "t_cam10":
                cameras[9]  = toggle(cameras[0], 'Camera 10', 0, 1, 0)
            case "t_cam11":
                cameras[10] = toggle(cameras[0], 'Camera 11', 0, 1, 0)
            case "t_cam12":
                cameras[11] = toggle(cameras[0], 'Camera 12', 0, 1, 0)

            case "e_cam_all":
                cameras = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
                print('all cameras enabled')
            case "d_cam_all":
                cameras = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                print('all cameras disabled')

# -----------------------------------------------------------------------------------------------------------------------

    if main[1] == 0:
        match str(message).lower():

            case "llight":
                if ActionChance(1,4) == 4:
                    if main[2] == 0 and main[4] == 0 and controls[0] == 1:
                        if main[0] == 2:
                            moveTo(160, 426)
                            sleep(0.5)
                            hold('left', 0.2)
                            moveTo(160, 330)
                            main[0] = 1
                        else:
                            moveTo(160, 426)
                            hold('left', 0.2)
                            moveTo(160, 330)

            case "rlight":
                if ActionChance(1,4) == 4:
                    if main[2] == 0 and main[4] == 0 and controls[1] == 1:
                        if main[0] == 1:
                            moveTo(860, 426)
                            sleep(0.5)
                            hold('left', 0.2)
                            moveTo(860, 330)
                            main[0] = 2
                        else:
                            moveTo(860, 426)
                            hold('left', 0.2)
                            moveTo(860, 330)

            case "light":
                if ActionChance(1,4) == 4:
                    if main[4] == 0 and controls[2] == 1:
                        keyboard.press('Ctrl')
                        sleep(0.2)
                        keyboard.release('Ctrl')

            case "mask":
                if ActionChance(1,4) == 4:
                    if main[2] == 0 and controls[5] == 1:
                        if main[4] == 0:
                            moveTo(403, 650)
                            moveTo(403, 700)
                            moveTo(500, 400)
                            main[4] = 1
                        else:
                            moveTo(403, 650)
                            moveTo(403, 700)
                            moveTo(500, 400)
                            main[4] = 0

            case "cams":
                if ActionChance(1,4) == 4:
                    if main[4] == 0 and controls[3] == 1:
                        if main[2] == 0:
                            moveTo(577, 650)
                            moveTo(577, 700)
                            moveTo(500, 400)
                            main[2] = 1
                        else:
                            moveTo(577, 650)
                            moveTo(577, 700)
                            moveTo(500, 400)
                            main[2] = 0
            
            case "cam1":
                if ActionChance(1,4) == 4:
                    camera(cameras[0], main[2], 595, 555)
                    main[5] = 0
            case "cam2":
                if ActionChance(1,4) == 4:
                    camera(cameras[1], main[2], 732, 553)
                    main[5] = 0
            case "cam3":
                if ActionChance(1,4) == 4:
                    camera(cameras[2], main[2], 597, 486)
                    main[5] = 0
            case "cam4":
                if ActionChance(1,4) == 4:
                    camera(cameras[3], main[2], 733, 492)
                    main[5] = 0
            case "cam5":
                if ActionChance(1,4) == 4:
                    camera(cameras[4], main[2], 603, 650)
            case "cam6":
                if ActionChance(1,4) == 4:
                    camera(cameras[5], main[2], 724, 649)
                    main[5] = 0
            case "cam7":
                if ActionChance(1,4) == 4:
                    camera(cameras[6], main[2], 757, 431)
                    main[5] = 0
            case "cam8":
                if ActionChance(1,4) == 4:
                    camera(cameras[7], main[2], 602, 420)
                    main[5] = 0
            case "cam9":
                if ActionChance(1,4) == 4:
                    camera(cameras[8], main[2], 913, 391)
                    main[5] = 0
            case "cam10":
                if ActionChance(1,4) == 4:
                    camera(cameras[9], main[2], 845, 506)
                    main[5] = 0
            case "cam11":
                if ActionChance(1,4) == 4:
                    camera(cameras[10], main[2], 948, 462)
                    main[5] = 1
            case "cam12":
                if ActionChance(1,4) == 4:
                    camera(cameras[11], main[2], 934, 557)
                    main[5] = 0

            case "wind":
                if ActionChance(1,4) == 4:
                    if main[5] == 1:
                        moveTo(428, 593)
                        hold('left', 3)
                        moveTo(500, 400)

            case "boop":
                if ActionChance(1,4) == 4:
                    if main[2] == 0 and main[4] == 0:
                        if main[0] == 1:
                            moveTo(151, 162)
                            click()
                            moveTo(500, 400)
                        else:
                            moveTo(151, 162)
                            sleep(0.5)
                            click()
                            moveTo(500, 400)
                            main[0] = 1

# -----------------------------------------------------------------------------------------------------------------------
# threading

Thread(target=hotkey).start()
Thread(target=twitch).start()