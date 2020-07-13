import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
import re

inputUrl = input("What website are we scraping?") 

toScrape = deque([inputUrl])  

scraped = set()  

emails = set()  

while len(toScrape):

    url = toScrape.popleft()  
    scraped.add(url)
    parts = urlsplit(url)
        
    #urlsplit() from urllib.parse library
    #Input: 
    #"https://www.google.com/example"
    #Output:
    #SplitResult(scheme='https', netloc='www.google.com', path='/example', query='', fragment='')

    base = "{0.scheme}://{0.netloc}".format(parts)
    if '/' in parts.path:
      path = url[:url.rfind('/')+1]
    else:
      path = url

    print("Crawling the entered URL: %s" % url)
    
    #error handling - throw away pages with mismatching Schema
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        continue


    # Reuglar expression matching an email from re documentation        
    newEmails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", response.text, re.I))
    emails.update(newEmails) 

    soup = BeautifulSoup(response.text, 'lxml')

    for anchor in soup.find_all("a"):
      if "href" in anchor.attrs:
        link = anchor.attrs["href"]
      else:
        link = ''

        if link.startswith('/'):
            link = base + link
        
        elif not link.startswith('http'):
            link = path + link

        if not link.endswith(".gz"):
          if not link in toScrape and not link in scraped:
              toScrape.append(link)

# Write to file named email.csv

df = pd.DataFrame(emails, columns=["Email"])
df.to_csv('email.csv', index=False)

print("Done! Check email.csv file created in the same folder as this program.")