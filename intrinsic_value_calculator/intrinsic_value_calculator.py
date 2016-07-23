#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# Project           : Intrinsic Value Calculator
#
# File name         : intrinsic_value_calculator.py
#
# Author            : Cheang Shian Chin
#
# Date created      : 23 Jul 2016
#
# Purpose           : Calculate the intrinsic value of stocks on KLSE.
#
#----------------------------------------------------------------------


from bs4 import BeautifulSoup
import requests

def main():
    cal_intrinsic_val()


def cal_intrinsic_val():
    #reference: http://www.buffettsbooks.com/howtoinvestinstocks/course3/intrinsic-value-formula.html
    FCF = get_FCF()
    print FCF

    average_fcf = sum(FCF)/len(FCF)    #RM million
    print 'Average = ',average_fcf

    short_fcf_growth_rate = 0.03
    short_term = 10    #years
    discount_rate = 0.1
    long_fcf_growth_rate = 0.03
    shares_outstanding = 7511    #million

    FCFn = average_fcf    # free cash flow at year N; init to average_fcf for year 0
    sum_of_FCFn = 0
    DFCFn = 0   # discounted free cash flow at year N
    sum_of_DFCFn = 0

    for n in range(1,12):
        print n
        print "before: ",FCFn
        FCFn = FCFn*(1+short_fcf_growth_rate)   # find FV of FCF at year N
        print "after: ", FCFn
        print "discount rate: ", (1+discount_rate)**n
        DFCFn = FCFn/(1+discount_rate)**n  # discount back to PV
        if n == 11:
            print 'DFCFn:',DFCFn
            #discontinued_perpetuity_cash_flow
            DPCF = (DFCFn*(1+long_fcf_growth_rate)) / (discount_rate - long_fcf_growth_rate)
            print 'DPCF:',DPCF
            DFCFn = 0   # don't add to sum
        else:
            sum_of_DFCFn += DFCFn
            print 'FCF',n,'=',FCFn
            print 'DFCF',n,'=',DFCFn
            print 'Sum of DFCFn =',sum_of_DFCFn

    intrinsic_value = (sum_of_DFCFn + DPCF)/shares_outstanding
    print ("Intrinsic value = RM {0:.2f}" .format(intrinsic_value))

def get_FCF():
    cashflowpage = requests.get('http://quotes.wsj.com/MY/XKLS/MAXIS/financials/annual/cash-flow')
    FCF = []
    FCF_int = []
    if cashflowpage.status_code == requests.codes.ok:
        cashflowHTML = cashflowpage.text.encode('utf-8')
        cashflowSoup = BeautifulSoup(cashflowHTML, "html.parser")

    #print cashflowSoup.prettify('utf-8')

    for tr_tag in cashflowSoup.find_all('tr'):
        if tr_tag.td:
            #print type(tr_tag.td)
            #print tr_tag.td
            #print tr_tag.td.contents[0]
            if tr_tag.td.contents[0] == 'Free Cash Flow':
                print tr_tag.td.contents[0]
                print '!!!!!!!!!!!!!!!!!'
                #latest
                FCF1 = tr_tag.td.next_sibling.next_sibling.string
                FCF2 = tr_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.string
                FCF3 = tr_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
                FCF4 = tr_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
                #5 years ago
                FCF5 = tr_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
                print FCF1
                print FCF2
                print FCF3
                print FCF4
                print FCF5
                print type(unicode(FCF1))
                FCF.append(unicode(FCF1))
                FCF.append(unicode(FCF2))
                FCF.append(unicode(FCF3))
                FCF.append(unicode(FCF4))
                FCF.append(unicode(FCF5))
    for x in FCF:
        a = x.replace(",","")   # delete comma from number
        FCF_int.append(int(a))  # convert to int
        print a
    return FCF_int

if __name__ == '__main__':
    main()

#----------------------------------------------------------------------
# Revision History  :
#
# Date           Author       Ref    Revision
# 23-Jul-2016    shianchin    1      Initial creation.
#
#----------------------------------------------------------------------