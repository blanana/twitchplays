import time
import mouse
import socket
import random
import userinfo
import keyboard
import threading
import pyautogui
import pydirectinput

global message

global direction
global stop
global cams

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

message = ' '
user = ' '

direction = 0
stop = 1
cams = 0

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

def camera(cam, x, y):
    if cam == 1:
        pydirectinput.moveTo(x, y)
        mouse.click('left')

    if cam == 0:
        return

def ActionChance(x,y):
    chance = random.randint(x,y)
    return chance

# ---------------------------------------------------------------------------

def please_stop():
    global stop
    if stop == 0:
        stop = 1
        print('commmands diabled')
        time.sleep(0.2)
        return

    if stop == 1:
        stop = 0
        print('commmands enabled')
        time.sleep(0.2)
        return

# -----------------------------------------------------------------------------------------------------------------------
# hotkeys

def hotkey():
    global direction
    global stop
    global cams

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

# ---------------------------------------------------------------------------
# toggle hotkeys
    # Left door toggle
        if keyboard.is_pressed('1'):
            if Ldoor == 1:
                Ldoor = 0
                print('Left door disabled')
                time.sleep(0.2)
            else:
                Ldoor = 1
                print('Left door enabled')
                time.sleep(0.2)

    # Right door toggle
        if keyboard.is_pressed('2'):
            if Rdoor == 1:
                Rdoor = 0
                print('Right door disabled')
                time.sleep(0.2)
            else:
                Rdoor = 1
                print('Right door enabled')
                time.sleep(0.2)

    # Left light toggle
        if keyboard.is_pressed('3'):
            if Llight == 1:
                Llight = 0
                print('Left light disabled')
                time.sleep(0.2)
            else:
                Llight = 1
                print('Left light enabled')
                time.sleep(0.2)

    # Right light toggle
        if keyboard.is_pressed('4'):
            if Rlight == 1:
                Rlight = 0
                print('Right light disabled')
                time.sleep(0.2)
            else:
                Rlight = 1
                print('Right light enabled')
                time.sleep(0.2)

    # Camera toggle
        if keyboard.is_pressed('5'):
            if cameras == 1:
                cameras = 0
                print('Cameras diabled')
                time.sleep(0.2)
            else:
                cameras = 1
                print('Cameras enabled')
                time.sleep(0.2)

    # Boop toggle
        if keyboard.is_pressed('6'):
            if boop == 1:
                boop = 0
                print('Boop disabled (How could you?)')
                time.sleep(0.2)
            else:
                boop = 1
                print('Boop enabled (boop)')
                time.sleep(0.2)


    # command toggle
        if keyboard.is_pressed('l'):
            please_stop()
# ---------------------------------------------------------------------------
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

    # test
        if keyboard.is_pressed('t'):
            print("                    ")
            print("direction:" + str(direction))
            print("cams:" + str(cams))
            print("stop:" + str(stop))
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
            print("--------------------")
            print(pyautogui.position())
            print("                    ")
            time.sleep(0.5)

# -----------------------------------------------------------------------------------------------------------------------
# threading

t1 = threading.Thread(target=twitch)
t2 = threading.Thread(target=hotkey)

t1.start()
t2.start()

# -----------------------------------------------------------------------------------------------------------------------
# game control

def process_input(message):

    global user

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

# ---------------------------------------------------------------------------

    if user.lower() == 'blanana_m' or 'astralspiff':
        match message:

        # toggle individual cameras
                case "s_start":
                    if cam1a == 1:
                        cam1a = 0
                        print('start disabled')
                    else:
                        cam1a = 1
                        print('start enabled')

                case "s_cam1b":
                    if cam1b == 1:
                        cam1b = 0
                        print('cam1b disabled')
                    else:
                        cam1b = 1
                        print('cam1b enabled')

                case "s_foxy":
                    if cam1c == 1:
                        cam1c = 0
                        print('foxy disabled')
                    else:
                        cam1c = 1
                        print('foxy enabled')

                case "s_cam2a":
                    if cam2a == 1:
                        cam2a = 0
                        print('cam2a disabled')
                    else:
                        cam2a = 1
                        print('cam2a enabled')

                case "s_cam2b":
                    if cam2b == 1:
                        cam2b = 0
                        print('cam2b disabled')
                    else:
                        cam2b = 1
                        print('cam2b enabled')

                case "s_cam3":
                    if cam3 == 1:
                        cam3 = 0
                        print('cam3 disabled')
                    else:
                        cam3 = 1
                        print('cam3 enabled')

                case "s_cam4a":
                    if cam4a == 1:
                        cam4a = 0
                        print('cam4a disabled')
                    else:
                        cam4a = 1
                        print('cam4a enabled')

                case "s_cam4b":
                    if cam4b == 1:
                        cam4b = 0
                        print('cam4b disabled')
                    else:
                        cam4b = 1
                        print('cam4b enabled')

                case "s_cam5":
                    if cam5 == 1:
                        cam5 = 0
                        print('cam5 disabled')
                    else:
                        cam5 = 1
                        print('cam5 enabled')

                case "s_cam6":
                    if cam6 == 1:
                        cam6 = 0
                        print('cam6 disabled')
                    else:
                        cam6 = 1
                        print('cam6 enabled')

                case "s_cam7":
                    if cam7 == 1:
                        cam7 = 0
                        print('cam7 disabled')
                    else:
                        cam7 = 1
                        print('cam7 enabled')


                case "s_cam_all":
                    if cam1a == 1 or cam1b == 1 or cam1c == 1 or cam2a == 1 or cam2b ==1 or cam3 == 1 or cam4a == 1 or cam5 == 1 or cam6 == 1 or cam7 == 1:
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
                        print('all cams disabled')

                    else:
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

# ---------------------------------------------------------------------------

    if stop == 0:
        match message.lower():

            # Left door
                case "ldoor":
                    if ActionChance(1,4) == 4:
                        if Ldoor == 1:
                            if cams == 0:
                                direction = 1
                                pydirectinput.moveTo(55, 355)
                                time.sleep(0.44)
                                mouse.click('left')
                                pydirectinput.moveTo(3, 455)
                            if cams == 1:
                                return

                        if Ldoor == 0:
                            return

            # Right door
                case "rdoor":
                    if ActionChance(1,4) == 4:
                        if Rdoor == 1:
                            if cams == 0:
                                direction = 2
                                pydirectinput.moveTo(1210, 350)
                                time.sleep(0.44)
                                mouse.click('left')
                                pydirectinput.moveTo(1278, 455)
                            if cams == 1:
                                return
                        
                        if Rdoor == 0:
                            return

# ---------------------------------------------------------------------------

            # Left light
                case "llight":
                    if ActionChance(1,4) == 4:
                        if Llight == 1:
                            if cams == 0:
                                direction = 1
                                pydirectinput.moveTo(55, 455)
                                time.sleep(0.44)
                                mouse.click('left')
                                pydirectinput.moveTo(3, 455)
                            if cams == 1:
                                return

                        if Llight == 0:
                            return

            # Right light
                case "rlight":
                    if ActionChance(1,4) == 4:
                        if Rlight == 1:
                            if cams == 0:
                                direction = 2
                                pydirectinput.moveTo(1210, 470)
                                time.sleep(0.44)
                                mouse.click('left')
                                pydirectinput.moveTo(1278, 455)
                            if cams == 1:
                                return
                        
                        if Rlight == 0:
                            return

# ---------------------------------------------------------------------------

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
                                return

                            if cams == 1:
                                cams = 0
                                pydirectinput.moveTo(550, 606)
                                time.sleep(0.1)
                                pydirectinput.moveTo(562, 667)
                                time.sleep(0.1)
                                pydirectinput.moveTo(550, 606)
                                return

                        if cameras == 0:
                            return

            # different cams
                case "start":
                    if cam1a == 1:
                        camera(cams, 980,350)

                case "cam1b":
                    if cam1b == 1:
                        camera(cams, 980,400)

                case "foxy":
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

# ---------------------------------------------------------------------------

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

                                    if cams == 1:
                                        return

                                if direction == 2:
                                    return
                        
                        if boop == 0:
                            return