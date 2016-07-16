#!/usr/bin/env python
# -*- coding: utf-8 -*-
#**********************************************************************
# Project           : Anime Downloader
#
# File name         : anime_downloader.py
#
# Author            : Cheang Shian Chin
#
# Date created      : 11 Jul 2016
#
# Purpose           : Download subsequent anime episodes as they come out.
#
# Revision History  :
#
# Date           Author       Ref    Revision
# 16-Jul-2016    shianchin    4      Created a log class. Got rid of unnecessary
#                                    try-except. More cleanups.
# 16-Jul-2016    shianchin    3      Combined regex of various shows into one.
#                                    Changed to use urllib2 to get html.
# 15-Jul-2016    shianchin    2      Created functions to parse showpage.html to
#                                    find dl link, func to download torrent file,
#                                    and use regex to find wanted shows.
# 11-Jul-2016    shianchin    1      Initial creation.
#
#**********************************************************************


from bs4 import BeautifulSoup
#import bs4
import re
import requests
import urllib2
import os.path

def main():
    # This is a list of regexes to be used as pattern recognition.
    shows_re = [
                ur"(【DHR動研&amp;輕之國度&amp;千夏&amp;KNA&amp;臉腫&amp;茉語星夢】\[Re：從零開始的異世界生活\])",
                ur"(【极影字幕社】 ★ 星之梦 planetarian)",
                ur"(\[澄空学园&amp;华盟字幕社\] 食戟之灵 二之皿)",
                ur"(【動漫國字幕組】★07月新番\[Rewrite\]\[\w\w\]\[720P\]\[簡繁外掛\]\[MKV\])"
               ] # be sure to escape any special char
    dmLog = Log('www.36dm.com')    
    MAX_PAGE = 5
    for page in range(MAX_PAGE):
        print 'Page',(page+1),'of',MAX_PAGE
        
        try:
            homepage = urllib2.urlopen('http://www.36dm.com/'+str(page+1)+'.html')
            find_match(homepage, shows_re, dmLog)
        except urllib2.HTTPError:
            print 'HTTP Error 404: Not Found'
    
    print '\n  ----Summary----'
    print 'Titles searched =',dmLog.search_count
    
    if len(dmLog.exist_list) > 0:
        print 'Existing files:'
        print '\n'.join(dmLog.exist_list)

    if len(dmLog.dl_list) > 0:
        print 'NEW files:'
        print '\n'.join(dmLog.dl_list)
    else:
        print 'No new release.'


def find_match(homepage, shows_re, dmLog):
    homepageSoup = BeautifulSoup(homepage.read(), "html.parser")
    combined_re = "(" + ")|(".join(shows_re) + ")"
    count = 0

    for td_tag in homepageSoup.find_all('td'):
        #print td_tag.get()
        if td_tag.get('style') == 'text-align:left;':
            count += 1
            title = td_tag.contents[1].string

            match = re.search(combined_re, title)

            if match:
                unicode_title = unicode(title).strip()
                print 'Found: '+unicode_title
        
                show_pageURL = 'http://www.36dm.com/'+td_tag.contents[1].get('href')
                partial_dl_link = find_dl_link(show_pageURL)
                torr_URL = 'http://www.36dm.com/'+partial_dl_link
                download_torrent(torr_URL, unicode_title, dmLog)

    dmLog.searched(count)


def find_dl_link(show_pageURL):
    #link to show page
    showpage = urllib2.urlopen(show_pageURL)
    showpageSoup = BeautifulSoup(showpage.read(), "html.parser")
    dl_list = []
    
    for dl_attrs in showpageSoup.select('#download'):
        dl_list.append(dl_attrs.get('href'))
    
    #Should find 2 identical download links
    if (len(dl_list) == 2) and (dl_list[0]==dl_list[1]):
        return dl_list.pop()
    else:
        print 'Error: Possible website layout change'


#This function will download a torrent file given link
def download_torrent(torr_URL, filename, torr_log):
    #replace any forward slash in filename
    torr_filename = filename.replace("/","- -")+'.torrent'

    if not os.path.isfile(torr_filename):
        # file NOT exist
        try:
            torr_data = urllib2.urlopen(torr_URL).read()
            with open(torr_filename, 'wb') as torr_f:
                torr_f.write(torr_data)
            torr_log.downloaded('TRUE', filename)
            print 'Torrent DOWNLOADED'
        except:
            print 'Error: Torrent file not created'

    else:
        torr_log.downloaded('FALSE', filename)
        print 'Torrent file already existed.'

class Log:
    def __init__(self, name):
        self.name = name
        self.search_count = 0
        self.dl_list = []
        self.exist_list = []

    def searched(self, count):
        self.search_count += count

    def downloaded(self, status, filename):
        if status == 'TRUE':
            self.dl_list.append(filename)
        elif status == 'FALSE':
            self.exist_list.append(filename)


if __name__ == '__main__':
    main()