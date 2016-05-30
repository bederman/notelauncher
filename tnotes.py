#notes.test.py
import re
import webbrowser, sys
import urllib
import urllib2
import string
import lxml.html
import httplib
import urlparse
from bs4 import BeautifulSoup
from lxml import etree
import os
savout = os.dup(1)
os.close(1)
os.open(os.devnull, os.O_RDWR)
try:

    def get_server_status_code(url):
        # http://stackoverflow.com/questions/1140661
        host, path = urlparse.urlparse(url)[1:3]    # elems [1] and [2]
        try:
            conn = httplib.HTTPConnection(host)
            conn.request('HEAD', path)
            return conn.getresponse().status
        except StandardError:
            return None

    def check_url(url):
        # see also http://stackoverflow.com/questions/2924422
        good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
        return get_server_status_code(url) in good_codes

    def litesearch(query):
        for lec in toc:
            if lec.contents[len(lec.contents)-1].find(query) != -1:
                if len(lec.contents) == 2:
                    print lec.find('a').string

    def deepsearch(query):
        for lec in lectures:
            lec_url = 'http://brick.cs.uchicago.edu/Courses/CMSC-16200/2013/' + lec['href']
            lec_page = urllib2.urlopen(lec_url)
            lec_soup = BeautifulSoup(lec_page.read())
            hits = lec_soup.body.findAll(text=re.compile(sys.argv[2]))
            if len(hits) > 0:
                print lec.string

    def summary(lec_nums):
        for i in lec_nums:
            exists = False
            for lec in toc:
                if len(lec.contents) == 2 and lec.find('a').string == "Lecture " + i:
                    print i + " - " + lec.contents[1][2:]
                    exists = True
            if not exists:
                print "Lecture " + i + " summary not available."

    toc_url = "http://brick.cs.uchicago.edu/Courses/CMSC-16200/2013/lectures.php"
    toc_page = urllib2.urlopen(toc_url)
    soup = BeautifulSoup(toc_page.read())
    toc_list = soup.find('ul')
    toc = toc_list.findAll('li')
    lectures = toc_list.findAll('a')

    if sys.argv[1] == "wiki":
        webbrowser.open('http://brick.cs.uchicago.edu/Courses/CMSC-16200/2013/pmwiki/pmwiki.php')
    elif sys.argv[1] == "toc":
        webbrowser.open(toc_url)
    elif sys.argv[1] == "latest":
        latest = toc[0]
        for lec in toc:
            latest = lec
        latest_link = latest.find('a')['href']
        webbrowser.open("http://brick.cs.uchicago.edu/Courses/CMSC-16200/2013/" + latest_link)

    elif len(sys.argv) > 2 and sys.argv[1] == "--search":
        litesearch(sys.argv[2])

    elif len(sys.argv) > 2 and sys.argv[1] == "--deep_search":
        deepsearch(sys.argv[2])


    elif len(sys.argv) > 2 and sys.argv[1] == "--summary":
        summary(sys.argv[2:])

    else:
        pages = {}
        for i in sys.argv[1:]:
            pages[i] = ("http://brick.cs.uchicago.edu/Courses/CMSC-16200/2013/Lectures/lecture-{0:02d}.php").format(int(i))
            if check_url(pages[i]):
                webbrowser.open((pages[i]))
            else:
                print "Lecture " + i + " not found!"

finally:
   os.dup2(savout, 1)
