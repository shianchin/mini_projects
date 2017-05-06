#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# Project           : Task table checker
#
# File name         : task_table_checker.py
#
# Author            : Cheang Shian Chin
#
# Date created      : 06 May 2017
#
# Purpose           : Check the order of task in tasks_table.
#
#----------------------------------------------------------------------

# python 2.7.6
import re

# File path constants
EXPECTED_TASK_TABLE = './expected_task_table.cpp'
ACTUAL_TASK_TABLE = './actual_task_table.cpp'

def main():
    with open(EXPECTED_TASK_TABLE, 'r') as file:
        expectedTaskname = PopulateTaskName(file)

    with open(ACTUAL_TASK_TABLE, 'r') as file:
        actualTaskname = PopulateTaskName(file)

    print expectedTaskname
    print actualTaskname
    for taskname in actualTaskname:
        # Assume there's only one task table in EXPECTED_TASK_TABLE.
        if cmp(expectedTaskname[0], taskname):
            print 'Error: Task table not matched.'
        else:
            print 'Looks good'

def PopulateTaskName(file):
    isStart = False
    isEnd = False
    taskname = []
    tasknameList = []

    for line in file:
        if (re.match('extern const task_t tasks_table', line)):
            isStart = True

        if (re.search('};', line)):
            isEnd = True

        if isStart and not isEnd:
            line = line.strip()  # strip whitespace and newline
            match = re.match(r'{\w+,', line)  # match string that looks like this: {XXX_YYY_ZZZ,
            if match:
                line = match.group()
                line = line.strip('{,')  # strip curly bracket and comma.
                taskname.append(line)

        # One table parsed complete.
        if isStart and isEnd:
            # Reset the flags.
            isStart = False
            isEnd = False
            # Save the list to another list, in case we have multiple tables.
            tasknameList.append(taskname)
            # Use a new list. Don't use 'del taskname[:]' since this will delete all reference to it.
            taskname = []

    # return the list of taskname
    return tasknameList


if __name__ == '__main__':
    main()

#----------------------------------------------------------------------
# Revision History  :
#
# Date           Author       Ref    Revision
# 06-May-2017    shianchin    1      Initial creation.
#
#----------------------------------------------------------------------
