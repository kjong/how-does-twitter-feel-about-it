# how-does-twitter-feel-about-it

Sentiment analysis tool written in Python using Tweepy and VADER

## Searches for tweets that:
- Contain specified hashtag
- Were posted between specified dates
- Were written in English

## Analysis:
- VADER sentiment analysis assigns a compound score between 1 (most positive) and -1 (most negative) to each tweet scraped

## Output:
- Total number of tweets scraped / analyzed
- Total number of positive tweets
- Total number of neutral tweets
- Total number of negative tweets
- Most positive tweet (text + compound score)
- Most negative tweet (text + compound score)
- Txt file of all scraped tweets

## Limitations:
- Twitter API free rate limits
- Can only scrape tweets from the past 7 days
- Can only analyze tweets in English

## Sample output:
![Sample Output](sample.png?raw=true "Sample Output")
