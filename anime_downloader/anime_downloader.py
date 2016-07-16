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
# Purpose           : Download anime torrent files from fansub.
#
# Revision History  :
#
# Date           Author       Ref    Revision
# 16-Jul-2016    shianchin    5      Support Doki Fansubs. Add dryrun option.
#                                    Use requests module.
# 16-Jul-2016    shianchin    4      Create a log class. Get rid of unnecessary
#                                    try-except. More cleanups.
# 16-Jul-2016    shianchin    3      Combine regex of various shows into one.
#                                    Change to use urllib2 to get html.
# 15-Jul-2016    shianchin    2      Create functions to parse showpage.html to
#                                    find dl link, func to download torrent file,
#                                    and use regex to find wanted shows.
# 11-Jul-2016    shianchin    1      Initial creation.
#
#**********************************************************************


from bs4 import BeautifulSoup
import os.path
import re
import requests
import sys

def main():
    # This is a lists of regexes to be used as pattern recognition.
    # Be sure to escape any special char
    DMshows_re = [
                 ur"【DHR動研&amp;輕之國度&amp;千夏&amp;KNA&amp;臉腫&amp;茉語星夢】\[Re：從零開始的異世界生活\]",
                 ur"【极影字幕社】 ★ 星之梦 planetarian",
                 ur"\[澄空学园&amp;华盟字幕社\] 食戟之灵 二之皿",
                 ur"【動漫國字幕組】★07月新番\[Rewrite\]\[\w\w\]\[720P\]\[簡繁外掛\]\[MKV\]",
                 ur"\[澄空学园&amp;雪飘工作室\]\[7月新番] Rewrite 第\d\d话 MP4 720p",
                 ] 
    DokiShows_re = [
                   ur"New Game! - \d\d \(1280x720 h264 AAC\)"
                   ]
    DM_MAX_PAGE = 7
    DOKI_MAX_PAGE = 5
    ### end of lists
    
    # if dryRun, only find matches but don't download them
    if (len(sys.argv) > 1) and (sys.argv[1] == '-d'):
        isDryRun = 'True'
        print 'DryRun is ON'
    else:
        isDryRun = 0


    ### Download from www.36dm.com
    DMLog = Log('www.36dm.com')    #log name is used as checks. Update all if changed.
    print '\n'+DMLog.name

    if len(DMshows_re) > 0:
        for page in range(1,DM_MAX_PAGE+1):
            print 'Page',page,'of',DM_MAX_PAGE
            homepage = requests.get('http://www.36dm.com/'+str(page)+'.html')

            if homepage.status_code == requests.codes.ok:
                find_match(homepage.text.encode('utf-8'), DMshows_re, DMLog, isDryRun)
    
    ### Download from doki.co
    DokiLog = Log('Doki Fansubs')   #log name is used as checks. Update all if changed.
    print '\n'+DokiLog.name

    if len(DokiShows_re) > 0:
        for page in range(1,DOKI_MAX_PAGE+1):
            print 'Page',page,'of',DOKI_MAX_PAGE
            homepage = requests.get('https://doki.co/page/'+str(page)+'/')
            
            if homepage.status_code == requests.codes.ok:
                find_match(homepage.text.encode('utf-8'), DokiShows_re, DokiLog, isDryRun)

    ### Report
    print '\n  ----Summary----'
    print 'Titles searched =',(DokiLog.search_count+DMLog.search_count)
    print 'Titles matched  =',(DokiLog.match_count+DMLog.match_count)
    
    if len(DokiLog.exist_list) > 0 or len(DMLog.exist_list) > 0:
        print '\nExisting files:'
        if len(DMLog.exist_list) > 0:
            print '\n'.join(DMLog.exist_list)
        if len(DokiLog.exist_list) > 0:
            print '\n'.join(DokiLog.exist_list)
    else:
        pass
        # do nothing
        
    if len(DokiLog.dl_list) > 0 or len(DMLog.dl_list) > 0:
        print '\nNEW files:'
        if len(DMLog.dl_list) > 0:
            print '\n'.join(DMLog.dl_list)
        if len(DokiLog.dl_list) > 0:
            print '\n'.join(DokiLog.dl_list)
    else:
        print '>>> No new release.'


def find_match(homepageHTML, shows_re_list, logObj, isDryRun):
    homepageSoup = BeautifulSoup(homepageHTML, "html.parser")
    combined_re = "(" + ")|(".join(shows_re_list) + ")"
    count = 0
    match_num = 0
    
    if logObj.name == 'Doki Fansubs':
        for p_tag in homepageSoup.find_all('p'):
            if p_tag.a and (p_tag.a.contents[0] == 'Torrent'):
                count += 1
                match = re.search(combined_re, p_tag.a.get('href'))
                if match:
                    match_num += 1
                    torr_URL = p_tag.a.get('href')
                    title = re.search(ur'\[Doki\].+mkv', torr_URL).group()  
                    # extract title from link
                    print 'Found: '+title
                    if not isDryRun:
                        download_torrent(torr_URL, title, logObj)

    elif logObj.name == 'www.36dm.com':
        for td_tag in homepageSoup.find_all('td'):
            if td_tag.get('style') == 'text-align:left;':
                count += 1
                title = td_tag.contents[1].string
                match = re.search(combined_re, title)
                if match:
                    match_num += 1
                    unicode_title = unicode(title).strip()
                    print 'Found: '+unicode_title
                    show_pageURL = 'http://www.36dm.com/'+td_tag.contents[1].get('href')
                    partial_dl_link = find_dl_link(show_pageURL)
                    if partial_dl_link and not isDryRun:
                        torr_URL = 'http://www.36dm.com/'+partial_dl_link
                        download_torrent(torr_URL, unicode_title, logObj)

    logObj.searched(count, match_num)


# Specific to www.36dm.com
def find_dl_link(show_pageURL):
    #link to show page
    showpageHTML = requests.get(show_pageURL).text.encode('utf-8')
    showpageSoup = BeautifulSoup(showpageHTML, "html.parser")
    dl_list = []
    
    for dl_attrs in showpageSoup.select('#download'):
        dl_list.append(dl_attrs.get('href'))
    
    #Should find 2 identical download links
    if (len(dl_list) == 2) and (dl_list[0]==dl_list[1]):
        retVal = dl_list.pop()
    else:
        print 'DL Link Error: Possible website layout change'
        retVal = 0

    return retVal


# This function will download a torrent file given link
def download_torrent(torr_URL, filename, logObj):
    #replace any forward slash in filename
    #append .torrent extension
    torr_filename = filename.replace("/","- -")+'.torrent'

    if not os.path.isfile(torr_filename):
        # file NOT exist
        fixedURL = torr_URL.replace(" ","%20")  # fix URL with white space
        
        r = requests.get(fixedURL)
        with open(torr_filename, 'wb') as torr_f:
            for chunk in r.iter_content(10000):
                torr_f.write(chunk)
        
        logObj.downloaded('TRUE', filename)
        print 'Torrent DOWNLOADED'

    else:
        logObj.downloaded('FALSE', filename)
        print 'Torrent file already exist.'


class Log:
    def __init__(self, name):
        self.name = name
        self.search_count = 0
        self.match_count = 0
        self.dl_list = []
        self.exist_list = []

    def searched(self, count, match):
        self.search_count += count
        self.match_count += match

    def downloaded(self, status, filename):
        if status == 'TRUE':
            self.dl_list.append(filename)
        elif status == 'FALSE':
            self.exist_list.append(filename)


if __name__ == '__main__':
    main()