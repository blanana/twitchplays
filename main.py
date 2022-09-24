import time
import mouse
import socket
import userinfo
import keyboard
import threading
import pydirectinput

from input_handler import InputHandler, InputKey, EventKind

global special_char
global capital_char
global command_cooldown
global stop

command_cooldown = []
special_char = ['!', '@', "#", "$", "%", "^", "&", "*", "(", ")", "?", ]
capital_char = ['A', "B", 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

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

def fucking_stop():
    global stop
    if stop == 0:
        stop = 1
        print('diabled')
        return
            
    if stop == 1:
        stop = 0
        print('enabled')
        return

t1 = threading.Thread(target=twitch)
t1.start()

# -----------------------------------------------------------------------------------------------------------------------        

def process_input(message):

    message_parts = message.split(" ")

    if stop == 0:
        try:
            command = message_parts[0].lower()
            time_value = float(message_parts[1])

            if time_value < 11 and time_value > 0:
                match command:
                    case "w": input_handler.register_keypress(0, time_value, InputKey.W)
                    case "a": input_handler.register_keypress(0, time_value, InputKey.A)
                    case "s": input_handler.register_keypress(0, time_value, InputKey.S)
                    case "d": input_handler.register_keypress(0, time_value, InputKey.D)
                    case "run":
                        input_handler.register_keypress(0, time_value, InputKey.SHIFT)
                        input_handler.register_keypress(0, time_value, InputKey.W)


            if time_value < 361 and time_value > 0:
                pixels = int(time_value*(1520/360))
                match command:
                    case "right": pydirectinput.move(pixels, None)
                    case "left":  pydirectinput.move(-pixels, None)
                    case "up":    pydirectinput.move(None, -pixels)
                    case "down":  pydirectinput.move(None, pixels)



        except (ValueError, IndexError):
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
                    mouse.click('left')

                case "stop":
                    input_handler.stop_all()

# -----------------------------------------------------------------------------------------------------------------------   

while True:
    if keyboard.is_pressed('l'):
        fucking_stop()
        time.sleep(0.5)