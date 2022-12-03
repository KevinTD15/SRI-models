from Crawler.crawler import *

seedUrl = [('https://www.geeksforgeeks.org/', 'http')]
def callCrawler(t):
    return Crawl(seedUrl, t)