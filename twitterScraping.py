#For Dataframes
import pandas as pd 
import datetime as dt 
#For scraping input
from twitterscraper import query_tweets
#Sentiment Learning and Analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#filter between English and Hindi
from langdetect import detect 
#Visualisation
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.mlab as mlab

# Error handling, excpetion thrown if input is not string
def detector(x):
    try:
       return detect(x)
    except:
        None 
       
# Tweets from before pogrom and after, two sets for comparison
begin_date = dt.date(2020,2,15)
end_date = dt.date(2020,2,24)
begin_date_premier = dt.date(2020,2,25)
end_date_premier = dt.date(2020,3,15)

# Use Twitterscraper to save tweet-sets
tweets_before = query_tweets("#CAA", begindate = begin_date, enddate= end_date, limit = 1000)
tweets_after = query_tweets("#CAA", begindate = begin_date_premier, enddate = end_date_premier)
# Save as DataFrames                            
df_before = pd.DataFrame(t.__dict__ for t in tweets_before)
df_after = pd.DataFrame(t.__dict__ for t in tweets_after)

# Filter for english tweets
df_before['lang'] = df_before['text'].apply(lambda x:detector(x))
df_before = df_before[df_before['lang'] == 'en']
df_after['lang'] = df_after['text'].apply(lambda x: detector(x))
df_after = df_after[df_after['lang'] == 'en'] 

# Save to file so we don't have to stream the tweets again later if required
df_before.to_csv('caa_tweets_before_clean.csv')
df_before = pd.read_csv('caa_tweets_before_clean.csv')
df_after.to_csv('cm_tweets_after_clean.csv')
df_after = pd.read_csv('cm_tweets_after_clean.csv')

analyzer = SentimentIntensityAnalyzer()

# Get sentiment scores
# Expected  output {'neg: X, 'neu': Y, 'pos': Z. 'compound': A}
# Returns a score for Negativity, Neutrality, Positivity within the text fed, and also a compound score of all three
# Compund score = "normalised, weighted composite score of the sum of the lexicon ratings":
# Positive Sentiment: compound score >= 0.5
# Neutral Sentiment: compound score > -0.5 and < 0.5
# Negative Sentiment: compound score <= -0.5

sentiment_before = df_before['text'].apply(lambda x: analyzer.polarity_scores(x))
sentiment_after = df_after['text'].apply(lambda x: analyzer.polarity_scores(x))

# Add sentiment scores into dataframe
df_before = pd.concat([df_before, sentiment_before.apply(pd.Series)],1)
df_after = pd.concat([df_after, sentiment_after.apply(pd.Series)],1)

# Removing duplicates - likely IT cell bot tweets
df_before.drop_duplicates(subset = 'text',inplace = True)
df_after.drop_duplicates(subset = 'text',inplace = True)

#Displaying the results in graphs
print("Compound scores ")
df_before['compound'].hist()
df_before['compound'].mean()
df_before['compound'].median()

df_after['compound'].hist()
df_after['compound'].mean()
df_after['compound'].median()

