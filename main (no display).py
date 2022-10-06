import time
import socket
import random
import userinfo
import keyboard
import threading

from input_handler import InputHandler, InputKey, EventKind

message = ' '
user = ' '
stop = 1
ran = 0
limit = 25

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

input_handler = InputHandler()
input_handler.run()

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

def toggle(var, text, val, a, b):
    if var == a:
        print(text + ' disabled')
        time.sleep(val)
        return b
    else:
        print(text + ' enabled')
        time.sleep(val)
        return a

def ActionChance(x,y):
    global ran
    if ran == 1:
        chance = random.randint(x,y)
        return chance
    else:
        chance = 4
        return chance

# -----------------------------------------------------------------------------------------------------------------------

def hotkey():
    global stop
    global ran
    while True:
        if keyboard.is_pressed('l'):
            stop = toggle(stop, "Commands", 0.2, 0, 1)

        if keyboard.is_pressed('7'):
            ran = toggle(ran, "Chance", 0.2, 1, 0)

# -----------------------------------------------------------------------------------------------------------------------

def process_input(message):

    global limit
    message_parts = message.split(" ")

    try:
        command = message_parts[0].lower()
        time_value = float(message_parts[1])

        if user.lower() == 'blanana_m' or 'astralspiff':
            match command:
                case "set_limit":
                    limit = time_value
                    print('limit = ' + str(limit))


        if time_value <= limit  and time_value > 0:
            if stop == 0:
                match command:
                    case "right":
                        if ActionChance(1,4) == 4:
                            input_handler.register_keypress(0, time_value, InputKey.RIGHT)

                    case "left":
                        if ActionChance(1,4) == 4:
                            input_handler.register_keypress(0, time_value, InputKey.LEFT)

                    case "up":
                        if ActionChance(1,4) == 4:
                            input_handler.register_keypress(0, time_value, InputKey.UP)

                    case "down":
                        if ActionChance(1,4) == 4:
                            input_handler.register_keypress(0, time_value, InputKey.DOWN)


    except (ValueError, IndexError):
        if stop == 0:
            match message.lower():
                case "jump":
                    if ActionChance(1,4) == 4:
                        input_handler.register_keypress(0, 0.1, InputKey.UP)

                case "jump right":
                    if ActionChance(1,4) == 4:
                        input_handler.register_keypress(0, 0.2, InputKey.RIGHT)
                        input_handler.register_keypress(0.1, 0.1, InputKey.UP)

                case "jump left":
                    if ActionChance(1,4) == 4:
                        input_handler.register_keypress(0, 0.2, InputKey.LEFT)
                        input_handler.register_keypress(0.1, 0.1, InputKey.UP)

                case "use":
                    if ActionChance(1,4) == 4:
                        input_handler.register_keypress(0, 0.3, InputKey.GRAB)

                case "hold":
                    if ActionChance(1,4) == 4:
                        input_handler.register_event(0, InputKey.GRAB, EventKind.PRESS)

                case "release":
                    if ActionChance(1,4) == 4:
                        input_handler.register_event(0, InputKey.GRAB, EventKind.RELEASE)

                case "enter":
                    if ActionChance(1,4) == 4:
                        input_handler.register_keypress(0, 0.2, InputKey.ENTER)
                    
                case "stop":
                    if ActionChance(1,4) == 4:
                        input_handler.stop_all()

# -----------------------------------------------------------------------------------------------------------------------

t1 = threading.Thread(target=twitch)
t2 = threading.Thread(target=hotkey)

t1.start()
t2.start()