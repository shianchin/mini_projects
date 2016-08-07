#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# Project           : Unit Test
#
# File name         : anime_downloader_test
#
# Author            : Cheang Shian Chin
#
# Date created      : 19 July 2016
#
# Purpose           : Unit test of anime_downloader.py
#
#----------------------------------------------------------------------

import unittest
from anime_downloader import download_torrent
from anime_downloader import find_dl_link
from anime_downloader import Log
from sandbox import rm
import os.path
import mock


class RmTestCase(unittest.TestCase):

    @mock.patch('sandbox.os')
    def test_rm(self, mock_os):
        rm("any path")
        # test that rm called os.remove with the right parameters
        mock_os.remove.assert_called_with("any path")

'''
class FindDlLinkTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getLinkToTorrent(self):
        self.assertTrue(find_dl_link('http://www.36dm.com/show-36b5bf6c9b3e1edda466377c95aad5a871a653d8.html'))

    def test_randomWebpage(self):
        self.assertFalse(find_dl_link('http://www.google.com'))
'''
class DownloadTorrentTest(unittest.TestCase):
    def setUp(self):
        self.filename = "C:\Users\user\Downloads\\test"
        self.torr_URL = "http://anidex.moe/[Doki]%20New%20Game!%20-%2003%20(1280x720%20h264%20AAC)%20[7471C168].mkv.torrent"
        self.logObj = Log('Doki Fansubs')

    def tearDown(self):
        pass
        #if os.path.isfile(self.filename+'.torrent'):
        #    os.remove(self.filename+'.torrent')

    @mock.patch('anime_downloader.requests.get')
    @mock.patch('anime_downloader.os.path')
    def test_newDownload(self, mock_os_path, mock_requests_get):
        # delete file if exist
        mock_response = mock.Mock()
        mock_os_path.isfile.return_value = False   # Make the file NOT 'exist'

        #mock_response.get =
        mock_requests_get.return_value = mock_response
        download_torrent(self.torr_URL, 'test', self.logObj)


    def test_fileExist(self):
        pass
        # download file if NOT exist
        if not os.path.isfile(self.filename+'.torrent'):
            download_torrent(self.torr_URL, 'test', self.logObj)
        self.assertTrue(os.path.isfile(self.filename+'.torrent'))
        #TODO: check return value when refactoring done

if __name__ == '__main__':
    unittest.main()


#----------------------------------------------------------------------
# Revision History  :
#
# Date           Author       Ref    Revision
# 19-Jul-2016    shianchin    1      Initial creation.
#
#----------------------------------------------------------------------