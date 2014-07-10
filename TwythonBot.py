## Twython Examples:
## First you need to install Twython:
## Installation
##
## pip install twython
## or, you can clone the repo and install it the old fashioned way
##
## git clone git://github.com/ryanmcgrath/twython.git
## cd twython
## sudo python setup.py install
##
## Twython makes use of the standard twitter API https://dev.twitter.com/docs/api/1.1
##
##
## This bot performs the following:
##	* Gets current Friends and Followers 
##	* Auto follows/prunes users
##	* Watches for Direct Messages
##  * Performs certian commands




from twython import Twython, TwythonError
from time import sleep
from os import system, name

############ BOT CONFIG SECTION ############

# You will need to generate API Keys at https://dev.twitter.com
# Make sure you enable Read / Write / Direct Messages access

consumer_key = "0cSu20Pr9qRqlrtl1mHLg"
consumer_secret = "WnrE5QQCp0tmYfFpEnYiN2DnQEwTnXybfu9cJA80c"
access_token = "148425198-Ls5NvKgwxxl1Ndw8PIZIsTpFaDENdCDibnFLIxQZ"
access_token_secret = "r8aIGHe6PcQO7AxicmvykQOJUK807G8UcMo60P598FU"

auto_follow = True  # Set to False if you do not want the bot to auto-follow back. If set to True, anyone could control your bot.
auto_prune = True  # Set to False if you do not want the bot to auto-unfollow users who unfollow it (not recommended)

CommandOneText = "Run command1"  # This is the command you want the bot to watch for. (Case insensitive)
CommandOne = "python /home/pi/command1.py"  # This is the external command you want the bot to run

CommandTwoText = "launch notepad"  # This is the other command you want the bot to watch for
CommandTwo = "notepad.exe"  # This is the other external command you want the bot to run



############ Example Functions ############
# See the full list of functions at:
# https://github.com/ryanmcgrath/twython/blob/master/twython/endpoints.py
# Compare it against the full Twitter API at: https://dev.twitter.com/docs/api/1.1

### Messaging Functions ####
def getdirectmessages(lastdm=0):  # Defines the "getdirectmessages" function.  Expects the input of the last DirectMessage ID we processed. (Not required)
	print "[+] Retrieving the last Direct Messages"
	dmsdict = twitter.get_direct_messages(since_id=lastdm)  # Returns results with an ID greater than (that is, more recent than) the specified ID in to a local dictionary
	dmsdict.reverse()  # Reverses the dictionary, so as we process it, we process the oldest command first.
	return dmsdict  # Returns the reversed dictionary to whatever called this function.


def senddirectmessage(user, message):  # Defines the "senddirectmessages" function.  Expects the input of the user we want to send to, and the message we want to send (both required)
	twitter.send_direct_message(user_id = user, text = message) 


def statusupdate(message):  # Defines the "statusupdate" function.  Expects the input of the message we want to tweet (required)
	twitter.update_status(status = message)


def imagestatus(imagepath, message = ""):  # Defines the "imagestatus" function.  Expects the local path to image you want to post, and message you want to tweet. (path required, message optional)
	photo = open(imagepath, 'rb')  # creates a variable "photo", and attempts to open the path passed in, in read only + binary modes.
	twitter.update_status_with_media(media=photo, status=message)


### Friends & Follwers Functions ###
def createfriendship(friend):  # Defines the "createfriendship" function.  Expects the input of the friendID of the person we want to follow (required)
	twitter.create_friendship(user_id=friend)


def destroyfriendship(friend):  # Defines the "destroyfriendship" function.  Expects the input of the friendID of the person we want to unfollow (required)
	twitter.destroy_friendship(user_id=friend)


def getfriendslist():
	print "[+] Retrieving our Friends List"
	'''This function uses the twitter api to get the full list of our friends. It will
	return a list that contains the Twitter IDs of our friends'''
	friends_IDs = []  # Create a List to hold friends TwitterIDs
	friends = twitter.get_friends_list()  # Call Twitter API to get full dictionary of Friends list
	for i in range(0, len(friends['users'])):  # Iterate through the first to last Friend
		friends_IDs.append(friends['users'][i]['id'])  # Populate list with Friend ID (NEVER USE SCREEN NAME!)
	friends_IDs.sort()  # resort the list in numerical order, so we can compare it against followers list later.
	return friends_IDs  # Returns the sorted list to whatever called this function.


def getfollowerslist():
	print "[+] Retrieving our Followers List"
	'''This function uses the twitter api to get the full list of our followers. It will
	return a list that contains the Twitter IDs of our folllowers'''
	follower_IDs = []  # Create a List to hold Followers TwitterIDs
	followers = twitter.get_followers_list()  # Call Twitter API to get full dictionary of Followers list
	for i in range(0, len(followers['users'])):  # Iterate through the first to last Friend
		follower_IDs.append(followers['users'][i]['id'])  # Populate list with Friend ID (NEVER USE SCREEN NAME!)
	follower_IDs.sort()  # resort the list in numerical order, so we can compare it against friends list later.
	return follower_IDs  # Returns the sorted list to whatever called this function.


### TwitterBot Functions ###
def autofollow(followernames, friendsnames):
	print "Running AutoFollow"
	'''This function will check for follers who we have not friended, and friend them.  It will also check our friend list
	for users who are not following us, then it will unfriend them.'''
	for follower in followernames:  # Iterate through all the followers in the list followernames (one at a time through the loop)
		if follower not in friendsnames and auto_follow is True:  # Check the friendsnames list to see if the follower is already a friend. Also make sure we want to autofollow
			print "   [+] Sir, I have found a nice person %s who needs to be followed" % follower
			createfriendship(follower)  # Call the createfriendship function, and pass it the current followerID that was not in friendsnames list.
			senddirectmessage(follower, "Welcome aboard, I await your command")  # Send that follower a direct message letting them know that we will now accept commands.

	for friend in friendsnames:  # Iterate through all the friends in the list friendsname (one at a time through the loop)
		if friend not in followernames and auto_prune is True:  # Check the followernames list to see if the friend isnt in there. Also make sure we want to autoprune
			print "   [+] Sir, I have found that '%s' needs to be un-followed" % friend
			destroyfriendship(friend)  # Call the destroyfriendship function, and pass it the current friendID that was not in followernames list.


def ProcessDirectMessages(lastdm):
	directmessages = getdirectmessages(lastdm)  # Assign the directmessages variable the output of the getdirectmessages function (what is returned)
	if len(directmessages) > 0:  # Make sure we have new direct messages
		for messages in directmessages:  # Iterate through all the messages in the direct messages dictionary (one at a time through the loop)
			lastdm = messages['id']  # Keep track of the last direct message we have processed. Because the list is reversed, we will work oldest to newest.
			print "   [-] New Direct Message Found [%s]" % lastdm
			CommandProcessing(messages['text'])  # Call the CommandProcessing function, and pass it the text of the Direct Message we are processing.
	return lastdm  # Return the ID of the last direct message that we processed to whatever called this function.


def CommandProcessing(command):
	print "Processing Command"
	'''This function will check the text passed in to see if it matches the prefined commands, and if so, will run the predefined commands.  This function uppercases everything
	so the commands are case insensitive.'''
	if command.upper() == CommandOneText.upper():  # Check the message passed to function, to see if it matches the predefined command text
		system(CommandOne)  # If it does, run the command.
	elif command.upper() == CommandTwoText.upper():  # Check the message passed to function, to see if it matches the predefined command text
		system(CommandTwo)  # If it does, run the command.
	else:  # If the command didnt match either one
		print "Did not understand command"


def header():
	''' This function just draws a super fancy header'''
	system(['clear', 'cls'][name == 'nt'])  # Use the system command clear, unless the system name is nt, then use cls
	print "#" * 30  # print 30 #s
	print "## SecKC Python Twitter Bot ##"
	print "#" * 30  # print 30 #s

################# MAIN PROGRAM LOOP #######################
twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)  # This authorize our bot, and will be our interface into the Twython functions
lastdm = 0  # This just initializies the lastdm variable.  "lastdm" keeps track of the last Direct Message we have processed.

while True:  # Main program loop, This will keep the bot running until there is an error or a Control+c
	try:  # Try to do this, if anything errors, go to the exception handler
		header()  # Call the header function
		followernames = getfollowerslist()  # Assign the variable followernames the output of the getfollowerslist function (it returns a list of follower IDs)
		friendsnames = getfriendslist()  # Assign the variable friendsnames the output of the getfriendslist function (it returns a list of friends IDs)
		lastdm = ProcessDirectMessages(lastdm)  # Assign the variable lastdm the output of the ProcessDirectMessages function (it returns the ID of the last DM we processed)

#################   Pruning User List  ################# 
		if followernames != friendsnames:  # Because we sort the followernames and friendsnames lists, if they are not the same, then we need to autofollow/autoprune
			print "User discrepency found, investigating..."
			autofollow(followernames, friendsnames)  # Call the autofollow function, passing it the sorted followernames & friendsnames lists
		else:  # If followernames & friendsnames are the same, then we dont need to do anything
			print "It looks like everything is fine, lets hang out for a bit"
			sleep(30)  # Sleep for 30 seconds.  We do this because Twitter is pretty sensitive about how often we make API calls.
	except Exception, e:  # Exception handler
		print "_" * 80  # Print 80 _s
		print "ERROR: %s" % e  # Print the error that occurred
		sleep(60)  # And sleep for 60 seconds
		continue  # This is a terrible idea, because this restarts the program loop, no matter what error we had.