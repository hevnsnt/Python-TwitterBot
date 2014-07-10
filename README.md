 Please note, I wrote a lot of it for someone who has never seen python before, so there is no need to point the fact that there is in-efficient use of functions.

What this bot does:

Connects to twitter over the Twitter 1.1 API
Monitors the bot's Friends and Follower list, and will autofollow any new followers, and auto un-follow any one that unfollows the bot.  This is needed for bi-directional communication. You can also disable this functionality in the config section if you would like a private use bot. (recommended)
Monitors for Direct Messages, for pre-defined commands.
In order for this to work "right out of the box", you will need to:

Install Python 2.7 if you are on windows (otherwise you are probably ok)
Install the Twython module (either with pip or install from source) Instructions are in the header of the bot code.  Please ask if you need any help here.
Create a new twitter account for your bot. Punny names like AlfredtheBotler are highly recommended. 
Create the API keys needed for the bot.  After the bot account is created, visit https://dev.twitter.com and login with the bot account.  Generate API keys, making sure to select Read, Write, and Direct Message access.
Update the bot with YOUR API keys.  It will not work without them.
Update the bot with the commands you want it to watch for:
Ex: CommandOneText = "Run command1
Changed to: CommandOneText = "Take a pic"
Update the bot with the commands you want it to run
Ex: CommandOne = "python /home/pi/command1.py"
Changed to: CommandOne = "raspistill –o image.jpg"
Please feel free to ask any questions, and please let me know if you get it running!
