#!/usr/bin/python

import csv
import tweepy
import config


# authentication
def authenticate():
    print("Authenticating...")

    try:
        auth = tweepy.AppAuthHandler(
            config.consumer_key, config.consumer_secret)
        print("Authentication successful.")
        api = tweepy.API(auth)

        return api
    except tweepy.TweepError:
        print(tweepy.TweepError)


# open a csv file and scrape to it
def scrape(api):
    # open csv file
    with open("scrape_data.csv", "a") as csv_file:
        csv_writer = csv.writer(csv_file)

        for tweet in tweepy.Cursor(api.search,
                                   q=config.query,
                                   lang="en",
                                   since=config.start_date,
                                   until=config.end_date).items(100):
            print(tweet.text)


def main():
    api = authenticate()
    scrape(api)


if __name__ == "__main__":
    main()
