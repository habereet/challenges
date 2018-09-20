from collections import namedtuple
import csv
import os

import tweepy

from config import CONSUMER_KEY, CONSUMER_SECRET
from config import ACCESS_TOKEN, ACCESS_SECRET

DEST_DIR = 'data'
EXT = 'csv'
NUM_TWEETS = 100

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

Tweet = namedtuple('Tweet', 'id_str created_at text')


class UserTweets(object):

    def __init__(self, handle, max_id=None):
        self.handle = handle
        self.max_id = max_id
        self.output_file = f'{DEST_DIR}/{self.handle}.{EXT}'
        self._tweets = list(self._get_tweets())
        #print(self._tweets)
        self._save_tweets()


    def _get_tweets(self):
        """Return several items of the same type (namedtuple) to the calling function (__init__ in this case).
        list(self._get_tweets()) aggregates these into a list to be stored in self._tweets
        For better explanation, uncomment lines 28, 43, and 77 then comment lines 29, 44, and 78
        Adding the following line will help as well, possibly:"""
        handles_tweets = api.user_timeline(self.handle, count=NUM_TWEETS, max_id=self.max_id)
        """I was receiving unicode errors when writing the text to a file.
        This appears to be an issues with Windows. I used an imperfect solution that just converts all unicode to ascii
        and ignores all errors.
        Source - https://stackoverflow.com/questions/3224268/python-unicode-encode-error
        """
        #return (number+1 for number in range(0,5))
        return (Tweet(current_tweet.id_str, current_tweet.created_at, current_tweet.text.encode('ascii', 'ignore').decode('ascii')) for current_tweet in handles_tweets)
        
    def _save_tweets(self):
        """I had to figure out why my file was including an extra line in between each line written by Python.
        It seems that, since I'm on Windows, an extra new line is added in some cases (only in csv.writer?).
        I resolved this by adding ", newline=''" in the open() command
        Source - https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row"""
        with open(self.output_file, 'w+', newline='') as tweet_file:
            """To pass the unit test, I used delimiter ',
            However, some tweets already have commas.
            This seems an odd delimiter so I prefer to use delimiter-'\t'"""
            #tweet_writer = csv.writer(tweet_file, delimiter=',')
            tweet_writer = csv.writer(tweet_file, delimiter='\t')
            tweet_writer.writerow(Tweet._fields)
            tweet_writer.writerows(self._tweets)
            #for count in range(0,len(self._tweets)):
            #    tweet_writer.writerow([self._tweets[count].id_str, self._tweets[count].created_at, self._tweets[count].text])


    def __len__(self):
        return len(self._tweets)


    def __getitem__(self, pos):
        return(self._tweets[pos])


if __name__ == "__main__":

    for handle in ('pybites', '_juliansequeira', 'bbelderbos'):
        print('--- {} ---'.format(handle))
        user = UserTweets(handle)
        for tw in user[:5]:
            #print(tw.text)
            print(tw)
        print()
