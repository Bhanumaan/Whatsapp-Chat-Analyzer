
            
import plotly.express
import re
import regex
import pandas as pd
import numpy as np
import emoji
import plotly.express as px
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import nltk.corpus
dir(nltk.corpus)
import stopwords
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

bad_words =['<Media omitted>']

with open("oldchat.txt") as oldfile,open('chat.txt', 'w') as newfile:
    for line in oldfile:
        if not any(bad_word in line for bad_word in bad_words):
            newfile.write(line)

def startsWithDateAndTime(s):
    pattern = '^\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{1,2}\S [AaPp][Mm] -'
    result = re.match(pattern, s)
    if result:
        return True
    return False


def FindAuthor(s):
    patterns = [
        '([\w]+):', 
        '([\w]+[\s]+[\w]+):', 
        '([\w]+[\s]+[\w]+[\s]+[\w]+):', 
        '([\w]+)[\u263a-\U0001f999]+:', 
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False


def getDataPoint(line):
    splitLine = line.split(' - ')
    dateTime = splitLine[0]
    message = ' '.join(splitLine[1:])
    if FindAuthor(message):
        splitMessage = message.split(': ')
        author = splitMessage[0]
        message = ' '.join(splitMessage[1:])
    else:
        author = None
    return dateTime, author, message


parsedData = []

conversationPath = 'chat.txt'
with open(conversationPath, encoding="utf-8") as fp:
    fp.readline()
    messageBuffer = []
    datetime, author = None, None
    while True:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if startsWithDateAndTime(line):
            if len(messageBuffer) > 0:
                parsedData.append([dateTime, author, ' '.join(messageBuffer)])
            messageBuffer.clear()
            dateTime, author, message = getDataPoint(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)

chat = pd.DataFrame(parsedData, columns=['DateTime', 'Author', 'Message'])

chat.head()
ducktales_group = list(chat.Author.unique())
ducktales_group
aliases = ['User 1','User 2','User 3','User 4','User 5','User 6','User 7','User 8','User 9','User 10','User 11','User 12','User 13','User 14','User 15','User 16','User 17','User 18','User 19','User 20','User 21','User 22','User 23','User 24','User 25','User 26','User 27','User 28','User 29','User 30','User 31','User 32','User 33','User 34','User 35','User 36','User 37','User 38','User 39','User 40','User 41','User 42','User 43','User 44','User 45','User 46','User 47','User 48','User 49','User 50','User 51','User 52','User 53','User 54','User 55','User 56','User 57','User 58','User 59','User 60','User 61','User 62','User 63']
chat['Author'].replace(ducktales_group, aliases, inplace=True)
for(name, alias) in zip(ducktales_group, aliases):
    chat.Message = chat.Message.str.replace(name,alias)
chat.head(10)

chat["DateTime"] = pd.to_datetime(chat["DateTime"])
