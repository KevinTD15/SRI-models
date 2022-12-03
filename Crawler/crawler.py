import queue
import requests
from bs4 import BeautifulSoup
import re
import time
import os

def GetLinks(url):
    return re.findall('"((http)s?://.*?)"', url)

def DeleteCommand(text, command):
    while(True):
        start = text.find('<'+command[0], 0, len(text))
        if(start == -1):
            break
        end = text.find('</'+command[0]+'>', start, len(text))
        text = text.replace(text[start:end + command[1]], ' ', 1)
    return text

def GetTextFromHtml(text):
    commands = [('script', 9), ('span', 7), ('style', 8)]
    for i in commands:
        text = DeleteCommand(text, i)
    soap = BeautifulSoup(text, features='lxml').get_text()
    soap = soap.replace('\n', '')
    return soap

def IsTrueWeb(url):
    url = url[0]
    return (url.count('.ico') + url.count('.gif') + url.count('.jpg') + url.count('.js') + url.count('.png') + url.count('.css')) == 0

def createNewTxt(folder):    
    return os.path.join(folder, str(len(os.listdir(folder))) + ".txt")

def saveDoc(url,text):
    
    with open(createNewTxt('Crawler\cache'),'w', encoding='utf8', errors='ignore') as f:
        f.write(url[0] + '\n' + text)

def Crawl(seedUrl, t):
    visitedUrl = set()
    parsedUrl = []
    htmlText = []
    start = time.time()
    end = time.time()
    while len(seedUrl)>0 and (end-start)<=t:
        visitedUrl.add(seedUrl[0])
        url = seedUrl.pop(0)
        parsedUrl.append(url)
        response = requests.get(url[0])
        links = GetLinks(response.text)
        htmlText.append(GetTextFromHtml(response.text))
        direct = os.listdir('Crawler\cache')
        for i in direct:
            a = open('Crawler/cache/'+i,encoding='utf8', errors='ignore')
            if(url[0] in a.read()):
                break
        saveDoc(url, htmlText[len(htmlText) - 1])
        if(len(links) > 0):
            for link in links:
                if(IsTrueWeb(link) and link not in seedUrl and link not in visitedUrl):
                    visitedUrl.add(link)
                    seedUrl.append(link) 
        end = time.time()   
    return htmlText, parsedUrl