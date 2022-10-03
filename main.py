import time
import mouse
import socket
import random
import userinfo
import keyboard
import threading
import pydirectinput
from tkinter import *

message = ' '
user = ' '

direction = 2
stop = 1
cams = 0
ran = 0

Ldoor   = 0
Rdoor   = 0
Llight  = 0
Rlight  = 0
cameras = 0
boop    = 0

cam1a = 0
cam1b = 0
cam1c = 0
cam2a = 0
cam2b = 0
cam3  = 0
cam4a = 0
cam4b = 0
cam5  = 0
cam6  = 0
cam7  = 0

# -----------------------------------------------------------------------------------------------------------------------

SERVER = "irc.twitch.tv"
PORT = 6667
PASS = userinfo.PASS
BOT = userinfo.BOT
CHANNEL = userinfo.CHANNEL
OWNER = userinfo.OWNER
irc = socket.socket()
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

def camera(cam, x, y, text):
    if cam == 1:
        pydirectinput.moveTo(x, y)
        mouse.click('left')
        text_stuff(text)

def ActionChance(x,y):
    global ran
    if ran == 1:
        chance = random.randint(x,y)
        return chance
    else:
        chance = 4
        return chance

def control(com1, com2, x1, y1, x2, y2):
    if com1 == 1:
        if com2 == 0:
            pydirectinput.moveTo(x1, y1)
            time.sleep(0.44)
            mouse.click('left')
            pydirectinput.moveTo(x2, y2)

def toggle(var, text, val, a, b):
    if var == a:
        print(text + ' disabled')
        time.sleep(val)
        return b
    else:
        print(text + ' enabled')
        time.sleep(val)
        return a

def display():
    global text
    root = Tk()
    text = Text(root, height=8)
    text.insert("1.0", "Soup")
    text.pack()
    root.mainloop()

def text_stuff(the, other):
    text.delete("0.0", "end")
    text.insert("1.0", the + ": " + other)

# -----------------------------------------------------------------------------------------------------------------------
# hotkeys

def hotkey():
    global direction
    global stop
    global cams
    global ran

    global Ldoor
    global Rdoor
    global Llight
    global Rlight
    global cameras
    global boop

    global cam1a
    global cam1b
    global cam1c
    global cam2a
    global cam2b
    global cam3
    global cam4a
    global cam4b
    global cam5
    global cam6
    global cam7

    while True:

    # Left door toggle
        if keyboard.is_pressed('1'):
            Ldoor = toggle(Ldoor, 'Left door', 0.2, 1, 0)

    # Right door toggle
        if keyboard.is_pressed('2'):
            Rdoor = toggle(Rdoor, 'Right door', 0.2, 1, 0)

    # Left light toggle
        if keyboard.is_pressed('3'):
            Llight = toggle(Llight, 'Left light', 0.2, 1, 0)

    # Right light toggle
        if keyboard.is_pressed('4'):
            Rlight = toggle(Rlight, 'Right light', 0.2, 1, 0)

    # Camera toggle
        if keyboard.is_pressed('5'):
            cameras = toggle(cameras, 'Cameras', 0.2, 1, 0)

    # Boop toggle
        if keyboard.is_pressed('6'):
            boop = toggle(boop, 'Boop', 0.2, 1, 0)

    # Chance toggle
        if keyboard.is_pressed('7'):
            ran = toggle(ran, 'Chance', 0.2, 1, 0)

    # command toggle
        if keyboard.is_pressed('l'):
            stop = toggle(stop, 'Commands', 0.2, 0, 1)

    # reset
        if keyboard.is_pressed('r'):
            cams = 0
            direction = 0
            Ldoor = 0
            Rdoor = 0
            Llight  = 0
            Rlight  = 0
            cameras = 0
            boop  = 0
            cam1a = 0
            cam1b = 0
            cam1c = 0
            cam2a = 0
            cam2b = 0
            cam3  = 0
            cam4a = 0
            cam4b = 0
            cam5  = 0
            cam6  = 0
            cam7  = 0
            print('reset')
            time.sleep(0.5)

    # testing
        if keyboard.is_pressed('t'):
            print("                    ")
            print("direction:" + str(direction))
            print("cams:"      + str(cams))
            print("chance:"    + str(ran))
            print("stop:"      + str(stop))
            print("--------------------")
            print("Ldoor:"   + str(Ldoor))
            print("Rdoor:"   + str(Rdoor))
            print("Llight:"  + str(Llight))
            print("Rlight:"  + str(Rlight))
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
            time.sleep(0.5)

# -----------------------------------------------------------------------------------------------------------------------
# game control

def process_input(message):

    global direction
    global cams
    global stop

    global Ldoor
    global Rdoor
    global Llight
    global Rlight
    global cameras
    global boop

    global cam1a
    global cam1b
    global cam1c
    global cam2a
    global cam2b
    global cam3
    global cam4a
    global cam4b
    global cam5
    global cam6
    global cam7

# streamer commands
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
                    cam1a = 1
                    cam1b = 1
                    cam1c = 1
                    cam2a = 1
                    cam2b = 1
                    cam3  = 1
                    cam4a = 1
                    cam4b = 1
                    cam5  = 1
                    cam6  = 1
                    cam7  = 1
                    print('all cams enabled')

                case "d_cam_all":
                    cam1a = 0
                    cam1b = 0
                    cam1c = 0
                    cam2a = 0
                    cam2b = 0
                    cam3  = 0
                    cam4a = 0
                    cam4b = 0
                    cam5  = 0
                    cam6  = 0
                    cam7  = 0
                    print('all cams enabled')

# viewer commands
    if stop == 0:
        match message.lower():

            # Left door
                case "ldoor":
                    if ActionChance(1,4) == 4:
                        direction = 1
                        control(Ldoor, cams,      55, 355,     3, 455)
                        text_stuff(user ,"Left door")

            # Right door
                case "rdoor":
                    if ActionChance(1,4) == 4:
                        direction = 2
                        control(Rdoor, cams,      1210, 350,   1278, 455)
                        text_stuff(user, "Right door")

            # Left light
                case "llight":
                    if ActionChance(1,4) == 4:
                        direction = 1
                        control(Llight, cams,     55, 455,     3, 455)
                        text_stuff(user, "Left Light")

            # Right light
                case "rlight":
                    if ActionChance(1,4) == 4:
                        direction = 2
                        control(Rlight, cams,     1210, 470,   1278, 455)
                        text_stuff(user, "Right Light")

            # general camera
                case "cams":
                    if ActionChance(1,4) == 4:
                        if cameras == 1:
                            if cams == 0:
                                cams = 1
                                pydirectinput.moveTo(550, 606)
                                time.sleep(0.1)
                                pydirectinput.moveTo(562, 700)
                                time.sleep(0.1)
                                pydirectinput.moveTo(550, 606)
                                text_stuff(user, "Cameras")
                                return

                            if cams == 1:
                                cams = 0
                                pydirectinput.moveTo(550, 606)
                                time.sleep(0.1)
                                pydirectinput.moveTo(562, 667)
                                time.sleep(0.1)
                                pydirectinput.moveTo(550, 606)
                                text_stuff(user, "Cameras")
                                return

            # different cams
                case "cam1a":
                    if cam1a == 1:
                        camera(cams, 980, 350, "Camera 1a")
                        text_stuff(user, "Camera 1a")

                case "cam1b":
                    if cam1b == 1:
                        camera(cams, 980, 400, "Camera 1b")
                        (user, "Camera 1b")

                case "cam1c":
                    if cam1c == 1:
                        camera(cams, 920, 480, "Camera 1c")
                        (user, "Camera 1c")

                case "cam2a":
                    if cam2a == 1:
                        camera(cams, 980, 600, "Camera 2a")
                        (user, "Camera 2a")

                case "cam2b":
                    if cam2b == 1:
                        camera(cams, 980, 650, "Camera 2b")
                        (user, "Camera 2b")

                case "cam3":
                    if cam3 == 1:
                        camera(cams, 900, 580, "Camera 3")
                        (user, "Camera 3")

                case "cam4a":
                    if cam4a == 1:
                        camera(cams, 1080, 600, "Camera 4a")
                        (user, "Camera 4a")

                case "cam4b":
                    if cam4b == 1:
                        camera(cams, 1080, 650, "Camera 4b")
                        (user, "Camera 4b")

                case "cam5":
                    if cam5 == 1:
                        camera(cams, 850, 430, "Camera 5")
                        (user, "Camera 5")

                case "cam6":
                    if cam6 == 1:
                        camera(cams, 1200, 570, "Camera 6")
                        (user, "Camera 6")

                case "cam7":
                    if cam7 == 1:
                        camera(cams, 1200, 430, "Camera 7")
                        (user, "Camera 7")

            # boop Freddy's nose - "the most important control"
                case "boop":
                    if ActionChance(1,4) == 4:
                        if boop == 1:
                            if direction == 1:
                                if cams == 0:
                                    pydirectinput.moveTo(679, 236)
                                    mouse.click('left')
                                    print('boop!')
                                    pydirectinput.moveTo(3, 455)
                                    text_stuff(user, "Boop!")

# -----------------------------------------------------------------------------------------------------------------------
# threading

t1 = threading.Thread(target=twitch)
t2 = threading.Thread(target=hotkey)
t3 = threading.Thread(target=display)

t1.start()
t2.start()
t3.start()