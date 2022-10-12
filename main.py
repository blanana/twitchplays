import userinfo
import pydirectinput
from time import sleep
from socket import socket
from mouse import click
from random import randint
from keyboard import is_pressed
from threading import Thread
from pydirectinput import move
from input_handler import InputHandler, InputKey

message, user, stop, ran = ' ', ' ', 1, 0

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
    if ran == 1:
        chance = randint(x,y)
        return chance
    else:
        chance = 4
        return chance

# -----------------------------------------------------------------------------------------------------------------------
# hotkey

def hotkey():
    global stop, ran
    while True:
        if is_pressed('l'):
            stop = toggle(stop, "Commands", 0.2, 0, 1)
            input_handler.stop_all()
        if is_pressed('7'):
            ran = toggle(ran, "Chance", 0.2, 1, 0)
            
# -----------------------------------------------------------------------------------------------------------------------
# process input

def process_input(message):
    message_parts = message.split(" ")

    try:
        command = message_parts[0].lower()
        time_value = float(message_parts[1])

        if time_value <= 10 and time_value > 0:
            if stop == 0:
                match command:
                    case "w":
                        input_handler.register_keypress(0, time_value, InputKey.W)

                    case "a":
                        input_handler.register_keypress(0, time_value, InputKey.A)

                    case "s":
                        input_handler.register_keypress(0, time_value, InputKey.S)

                    case "d":
                        input_handler.register_keypress(0, time_value, InputKey.D)

                    case "run":
                        input_handler.register_keypress(0, time_value, InputKey.W)
                        input_handler.register_keypress(0, time_value, InputKey.SHIFT)


        if time_value <= 90 and time_value > 0:
            if stop == 0:
                pixels = int(time_value*(1520/360))
                match command:
                    case "right":
                        if ActionChance(1, 4) == 4:
                            move(pixels, None)

                    case "left":
                        if ActionChance(1, 4) == 4:
                            move(-pixels, None)

                    case "up":
                        if ActionChance(1, 4) == 4:   
                            move(None, -pixels)

                    case "down":
                        if ActionChance(1, 4) == 4:
                            move(None, pixels)


    except (ValueError, IndexError):
        if stop == 0:
            match message.lower():
                case "jump":
                    input_handler.register_keypress(0, 0.2, InputKey.SPACE)

                case "jump w":
                    input_handler.register_keypress(0, 0.7, InputKey.W)
                    input_handler.register_keypress(0.1, 0.2, InputKey.SPACE)

                case "use":
                    input_handler.register_keypress(0, 5, InputKey.E)

                case "call":
                    input_handler.register_keypress(0, 0.1, InputKey.Q)

                case "sneak":
                    input_handler.register_keypress(0, 0.1, InputKey.CTRL)
                    input_handler.register_keypress(5.1, 0.1, InputKey.CTRL)

                case "tab":
                    input_handler.register_keypress(0, 0.1, InputKey.TAB)

                case "1":
                    input_handler.register_keypress(0, 0.1, InputKey.ONE)

                case "2":
                    input_handler.register_keypress(0, 0.1, InputKey.TWO)

                case "3":
                    input_handler.register_keypress(0, 0.1, InputKey.THREE)

                case "click":
                    if ActionChance(1, 4) == 4:
                        click('left')

# -----------------------------------------------------------------------------------------------------------------------
# threading

Thread(target=twitch).start()
Thread(target=hotkey).start()

input_handler = InputHandler()
input_handler.run()