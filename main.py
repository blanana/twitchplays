import userinfo
import pydirectinput
from time import sleep
from mouse import click
from socket import socket
from random import randint
from keyboard import is_pressed
from threading import Thread
from pydirectinput import moveTo

message, user = ' ', ' '

#       direction, stop, camera, ran
main = [        2,    1,      0,   0]

#           Ldoor, Rdoor, Llight, Rlight, Cameras, boop
controls = [    0,     0,      0,      0,       0,    0]

#          cam1a, cam1b, cam1c, cam2a, cam2b, cam3, cam4a, cam4b, cam5, cam6, cam7
cameras = [    0,     0,     0,     0,     0,    0,     0,     0,    0,    0,    0]

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
# twitch connection

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
                global message
                user = getUser(line)
                message = getMessage(line)
                if user == "" or user == " ":
                    continue
                print(user.title() + " : " + message)
                process_input(message)

# -----------------------------------------------------------------------------------------------------------------------
# Functions

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
            sleep(0.44)
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

# -----------------------------------------------------------------------------------------------------------------------
# hotkeys

def hotkey():
    while True:

        if is_pressed('L'):
            main[1] = toggle(main[1], 'Commands', 0.2, 0, 1)

        if is_pressed('1'):
            controls[0] = toggle(controls[0], 'Left door', 0.2, 1, 0)

        if is_pressed('2'):
            controls[1] = toggle(controls[1], 'Right door', 0.2, 1, 0)

        if is_pressed('3'):
            controls[2] = toggle(controls[2], 'Left light', 0.2, 1, 0)

        if is_pressed('4'):
            controls[3] = toggle(controls[3], 'Right light', 0.2, 1, 0)

        if is_pressed('5'):
            controls[4] = toggle(controls[4], 'Cameras', 0.2, 1, 0)

        if is_pressed('6'):
            controls[5] = toggle(controls[5], 'boop', 0.2, 1, 0)

        if is_pressed('7'):
            main[3] = toggle(main[3], 'Chance', 0.2, 1, 0)

# -----------------------------------------------------------------------------------------------------------------------
# game control

def process_input(message):
    if user.lower() == 'blanana_m' or 'astralspiff':
        match str(message).lower():

            case "t_cam1a":
                cameras[0]  = toggle(cameras[0], 'Camera 1a', 0, 1, 0)

            case "t_cam1b":
                cameras[1]  = toggle(cameras[1], 'Camera 1b', 0, 1, 0)

            case "t_cam1c":
                cameras[2]  = toggle(cameras[2], 'Camera 1c', 0, 1, 0)

            case "t_cam2a":
                cameras[3]  = toggle(cameras[3], 'Camera 2a', 0, 1, 0)

            case "t_cam2b":
                cameras[4]  = toggle(cameras[4], 'Camera 2b', 0, 1, 0)

            case "t_cam3":
                cameras[5]  = toggle(cameras[5], 'Camera 3', 0, 1, 0)

            case "t_cam4a":
                cameras[6]  = toggle(cameras[6], 'Camera 4a', 0, 1, 0)

            case "t_cam4b":
                cameras[7]  = toggle(cameras[7], 'Camera 4b', 0, 1, 0)

            case "t_cam5":
                cameras[8]  = toggle(cameras[8], 'Camera 5', 0, 1, 0)
            
            case "t_cam6":
                cameras[9]  = toggle(cameras[9], 'Camera 6', 0, 1, 0)

            case "t_cam7":
                cameras[10] = toggle(cameras[10], 'Camera 7', 0, 1, 0)

            case "e_cam_all":
                cameras = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
                print('all cameras enabled')

            case "1_cam_all":
                cameras = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                print('all cameras disabled')

    if main[1] == 0:
        match str(message).lower():

                case "ldoor":
                    if ActionChance(1,4) == 4:
                        main[0] = 1
                        control(controls[0], main[2], 55, 355, 3, 455)

                case "rdoor":
                    if ActionChance(1,4) == 4:
                        main[0] = 2
                        control(controls[1], main[2], 1210, 350, 1278, 455)

                case "llight":
                    if ActionChance(1,4) == 4:
                        main[0] = 1
                        control(controls[2], main[2], 55, 455, 3, 455)

                case "rlight":
                    if ActionChance(1,4) == 4:
                        main[0] = 2
                        control(controls[3], main[2], 1210, 470, 1278, 455)


                case "cams":
                    if controls[4] == 1 and ActionChance(1,4) == 4:
                            if main[2] == 0:
                                main[2] = cams(1, 550, 606, 562, 700)
                                return
                            if main[2] == 1:
                                main[2] = cams(0, 550, 606, 562, 700)


                case "cam1a":
                    camera(cameras[0], main[3], 980, 350)

                case "cam1b":
                    camera(cameras[1], main[3], 980, 350)

                case "cam1c":
                    camera(cameras[2], main[3], 980, 350)

                case "cam2a":
                    camera(cameras[3], main[3], 980, 350)

                case "cam2b":
                    camera(cameras[4], main[3], 980, 350)

                case "cam3":
                    camera(cameras[5], main[3], 980, 350)

                case "cam4a":
                    camera(cameras[6], main[3], 980, 350)

                case "cam4b":
                    camera(cameras[7], main[3], 980, 350)

                case "cam5":
                    camera(cameras[8], main[3], 980, 350)

                case "cam6":
                    camera(cameras[9], main[3], 980, 350)

                case "cam7":
                    camera(cameras[10], main[3], 980, 350)


                case "boop":
                    if controls[5] == 1 and main[2] == 0 and ActionChance(1,4) == 4:
                        if main[0] == 1:
                            moveTo(679,236)
                            click('left')
                            moveTo(3,455)
                        if main[0] == 2:
                            moveTo(3,455)
                            sleep(0.44)
                            moveTo(679,236)
                            click('left')
                            moveTo(3,455)
                            main[0] = 1

# -----------------------------------------------------------------------------------------------------------------------
# threading

Thread(target=hotkey).start()
Thread(target=twitch).start()