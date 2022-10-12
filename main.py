import userinfo
import pydirectinput
from time import sleep
from mouse import click
from socket import socket
from random import randint
from keyboard import is_pressed
from threading import Thread
from pydirectinput import moveTo

message, user, direction, stop, cams, ran = ' ', ' ', 2, 1, 0, 0
ld, rd, ll, rl, cameras, boop = 0, 0, 0, 0, 0, 0
cam1a, cam1b, cam1c, cam2a, cam2b, cam3, cam4a, cam4b, cam5, cam6, cam7 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

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
# miscellaneous functions

def camera(cam, x, y):
    if cam == 1:
        moveTo(x, y)
        click('left')

def ActionChance(x,y):
    global ran
    if ran == 1:
        chance = randint(x,y)
        return chance
    else:
        chance = 4
        return chance

def control(com1, com2, x1, y1, x2, y2):
    if not com1 == 1 or not com2 == 0:
        return
    moveTo(x1, y1)
    sleep(0.44)
    click('left')
    moveTo(x2, y2)

def toggle(var, text, val, a, b):
    if var == a:
        print(text + ' disabled')
        sleep(val)
        return b
    else:
        print(text + ' enabled')
        sleep(val)
        return a

# -----------------------------------------------------------------------------------------------------------------------
# hotkeys

def hotkey():
    global direction, stop, cams, ran
    global ld, rd, ll, rl, cameras, boop
    global cam1a, cam1b, cam1c, cam2a, cam2b, cam3, cam4a, cam4b, cam5, cam6, cam7
    while True:

# ---------------------------------------------------------------------------
# toggle hotkeys

    # Left door toggle
        if is_pressed('1'):
            ld = toggle(ld, 'Left door', 0.2, 1, 0)

    # Right door toggle
        if is_pressed('2'):
            rd = toggle(rd, 'Right door', 0.2, 1, 0)

    # Left light toggle
        if is_pressed('3'):
            ll = toggle(ll, 'Left light', 0.2, 1, 0)

    # Right light toggle
        if is_pressed('4'):
            rl = toggle(rl, 'Right light', 0.2, 1, 0)

    # Camera toggle
        if is_pressed('5'):
            cameras = toggle(cameras, 'Cameras', 0.2, 1, 0)

    # Boop toggle
        if is_pressed('6'):
            boop = toggle(boop, 'Boop', 0.2, 1, 0)

    # Chance toggle
        if is_pressed('7'):
            ran = toggle(ran, 'Chance', 0.2, 1, 0)

    # command toggle
        if is_pressed('l'):
            stop = toggle(stop, 'Commands', 0.2, 0, 1)

    # reset
        if is_pressed('r'):
            cams, direction = 0, 2
            ld, rd, ll, rl, cameras, boop = 0, 0, 0, 0, 0, 0
            cam1a, cam1b, cam1c, cam2a, cam2b, cam3, cam4a, cam4b, cam5, cam6, cam7 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            print('reset')
            sleep(0.5)

    # test
        if is_pressed('t'):
            print("                    ")
            print("direction:" + str(direction))
            print("cams:"      + str(cams))
            print("chance:"    + str(ran))
            print("stop:"      + str(stop))
            print("--------------------")
            print("Ldoor:"   + str(ld))
            print("Rdoor:"   + str(rd))
            print("Llight:"  + str(ll))
            print("Rlight:"  + str(rl))
            print("cameras:" + str(cameras))
            print("boop:"    + str(boop))
            print("--------------------")
            print("cam1a:" + str(cam1a))
            print("cam1b:" + str(cam1b))
            print("cam1c:" + str(cam1c))
            print("cam2a:" + str(cam2a))
            print("cam2b:" + str(cam2b))
            print("cam3:"  + str(cam3))
            print("cam4a:" + str(cam4a))
            print("cam4b:" + str(cam4b))
            print("cam5:"  + str(cam5))
            print("cam6:"  + str(cam6))
            print("cam7:"  + str(cam7))
            print("                    ")
            sleep(0.5)

# -----------------------------------------------------------------------------------------------------------------------
# game control

def process_input(message):

    global user, direction, stop, cams, ran
    global ld, rd, ll, rl, cameras, boop
    global cam1a, cam1b, cam1c, cam2a, cam2b, cam3, cam4a, cam4b, cam5, cam6, cam7

# ---------------------------------------------------------------------------

    if user.lower() == 'blanana_m' or 'astralspiff':
        match message.lower():

        # toggle individual cameras
                case "t_cam1a":
                    cam1a = toggle(cam1a, 'Camera 1a', 0, 1, 0)

                case "t_cam1b":
                    cam1b = toggle(cam1b, 'Camera 1b', 0, 1, 0)

                case "t_cam1c":
                    cam1c = toggle(cam1c, 'Camera 1c', 0, 1, 0)

                case "t_cam2a":
                    cam2a = toggle(cam2a, 'Camera 2a', 0, 1, 0)

                case "t_cam2b":
                    cam2b = toggle(cam2b, 'Camera 2b', 0, 1, 0)

                case "t_cam3":
                    cam3  = toggle(cam3, 'Camera 3', 0, 1, 0)

                case "t_cam4a":
                    cam4a = toggle(cam4a, 'Camera 4a', 0, 1, 0)

                case "t_cam4b":
                    cam4b = toggle(cam4b, 'Camera 4b', 0, 1, 0)

                case "t_cam5":
                    cam5  = toggle(cam5, 'Camera 5', 0, 1, 0)

                case "t_cam6":
                    cam6  = toggle(cam6, 'Camera 6', 0, 1, 0)

                case "t_cam7":
                    cam7  = toggle(cam7, 'Camera 7', 0)

                case "e_cam_all":
                    cam1a, cam1b, cam1c, cam2a, cam2b, cam3, cam4a, cam4b, cam5, cam6, cam7 = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
                    print('all cams enabled')

                case "d_cam_all":
                    cam1a, cam1b, cam1c, cam2a, cam2b, cam3, cam4a, cam4b, cam5, cam6, cam7 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    print('all cams enabled')

# ---------------------------------------------------------------------------

    if stop == 0:
        match message.lower():

            # Left door
                case "ldoor":
                    if ActionChance(1,4) == 4:
                        direction = 1
                        control(ld, cams, 55,355, 3,455)

            # Right door
                case "rdoor":
                    if ActionChance(1,4) == 4:
                        direction = 2
                        control(rd, cams, 1210,350, 1278,455)

            # Left light
                case "llight":
                    if ActionChance(1,4) == 4:
                        direction = 1
                        control(ll, cams, 55,455, 3,455)

            # Right light
                case "rlight":
                    if ActionChance(1,4) == 4:
                        direction = 2
                        control(rl, cams, 1210,470, 1278,455)

            # general camera
                case "cams":
                    if not ActionChance(1,4) == 4 or not cameras == 1:
                        return
                    if cams == 0:
                        cams = 1
                        moveTo(550,606)
                        moveTo(562,700)
                        moveTo(550,606)
                        return
                    if cams == 1:
                        cams = 0
                        moveTo(550,606)
                        moveTo(562,667)
                        moveTo(550,606)
                        return

            # different cams
                case "cam1a":
                    if cam1a == 1:
                        camera(cams, 980,350)

                case "cam1b":
                    if cam1b == 1:
                        camera(cams, 980,400)

                case "cam1c":
                    if cam1c == 1:
                        camera(cams, 920,480)

                case "cam2a":
                    if cam2a == 1:
                        camera(cams, 980,600)

                case "cam2b":
                    if cam2b == 1:
                        camera(cams, 980,650)

                case "cam3":
                    if cam3 == 1:
                        camera(cams, 900,580)

                case "cam4a":
                    if cam4a == 1:
                        camera(cams, 1080,600)

                case "cam4b":
                    if cam4b == 1:
                        camera(cams, 1080,650)

                case "cam5":
                    if cam5 == 1:
                        camera(cams, 850,430)

                case "cam6":
                    if cam6 == 1:
                        camera(cams, 1200,570)

                case "cam7":
                    if cam7 == 1:
                        camera(cams, 1200,430)

            # boop Freddy's nose - "the most important control"
                case "boop":
                    if not ActionChance(1,4) == 4 or not boop == 1 or not direction == 1 or not cams == 0:
                        return
                    moveTo(679,236)
                    click('left')
                    print('boop!')
                    moveTo(3,455)

# -----------------------------------------------------------------------------------------------------------------------
# threading

Thread(target=twitch).start()
Thread(target=hotkey).start()