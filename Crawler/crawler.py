import queue
import requests
from bs4 import BeautifulSoup
import re

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
    soap = BeautifulSoup(text, 'lxml')
    return soap.get_text()

def Crawl(seedUrl, anchor):
    urls = []
    anchorQueue = queue.Queue()
    while True:
        response = requests.get(seedUrl + anchor)
        links = GetLinks(response.text)
        htmlText = GetTextFromHtml(response.text)
        if(len(links) > 0):
            for link in links:
                return                
        a = 5