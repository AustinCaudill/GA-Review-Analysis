#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 15:22:56 2021

@author: austincaudill
"""

## Prep console and clear variables ##
# %clear
from IPython import get_ipython
get_ipython().magic('reset -sf')
#######################################

import requests
from bs4 import BeautifulSoup

# Define the process by which we retrieve the page data.
def getData(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all("ul", class_="review course-card")
    soup2 = BeautifulSoup(str(results), 'html.parser')
    results2 = soup2.find_all("div", class_="read-more")
    soup3 = BeautifulSoup(str(results2), 'html.parser')
    reviews = soup3.get_text()
    # print(results)
    if reviews == None:
        return []
    else:
        return reviews


# Scrape the webpages
reviews_all = []
i = 46 #Don't start at 0 as server gives same page at 0 or 1.
while True:
    data = getData(f'https://www.coursereport.com/schools/general-assembly?filter_by=default&amp;page={i}&amp;sort_by=default#reviews')
    if data != '[]':
        
        print(f'Page No:     {i}')
        reviews_all.append(data)
        i= i +1 
            # Should be no more than 50 pages.
    else:
        print("Review Scraping Complete.")
        break

# Write all scraped data to file.
f = open("scraped_reviews.txt", "a")
f.write(str(reviews_all))
f.close()


# Text Preprocessing
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from nltk.stem import PorterStemmer
stop_words = set(stopwords.words('english'))
stop_words_ext = ['ga', 'go', 'bootcamp', 'instructor', 'review', 'helpful', 'flag', 'inappropriate', 'xa', 'General', 'Assembly']


def preprocess(text):
    
    #regular expression keeping only letters - more on them later
    letters_only_text = re.sub("[^a-zA-Z]", " ", text)
    letters_only_text  = re.sub("'", "", letters_only_text)

    # convert to lower case and split into words -> convert string into list ( 'hello world' -> ['hello', 'world'])
    words = letters_only_text.lower().split()

    cleaned_words = []
    lemmatizer = PorterStemmer()
    
    # remove stopwords
    for word in words:
        if word not in stop_words and word not in stop_words_ext:
            cleaned_words.append(word)
            
    cleaned_words = [i.replace("'", "") for i in cleaned_words]      
    return cleaned_words
    
    
    # stemm or lemmatise words
    stemmed_words = []
    for word in cleaned_words:
        word = lemmatizer.stem(word)
        stemmed_words.append(word)
        
        
    stemmed_words2 = []
    for word in stemmed_words:
        if word not in stop_words_ext:
            stemmed_words2.append(word)
    
    # converting list back to string
    return " ".join(stemmed_words2)



reviews_all = str(reviews_all)
cleaned_reviews = preprocess(reviews_all)    

word_tokens = word_tokenize(str(cleaned_reviews)) #converts into individual words

number_of_words = len(word_tokens)
# print(number_of_words)


from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(width = 700, height = 700, 
                background_color ='white', 
                min_font_size = 10).generate(str(word_tokens) )
  
# plot the WordCloud image                        
plt.figure(figsize = (10, 10), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show()
        
        
