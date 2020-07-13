# Here are a few short programs I wrote to help me understand Blockchain, Web Scraping and a little bit of NLP

In 2018, Imogen Heap started selling music through Blockchain and that was also when I found out about Kobalt for music streaming services - I wanted to really understand Blockchain deeper than Bitcoin at that point so I tried to implement my own:
1) basicBlocks.py was for me to understand how blockchains can actually maintain immutabililty through hashes
2) postBlockchain.py was an implementation of a blockchain to allow users to post comments which are added to blocks, which are added to the final blockchain. I have commented out the section where I had attempted to use Flask's documentation to add user endpoints for input during an IBM tutorial.

When I started to work on sourcing leads for WeWork in Hyderabad, we were not investing any money into software to help and all commercial email scrapers had daily limits, so I experiemtned with python to build my own:
3) emailScraper.py downloads all email addresses on the input url into an email.csv file
While understanding how to scrape data, a lot of tutorials showed how this data could be fed into machine learning algorithms so I wanted to see what was possible:
4) mlScraper.py uses the twitterscraper API to download tweets mentioning a specific phrase into a pandas dataframe
5) irisML.py is an implementation of analysis on the famous iris data set from the UCI machine learning repository, from their own tutorials
6) twitterScraping.py uses the same method as mlScraper.py to collect data and then run sentiment analysis using the vaderSentiment API - this instance of the class finds tweets about the extremely controversial Citizenship Amendment Act that the governement tried to pass in India just before covid-19, and compares the sentiments expressed in the tweets before the historic pogrom event in Delhi February and after. 
