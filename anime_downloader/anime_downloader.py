#!/usr/bin/env python

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
# 11-Jul-2016    shianchin    1      Initial creation.
#
#**********************************************************************


#from bs4 import BeautifulSoup
import bs4
import re
import requests


def main():
    res = requests.get('http://www.36dm.com/show-5f648c77db97b1777d6f58fcc4bc20f5b4c8f36a.html')
    res.raise_for_status()
    playFile = open('test.html', 'wb')
    for chunk in res.iter_content(100000):
        playFile.write(chunk)
    playFile.close()

    exampleFile = open('test.html')
    exampleSoup = bs4.BeautifulSoup(exampleFile.read(), "html.parser")
    #exampleSoup.prettify("gbk")
    #for link in exampleSoup.find_all('p', class_="original download"):
    for link in exampleSoup.select('#download'):
        print(link.get('href'))
    #elems = exampleSoup.select('#download')
    #print type(elems)
    #print len(elems)
    #print elems[0]


if __name__ == '__main__':
    main()