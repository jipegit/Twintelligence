#
# Twintelligence
#
# Twintelligence is a free Twitter OSINT tool
#
# Author: @Jipe_ 
#

import twitter
from datetime import *
from flask import Flask, render_template, redirect, request

YOUR_APP_CONSUMER_KEY = ""
YOUR_APP_CONSUMER_SECRET = ""

YOUR_ACCESS_TOKEN = ""
YOUR_ACCESS_TOKEN_SECRET = ""

app = Flask(__name__)

class Data(object):
	def __init__(self, g, l, h):
		self.g = g
		self.l = l
		self.h = h

def getstatuses(twapi, userid, twnumber):
	""" Get the list of Tweets"""
	
	totalitems = 0
	items = None
	gpscoordinates = []
	langs = {}
	hours = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	maxid = 0

	print("[D] Retrieving the list of tweets (it might take a while...)")

	try:
		items = twapi.GetUserTimeline(user_id=userid, count=200)		#Can't request more than 200 items at a time
	except twitter.TwitterError as e:
		print(u"[-] ERROR: (" + e[0] + ")")
		return(Data(0,0,0))
		
	while len(items) > 0 and totalitems < twnumber:
		if maxid == items[-1].id:
			break
		maxid = items[-1].id
		for item in items:
			if totalitems >= twnumber:
				break
			
			if item.coordinates:
				gpscoordinates.append({'created_at' : item.created_at, 'lat' : item.coordinates['coordinates'][1], 'lng' : item.coordinates['coordinates'][0]})

			if item.lang in langs:
				langs[item.lang] += 1
			else:
				langs[item.lang] = 1
			
			hours[datetime.strptime(item.created_at, "%a %b %d %H:%M:%S +0000 %Y").hour] += 1
			
			totalitems += 1
			print("[D] [" + str(totalitems) + "] - "+ str(item.id) + " (" + item.created_at + ") - lang: " + item.lang + " added")
			#print(item)

		try:
			items = twapi.GetUserTimeline(user_id=userid, count=200, max_id=maxid)
		except twitter.TwitterError as e:
			print(u"[-] ERROR: (" + e[0] + ")")
			return(Data(0,0,0))

	print("[D] Got " + str(totalitems) + " tweets")
	
	print gpscoordinates
	
	langscountries = []
	langsnumbers = []
	langsdata = []

	for key in langs.keys():
		langscountries.append(key)
		langsnumbers.append(langs[key]) 
	
	langsdata.append(langscountries)
	langsdata.append(langsnumbers)

	return(Data(gpscoordinates, langsdata, hours))

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/contact")
def contact():
	return render_template("contact.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/report", methods=['GET', 'POST'])
def report():
	if request.method == 'POST':
		twapi = twitter.Api(consumer_key=YOUR_APP_CONSUMER_KEY,
						consumer_secret=YOUR_APP_CONSUMER_SECRET,
						access_token_key=YOUR_ACCESS_TOKEN,
	 					access_token_secret=YOUR_ACCESS_TOKEN_SECRET)
		
		userid = twapi.GetUser(screen_name=request.form['screen_name']).GetId()
		
		if request.form['nbtweets'] != "":
			nbtweets = int(request.form['nbtweets'])
			if nbtweets > 2000: nbtweets = 2000
		else:
			nbtweets = 1000
		
		print('[D] Trying to get [' + str(nbtweets) + '] tweets')

		userdetails = {}
		userdetails['screen_name'] = '@' + twapi.GetUser(userid).GetScreenName()
		userdetails['name'] = twapi.GetUser(userid).GetName()
		userdetails['created_at'] = twapi.GetUser(userid).GetCreatedAt()
		userdetails['location'] = twapi.GetUser(userid).GetLocation() 
		userdetails['utcoffset'] = str(twapi.GetUser(userid).GetUtcOffset())
		userdetails['tz'] = twapi.GetUser(userid).GetTimeZone()
		userdetails['lang'] = twapi.GetUser(userid).GetLang()
		userdetails['nbtweets'] = nbtweets
		
		print('[D] Trying to get the followers')
		followersid = twapi.GetFollowerIDs(user_id=userid)
		if len(followersid) <= 20:
			firstfollowersid = followersid
		else:
			firstfollowersid = followersid[-21:-1]

		#print('[D] Got ' + str(len(followers)) + ' followers')

		print('[D] Trying to get the friends')
		
		friendsid = twapi.GetFriendIDs(user_id=userid)
		if len(friendsid) <= 20:
			firstfriendsid = friendsid
		else:
			firstfriendsid = friendsid[-21:-1]

		firstfollowers = twapi.UsersLookup(user_id=firstfollowersid)
		firstfriends = twapi.UsersLookup(user_id=firstfriendsid)

		userdetails['firstfollowers'] = [ x.screen_name for x in firstfollowers]
		userdetails['firstfriends'] = [ x.screen_name for x in firstfriends]

		print userdetails['firstfollowers'] 
		print userdetails['firstfriends']

		# print('[D] Joined Friends/Followers')
		# for f in fff:
		# 	print('[D] ' + f.screen_name)

		print('[D] Trying to get [' + str(nbtweets) + '] tweets')
		returneddata = getstatuses(twapi, userid, nbtweets)

		return render_template("report.html",
			userdetails = userdetails,
			gpsdata = returneddata.g,
			langsbarchartdata = returneddata.l,
			hoursbarchartdata = returneddata.h)
	else:
		return redirect("/")

if __name__ == "__main__":
	app.run(debug=True)
