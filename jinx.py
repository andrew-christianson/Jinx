import io
import json
import math
import twitter
import time
import hashlib
import pdb

from jinx_auth import CONSUMER_KEY, CONSUMER_SECRET
from jinx_auth import OAUTH_TOKEN, OAUTH_TOKEN_SECRET 

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
stream = twitter.TwitterStream(auth=auth)
test = stream.statuses.sample()
count = 0
tweets_hash = []
tweets_list = []
uid = []
time_collected= []
EPSILON = 300 # seconds tweets must be within to count as contemporaneous
strip_index = None
print "Acquiring tweets_list"
start = time.time() 

for tweet in test:
	key = u'text' in tweet.keys()
	timeout = time.time() <= start + 1800
	if key and timeout and not tweet[u'text'][:2] == u'RT':
		digest = hashlib.sha1(tweet[u'text'].__repr__()).hexdigest()
		# print digest
		if digest in tweets_hash:
			index = tweets_hash.index(digest)
			print "Jinx! "+ str(tweet[u'user'][u'id']) + " owes ", 
			print str(uid[index]) + " a soda!"
			print "\t" + str(tweet[u'user'][u'id']) + " said: " + tweet[u'text']
			print "\t" + str(uid[index]) + " said: " + tweets_list[index]
		tweets_hash.append(digest)
		tweets_list.append(tweet[u'text'])
		uid.append(tweet[u'user'][u'id'])
		time_collected.append(time.time())
	elif not key:
		pass
	elif not timeout:
		break
	cutoff = time.time() - EPSILON
	try:
		strip_time = (x for x in time_collected if x < cutoff)
		strip_time = strip_time.next()
	except StopIteration:
		strip_time = None
	if strip_index is not None:
		print "Pruning Lists"
		tweets_list = tweets_list[strip_index:]
		tweets_hash = tweets_hash[strip_index:]
		uid = uid[strip_index:]
		time_collected = time_collected[strip_index:]

		