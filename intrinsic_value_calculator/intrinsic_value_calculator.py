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
import math
import requests

def main():
    #company_name = "MAXIS"
    company_name = "DIGI"
    #company_name = "TIMECOM"
    #company_name = "VS"
    incomeObj = Webpage("http://quotes.wsj.com/MY/XKLS/"+company_name+"/financials/annual/income-statement")
    #print incomeObj.getSoup()
    cashflowObj = Webpage("http://quotes.wsj.com/MY/XKLS/"+company_name+"/financials/annual/cash-flow")
    #print cashflowObj.getSoup()
    calcIntrinsicValue(company_name, incomeObj, cashflowObj)



def calcIntrinsicValue(company_name, incomeObj, cashflowObj):
    #reference: http://www.buffettsbooks.com/howtoinvestinstocks/course3/intrinsic-value-formula.html
    FCF = getPast5Years("Free Cash Flow", cashflowObj)
    print FCF

    average_fcf = sum(FCF)/len(FCF)    #MYR million / thousand
    print 'Average FCF = ',average_fcf

    short_fcf_growth_rate = getShortFcfGrowthRate(incomeObj)
    short_term = 10    #years
    # What do you consider short term (most common is 10 years)?
    discount_rate = 0.1
    # What discount rate to use?
    long_fcf_growth_rate = 0.03
    # After the 10th year, what percent (whole number) will the company continue to
    # grow into perpetuity (recommend 3% or lower)?
    shares_outstanding = getSharesOutstanding(incomeObj)    #million / thousand

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
    print "Company: "+company_name
    print ("Intrinsic value = RM {0:.2f}" .format(intrinsic_value))


def getSharesOutstanding(incomeObj):
    shares = getPast5Years("Diluted Shares Outstanding", incomeObj)
    return shares[0]    # get only the latest

def getShortFcfGrowthRate(incomeObj):
    netIncome = getPast5Years("Net Income", incomeObj)

    print "Year 2011:", netIncome[4]
    print "Year 2015:", netIncome[0]

    # value1 = value5*(1+short_fcf_growth_rate)^4
    temp1 = math.log10(float(netIncome[0])/float(netIncome[4]))
    temp2 = temp1/4
    short_fcf_growth_rate = math.pow(10, temp2) -1
    print "Short term FCF growth rate: ",short_fcf_growth_rate
    return short_fcf_growth_rate

def getPast5Years(toFind, webObj):
    retList_unicode = []
    retList_int = []
    webSoup = webObj.getSoup()

    #print webSoup.prettify('utf-8')

    for tr_tag in webSoup.find_all('tr'):
        if tr_tag.td:
            #print type(tr_tag.td)
            #print tr_tag.td
            #print tr_tag.td.contents[0]
            if tr_tag.td.contents[0] == toFind:
                print tr_tag.td.contents[0]
                print '!!!!!!!!!!!!!!!!!'

                value1 = tr_tag.td.next_sibling.next_sibling.string
                value2 = tr_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.string
                value3 = tr_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
                value4 = tr_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
                value5 = tr_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string

                print value1    #latest
                print value2
                print value3
                print value4
                print value5    #5 years ago
                print type(unicode(value1))

                retList_unicode.append(unicode(value1))
                retList_unicode.append(unicode(value2))
                retList_unicode.append(unicode(value3))
                retList_unicode.append(unicode(value4))
                retList_unicode.append(unicode(value5))


    for u in retList_unicode:
        i = u.replace(",","")   # remove comma from number
        print i.translate("()")
        i = i.replace("(","-")  # ugly way to convert bracket number to -ve
        i = i.replace(")","")
        print "i :",i
        #print type(i)
        retList_int.append(float(i))  # convert to float

    return retList_int

class Webpage:
    def __init__(self, pageURL):
        self.page_soup = None
        self.setSoup(pageURL)

    def setSoup(self, pageURL):
        r = requests.get(pageURL)
        if r.status_code == requests.codes.ok:
            pageHTML = r.text.encode('utf-8')
            page_soup = BeautifulSoup(pageHTML, "html.parser")
        self.page_soup = page_soup

    def getSoup(self):
        return self.page_soup

if __name__ == '__main__':
    main()

#----------------------------------------------------------------------
# Revision History  :
#
# Date           Author       Ref    Revision
# 23-Jul-2016    shianchin    1      Initial creation.
#
#----------------------------------------------------------------------