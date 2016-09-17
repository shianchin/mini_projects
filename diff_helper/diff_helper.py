#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# Project           : Diff Helper
#
# File name         : diff_helper.py
#
# Author            : Cheang Shian Chin
#
# Date created      : 17 September 2016
#
# Purpose           : To format the output of diff_helper.sh into CSV.
#
#----------------------------------------------------------------------

import os
import re
import subprocess

def main():
    while subprocess.call(["./diff_helper.sh"]):
        continue
        # SUCCESS, since return code is 0

    old_dir = ''
    with open('diff_raw.txt', 'r') as f:
        for line in f:
            if re.search(r'->', line):
                # is symlink
                d = os.path.split(line.split()[0])
                symlinkFlag = True
            else:
                d = os.path.split(line.rstrip())
                symlinkFlag = False

            new_dir = d[0]
            if(new_dir==old_dir):
                # files are in same directory
                print '\n,'+d[1],
                if symlinkFlag:
                    print ','+line.split()[1],line.split()[2],
            else:
                # files in different directory
                print '\n'+d[0]+','+d[1],
                if symlinkFlag:
                    print ','+line.split()[1],line.split()[2],
                old_dir = d[0]

if __name__ == '__main__':
  main()

#----------------------------------------------------------------------
# Revision History  :
#
# Date           Author       Ref    Revision
# 17-Sep-2016    shianchin    1      Initial creation.
#
#----------------------------------------------------------------------
