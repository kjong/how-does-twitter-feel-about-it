#!/usr/bin/python

import re
import tweepy
import config
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def authenticate():
    """Authentication
    """
    print("Authenticating...")

    try:
        auth = tweepy.AppAuthHandler(config.consumer_key,
                                     config.consumer_secret)
        print("Authentication successful.")
        api = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)

        return api
    except tweepy.TweepError:
        print(tweepy.TweepError)


def clean(text):
    """Clean up text
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())


def analyze(text):
    """Perform sentiment analysis on text

    Positive sentiment : compound_score >= 0.05
    Neutral sentiment : 0.05 > compound_score > -0.05
    Negative sentiment : compound_score <= -0.05

    :return: compound_score -> compound score between -1 (most negative) and 1 (most positive)
    """
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)["compound"]
    print(score)
    return score


def scrape(api):
    """Open a txt file and scrape to it

    :return: total_tweets -> total number of tweets scraped to file
    """
    # open txt file
    with open("scraped_tweets.txt", "w", encoding="utf-8") as txt_file:
        print("Scraping...")

        total_tweets = 0
        pos_count = 0
        neu_count = 0
        neg_count = 0
        curr_score = 0
        highest_score = 0
        lowest_score = 0
        for tweet in tweepy.Cursor(api.search,
                                   q=config.query,
                                   lang="en",
                                   since=config.start_date,
                                   until=config.end_date).items(5000):
            # exclude retweets
            if "RT" not in tweet.text:
                clean_text = clean(tweet.text)
                txt_file.write(clean_text + "\n")

                # analyze
                curr_score = analyze(clean_text)

                # positive
                if curr_score >= 0.05:
                    pos_count += 1

                # neutral
                elif curr_score > -0.05 and curr_score < 0.05:
                    neu_count += 1

                # negative
                elif curr_score <= -0.05:
                    neg_count += 1

                if curr_score > highest_score:
                    highest_score = curr_score
                    pos_text = clean_text

                elif curr_score < lowest_score:
                    lowest_score = curr_score
                    neg_text = clean_text

                total_tweets += 1

        print("Scraped " + str(total_tweets) + " tweets.")
        return (highest_score, pos_text), (lowest_score, neg_text), (pos_count, neu_count, neg_count)


def main():
    api = authenticate()
    pos_tweet, neg_tweet, counts = scrape(api)

    # print results
    print("Number of positive tweets: " + str(counts[0]))
    print("Number of neutral tweets: " + str(counts[1]))
    print("Number of negative tweet: " + str(counts[2]))
    print("Most positive tweet: " + pos_tweet[1] +
          " with a score of: " + str(pos_tweet[0]))
    print("Most negative tweet: " + neg_tweet[1] +
          " with a score of: " + str(neg_tweet[0]))


if __name__ == "__main__":
    main()
