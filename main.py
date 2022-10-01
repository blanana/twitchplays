import time
import socket
import userinfo
import keyboard
import threading

from input_handler import InputHandler, InputKey, EventKind

global stop

message = ' '
user = ' '

stop = 1

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

def hotkey():
    while True:
        if keyboard.is_pressed('l'):
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

t1 = threading.Thread(target=twitch)
t2 = threading.Thread(target=hotkey)

t1.start()
t2.start()

# -----------------------------------------------------------------------------------------------------------------------

def process_input(message):

    message_parts = message.split(" ")

    try:
        command = message_parts[0].lower()
        time_value = float(message_parts[1])

        if time_value < 26 and time_value > 0:
            if stop == 0:
                match command:
                    case "right": input_handler.register_keypress(0, time_value, InputKey.RIGHT)
                    case "left":  input_handler.register_keypress(0, time_value, InputKey.LEFT)
                    case "up":    input_handler.register_keypress(0, time_value, InputKey.UP)
                    case "down":  input_handler.register_keypress(0, time_value, InputKey.DOWN)


    except (ValueError, IndexError):
        if stop == 0:
            match message.lower():
                case "jump":
                    input_handler.register_keypress(0, 0.1, InputKey.UP)

                case "jump right":
                    input_handler.register_keypress(0, 0.2, InputKey.RIGHT)
                    input_handler.register_keypress(0.1, 0.1, InputKey.UP)

                case "jump left":
                    input_handler.register_keypress(0, 0.2, InputKey.LEFT)
                    input_handler.register_keypress(0.1, 0.1, InputKey.UP)

                case "use":
                    input_handler.register_keypress(0, 0.3, InputKey.GRAB)

                case "hold":
                    input_handler.register_event(0, InputKey.GRAB, EventKind.PRESS)

                case "release":
                    input_handler.register_event(0, InputKey.GRAB, EventKind.RELEASE)

                case "enter":
                    input_handler.register_keypress(0, 0.2, InputKey.ENTER)
                    
                case "stop":
                    input_handler.stop_all()