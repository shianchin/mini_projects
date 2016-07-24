#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
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
#----------------------------------------------------------------------


from bs4 import BeautifulSoup
import argparse
import os.path
import re
import requests

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
    DM_MAX_PAGE = 10
    DOKI_MAX_PAGE = 5
    ### end of lists

    # if dryRun, only find matches but don't download them
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dry", help="Perform a dry run - find all the matches without downloading them.",
                        action ="store_true", default = 0)
    args = parser.parse_args()
    if args.dry:
        isDryRun = 1
        print 'DryRun is ON'
    else:
        isDryRun = 0


    ### Download from www.36dm.com
    DMLog = Log('www.36dm.com')
    print '\n'+DMLog.name

    if len(DMshows_re):
        combined_re = "(" + ")|(".join(DMshows_re) + ")"
        reObj = re.compile(combined_re)
        stop = 0
        page = 1
        while ( not stop ):
            print 'Page',page,'of',DM_MAX_PAGE
            homepage = requests.get('http://www.36dm.com/'+str(page)+'.html')

            if homepage.status_code == requests.codes.ok:
                stop = findMatchDm(homepage.text.encode('utf-8'), reObj, DMLog, isDryRun)
            if page == DM_MAX_PAGE:
                stop = 1    # Force stop after reaching max page
            else:
                page += 1   # Go to next page

    ### Download from doki.co
    DokiLog = Log('Doki Fansubs')
    print '\n'+DokiLog.name

    if len(DokiShows_re):
        combined_re = "(" + ")|(".join(DokiShows_re) + ")"
        reObj = re.compile(combined_re)
        stop = 0
        page = 1
        while ( not stop ):
            print 'Page',page,'of',DOKI_MAX_PAGE
            homepage = requests.get('https://doki.co/page/'+str(page)+'/')

            if homepage.status_code == requests.codes.ok:
                stop = findMatchDoki(homepage.text.encode('utf-8'), reObj, DokiLog, isDryRun)
            if page == DOKI_MAX_PAGE:
                stop = 1    # Force stop after reaching max page
            else:
                page += 1   # Go to next page

    ### Output summary report
    report(DokiLog, DMLog)


def findMatchDoki(homepageHTML, shows_reObj, logObj, isDryRun):
    homepageSoup = BeautifulSoup(homepageHTML, "html.parser")
    count = 0
    match_num = 0
    fileExist = 0

    for p_tag in homepageSoup.find_all('p'):
        if p_tag.a and (p_tag.a.contents[0] == 'Torrent'):
            count += 1
            match = shows_reObj.search(p_tag.a.get('href'))
            if match:
                match_num += 1
                torr_URL = p_tag.a.get('href')
                # extract title from link
                title = re.search(ur'\[Doki\].+mkv', torr_URL).group()
                print 'Found: '+title
                if not isDryRun:
                    fileExist = downloadTorrent(torr_URL, title, logObj)
        if fileExist:
            logObj.addToTotal(count, match_num)
            return True    # break out from for-loop, force stop

    logObj.addToTotal(count, match_num)
    return False


def findMatchDm(homepageHTML, shows_reObj, logObj, isDryRun):
    homepageSoup = BeautifulSoup(homepageHTML, "html.parser")
    count = 0
    match_num = 0
    fileExist = 0

    for td_tag in homepageSoup.find_all('td'):
        if td_tag.get('style') == 'text-align:left;':
            count += 1
            title = td_tag.contents[1].string
            match = shows_reObj.search(title)
            if match:
                match_num += 1
                unicode_title = unicode(title).strip()
                print 'Found: '+unicode_title
                show_pageURL = 'http://www.36dm.com/'+td_tag.contents[1].get('href')
                partial_dl_link = findDlLink(show_pageURL)
                if partial_dl_link and not isDryRun:
                    torr_URL = 'http://www.36dm.com/'+partial_dl_link
                    fileExist = downloadTorrent(torr_URL, unicode_title, logObj)
                    if fileExist:
                        logObj.addToTotal(count, match_num)
                        return True    # break out from for-loop, force stop

    logObj.addToTotal(count, match_num)
    return False


# Specific to www.36dm.com
def findDlLink(show_pageURL):
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


def report(DokiLog, DMLog):
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


# This function will download a torrent file given link
def downloadTorrent(torr_URL, filename, logObj):
    #replace any forward slash in filename
    #append .torrent extension
    torr_filename = filename.replace("/","- -")+'.torrent'

    if not os.path.isfile(r'C:\Users\user\Downloads\\'+torr_filename):
        # file NOT exist
        fixedURL = torr_URL.replace(" ","%20")  # fix URL with white space

        r = requests.get(fixedURL)
        with open(r'C:\Users\user\Downloads\\'+torr_filename, 'wb') as torr_f:
            for chunk in r.iter_content(10000):
                torr_f.write(chunk)

        logObj.downloaded('TRUE', filename)
        print 'Torrent DOWNLOADED'
        fileExist = 0

    else:
        logObj.downloaded('FALSE', filename)
        print 'Torrent file already exist.'
        fileExist = 1
    return fileExist


class Log:
    def __init__(self, name):
        self.name = name
        self.search_count = 0
        self.match_count = 0
        self.dl_list = []
        self.exist_list = []

    def addToTotal(self, count, match):
        self.search_count += count
        self.match_count += match

    def downloaded(self, status, filename):
        if status == 'TRUE':
            self.dl_list.append(filename)
        elif status == 'FALSE':
            self.exist_list.append(filename)


if __name__ == '__main__':
    main()

#----------------------------------------------------------------------
# Revision History  :
#
# Date           Author       Ref    Revision
# 24-Jul-2016    shianchin    7      Create reObj before sending to findMatch.
#                                    Change functions naming convention.
# 20-Jul-2016    shianchin    6      Stop searching once find existing files.
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
#----------------------------------------------------------------------