#!/usr/bin/python

import tweepy
import config


# authentication
def authenticate():
    print("Authenticating...")

    try:
        auth = tweepy.AppAuthHandler(
            config.consumer_key, config.consumer_secret)
        print("Authentication successfull.")
        return auth
    except tweepy.TweepError:
        print(tweepy.TweepError)


def main():
    auth = authenticate()


if __name__ == "__main__":
    main()
