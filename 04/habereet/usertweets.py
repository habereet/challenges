from collections import namedtuple
import csv
import os

import tweepy

from config import CONSUMER_KEY, CONSUMER_SECRET
from config import ACCESS_TOKEN, ACCESS_SECRET

DEST_DIR = 'data'
EXT = 'csv'
NUM_TWEETS = 100

Tweet = namedtuple('Tweet', 'id_str created_at text')


class UserTweets(object):

    def __init__(self, handle, max_id=None):
        self.handle = handle
        self.max_id = max_id
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api = tweepy.API(auth)
        """Get handle and optional max_id.
        Use tweepy.OAuthHandler, set_access_token and tweepy.API
        to create api interface.
        Use _get_tweets() helper to get a list of tweets.
        Save the tweets as data/<handle>.csv"""
        # ...
        self._tweets = list(self._get_tweets())
        self._save_tweets()

    def _get_tweets(self):
        """Hint: use the user_timeline() method on the api you defined in init.
        See tweepy API reference: http://docs.tweepy.org/en/v3.5.0/api.html
        Use a list comprehension / generator to filter out fields
        id_str created_at text (optionally use namedtuple)"""
        handles_tweets = self.api.user_timeline(self.handle, count=NUM_TWEETS, max_id=self.max_id)
        Tweet = namedtuple('Tweet', ['id_str', 'created_at', 'text'])
        Tweet_List = []
        for current_tweet in handles_tweets:
            Tweet_Tuple = Tweet(current_tweet.id_str, current_tweet.created_at, current_tweet.text)
            Tweet_List.append(Tweet_Tuple)
        return Tweet_List
        

    def _save_tweets(self):
        """Use the csv module (csv.writer) to write out the tweets.
        If you use a namedtuple get the column names with Tweet._fields.
        Otherwise define them as: id_str created_at text
        You can use writerow for the header, writerows for the rows"""
        with open(f'{DEST_DIR}/{self.handle}.{EXT}', mode='w+') as tweet_file:
            tweet_writer = csv.writer(tweet_file, delimiter='\t')
            tweet_writer.writerow(['id_str', 'created_at', 'text'])
            for count in range(0,len(self._tweets)):
                tweet_writer.writerow([self._tweets[count].id_str, self._tweets[count].created_at, self._tweets[count].text.encode('ascii', 'ignore')])

    def __len__(self):
        """See http://pybit.es/python-data-model.html"""
        pass

    def __getitem__(self, pos):
        """See http://pybit.es/python-data-model.html"""
        pass


if __name__ == "__main__":

    for handle in ('pybites', '_juliansequeira', 'bbelderbos'):
        print('--- {} ---'.format(handle))
        user = UserTweets(handle)
        #for tw in user[:5]:
        #    print(tw)
        print()
