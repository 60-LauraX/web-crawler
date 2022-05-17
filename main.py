import requests
import threading
import queue
import csv
import validators
import time

from urllib.request import Request, urlopen, URLError, urljoin
from urllib.parse import urlparse
from datetime import datetime
from bs4 import BeautifulSoup

from multiprocessing import Lock

# get html content on first URL
startUrl = 'http://komputasi.lipi.go.id/utama.cgi?depan'
outputName = 'WebCrawler.csv'

lst = []
freq = []
temp = []

# max executed time
timeout = 30.0
# max url crawled
maxUrl = 10

# start time
startTime = time.time()


class crawler(threading.Thread):
    def getResponse(self):
        currentTime = datetime.now()
        response = requests.get(startUrl)
        soup = BeautifulSoup(response.content, 'lxml')
        return soup

    def __init__(self, startUrl_locks, startUrl):
        threading.Thread.__init__(self)
        # print("Web Crawler worker" + {threading.current_thread()} + "has Started")
        # self.base_url = base_url
        # self.links_to_crawl = links_to_crawl
        # self.have_visited = have_visited
        # self.error_links = error_links
        self.startUrl_locks = startUrl_locks
        self.startUrl = startUrl

    def urlScrapping(self, soup, w):
        for row in soup.findAll('a', href=True):
            self.startUrl_locks.acquire()
            # startUrl = self.startUrl.get()
            startUrl = self.startUrl
            self.startUrl_locks.release()

            # scrappedUrl = {}
            newUrl = row['href']
            parsed = urlparse(newUrl)
            splitUrl = parsed.netloc
            temp.append(splitUrl)
            isTimeout = self.timeoutChecker()
            if isTimeout == False:
                self.webCrawler(newUrl, w)
            else:
                break
                # print("URL:", a['href'])

        # self.splitUrl.task_done()

    def appendToDict(self, w):
        countDict = {i: temp.count(i) for i in temp}
        # print(countDict)
        lst = [url for (url, count) in countDict.items()] \
            # lst = countDict.items()
        freq = [count for (url, count) in countDict.items()]
        # isValid = validators.url(newUrl)
        for k, v in countDict.items():
            w.writerow([k, v])
        return

    # def generateCsv(urls):
    #   with open(outputName, 'w', newline = '') as f:
    #     header = ['Scrapped URL', 'Frequency']
    #     w = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
    #     w.writeheader()
    #     for k,v in lst:
    #       print(k,v)
    #       w.writerow(k + "," + v)

    def webCrawler(self, url, w):
        # start web crawling
        soup = self.getResponse()
        self.urlScrapping(soup, w)

    def timeoutChecker(self):
        currentTime = time.time()
        checker = currentTime - startTime
        print(checker)
        if checker < timeout:
            return False
        else:
            return True

    def main(self):
        with open(outputName, 'w', newline='') as f:
            header = ['Scrapped URL', 'Frequency']
            # w = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
            # w.writeheader()]
            w = csv.writer(f, delimiter=',')
            w.writerow(header)

            asd = self.webCrawler(startUrl, w)
            self.appendToDict(w)
            print('Lanjut csv')
            # self.generateCSV(lst)
            print('Web Crawler Success')

            # crawler = Crawler(startUrl_locks = startUrl_locks, startUrl = startUrl)


if __name__ == "__main__":
    startUrl_locks = Lock()
    cr = crawler(startUrl_locks=startUrl_locks, startUrl=startUrl)
    cr.main()