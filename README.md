This is a twitch bot that executes commands on your computer.\
Current features:\
mouse control, keyboard control, specifying the holding time in the message, display with last used command, toggleable Chance

The commands are toggled off at startup!\
Press L to toggle the commands
  
start the bot:
- make sure the libraries are installed
- add your user info to userinfo.py
- run main.py
  
add new keys:
- add the key definition to input_handler.py
- add the case
  
add new commands with time_value:
- add a new time_value limit to main.py (optional)
- add the command
  
with mouse movement:
- add a new time_value limit and pixel calculation to main.py (optional)
- add the command
  
without time_value:
- add the command to main.py
  
add new commands to stop:
- add the definition to input_handler.py

adjust the Chance:
- change the second value where the AnctionChance() function gets called in main.py
