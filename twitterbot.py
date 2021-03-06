from time import sleep

import markovify
import tweepy
from twitter_cred import consumer_key, consumer_secret, access_token, access_token_secret

class TweetBot:
    def __init__(self, corpus):
        self.load_corpus(corpus)

        # initialize Twitter authorization with Tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def load_corpus(self, corpus):
        with open(corpus) as corpus_file:
            corpus_lines = corpus_file.read()
        self.model = markovify.Text(corpus_lines)

    def tweet(self):
        message = self.model.make_short_sentence(140)
        try:
            self.api.update_status(message)
        except tweepy.TweepError as error:
            print(error.reason)

    def automate(self, delay):
        while True:
            self.tweet()
            sleep(delay)


def main():
    bot = TweetBot("corpus.txt")
    bot.automate(3600)


if __name__ == "__main__":
    main()