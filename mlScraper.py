from twitterscraper import query_tweets
import pandas as pd
import datetime as dt

begin_date = dt.date(2018,10, 20)
end_date = dt.date(2019, 3, 14)

limit = 200
lang = 'English'

tweets = query_tweets("Trump", begindate = begin_date, enddate = end_date, limit = limit, lang = lang)

df = pd.DataFrame(t.__dict__ for t in tweets)

print(df)
