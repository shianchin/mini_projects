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
# 16-Jul-2016    shianchin    3      Combined regex of various shows into one.
#                                    Changed to use urllib2 to get html.
# 15-Jul-2016    shianchin    2      Created functions to parse showpage.html to
#                                    find dl link, func to download torrent file,
#                                    and use regex to find wanted shows.
# 11-Jul-2016    shianchin    1      Initial creation.
#
#**********************************************************************


#from bs4 import BeautifulSoup
import bs4
import re
import requests
import urllib2
import os.path

def main():
    MAX_PAGE = 5
    for page in range(MAX_PAGE):
        print 'Page',(page+1),'of',MAX_PAGE
        homepage = urllib2.urlopen('http://www.36dm.com/'+str(page+1)+'.html')
                
        #print res.read().decode('utf-8')
        if homepage.getcode() == 200:
            find_match(homepage)
        else:
            print 'Error '+homepage.getcode()
        
        

    #print exampleFile.read().decode('utf-8')

    testWord = 'an example word:cat!!'
    match = re.search(r'word:\w\w\w', testWord)
    print match.group()

    #print title_list
    #for abc in exampleSoup.find_all('a'):
    #    print abc.get('href')

    #webpage = exampleSoup.prettify("gbk")
    #print webpage

    #elems = exampleSoup.select('#download')
    #print type(elems)
    #print len(elems)
    #print elems[0]

def find_match(homepage):
    homepageSoup = bs4.BeautifulSoup(homepage.read(), "html.parser")

    tag = homepageSoup.td
    count = 0
    fail_count = 0
    title_list = []

    for link in homepageSoup.find_all('td'):
        #print link.get()
        if link.get('style') == 'text-align:left;':
            count+=1
            #print type(tag)
            #str(link.contents[1]).decode('utf-8')
            title = link.contents[1].string
            title_list.append(title)

            shows_re = [
                        u"(【DHR動研&amp;輕之國度&amp;千夏&amp;KNA&amp;臉腫&amp;茉語星夢】\[Re：從零開始的異世界生活\])",
                        u"(【极影字幕社】 ★ 星之梦 planetarian)",
                        u"(\[澄空学园&amp;华盟字幕社\] 食戟之灵 二之皿)",
                        u"(【動漫國字幕組】★07月新番\[Rewrite\]\[\w\w\]\[720P\]\[簡繁外掛\]\[MKV\])"
                       ] # be sure to escape any special char
            combined_re = "(" + ")|(".join(shows_re) + ")"
            #print combined_re
            #regexes = [re.compile(ur'【DHR動研&amp;輕之國度&amp;千夏&amp;KNA&amp;臉腫&amp;茉語星夢】\[Re：從零開始的異世界生活\]')]
            #               re.compile(ur'【极影字幕社】 ★ 星之梦 planetarian')]
            #wantedTitle = [u'【DHR動研&amp;輕之國度&amp;千夏&amp;KNA&amp;臉腫&amp;茉語星夢】[Re：從零開始的異世界生活]']
            #               u'【极影字幕社】 ★ 星之梦 planetarian']
            #match = re.search(ur'(【DHR動研&amp;輕之國度&amp;千夏&amp;KNA&amp;臉腫&amp;茉語星夢】\[Re：從零開始的異世界生活\])|(【极影字幕社】 ★ 星之梦 planetarian)|(\[澄空学园&amp;华盟字幕社\] 食戟之灵 二之皿)|(【動漫國字幕組】★07月新番\[Rewrite\]\[\w\w\]\[720P\]\[簡繁外掛\]\[MKV\])', title)
            match = re.search(combined_re, title)

            try:
                if match:
                    #print match.group()
                    unicode_title = unicode(title)
                    print 'matched title: '+unicode_title
                    print type(unicode_title)
            
                    show_pageURL = 'http://www.36dm.com/'+link.contents[1].get('href')
                    print show_pageURL
                    dl_link = find_dl_link(show_pageURL)
                    torr_URL = 'http://www.36dm.com/'+dl_link
                    print torr_URL
                    download_torrent(torr_URL, unicode_title)
                    #titleFile.write(str(title).decode('utf-8'))
            except:
                fail_count+=1
                pass

            #print len(link.contents)

    print 'count = ',count
    print 'fail count = ',fail_count
    print 'title_list = ',len(title_list)

def find_dl_link(show_pageURL):
    #link to show page
    showpage = urllib2.urlopen(show_pageURL)
    showpageSoup = bs4.BeautifulSoup(showpage.read(), "html.parser")
    
    #exampleSoup.prettify("gbk")
    #for link in exampleSoup.find_all('p', class_="original download"):

    dl_list = []
    for link in showpageSoup.select('#download'):
        dl_list.append(link.get('href'))
        #print len(dl_list)
        #print(link.get('href'))
    
    return dl_list.pop()    #TODO : use list?

def download_torrent(dl_link, filename):
    #link to actual torrent file
    torrent_link = requests.get(dl_link)

    if torrent_link.status_code == requests.codes.ok:
        print 'Link OK'
    else:
        print 'Link ERROR'
    torrent_link.raise_for_status()
    

    torrent_filename = filename.strip().replace("/","- -")+'.torrent'   #replace any forward slash in filename
    print 'torrent name: '+torrent_filename
    print type(torrent_filename)

    if not os.path.isfile(torrent_filename):
        # file NOT exist
        try:
            torrent_file = open(torrent_filename, 'wb')
            for chunk in torrent_link.iter_content(100000):
                torrent_file.write(chunk)
            torrent_file.close()
            print 'Torrent DOWNLOADED'
        except:
            print 'Torrent file not created.'

    else:
        print 'Torrent file already existed.'

if __name__ == '__main__':
    main()