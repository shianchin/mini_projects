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
    #companyObj = Webpage("http://quotes.wsj.com/company-list/country/malaysia/1")
    #company_dict = getCompany(companyObj)
    #for k, v in company_dict.items():
    #    print k,v
    # FBM KLCI TOP 30 companies

    FBM_KLCI = ["AMBANK",
                "ASTRO",
                "AXIATA",
                "BAT",
                "CIMB",
                "DIGI",
                "FGV",
                "GENTING",
                "GENM",
                "HLBANK",
                "HLFG",
                "IHH",
                "IOICORP",
                "IOIPG",
                "KLK",
                "MAYBANK",
                "MAXIS",
                "MISC", #!!!!!!!
                "PCHEM",
                "PETDAG",
                "PETGAS",
                "PPB",
                "PBBANK",
                "RHBBANK",  #!!!!!!!
                "SKPETRO",
                "SIME",
                "TM",
                "TENAGA",
                "UMW",
                "YTL"]

    #company_name = "TIMECOM"
    #company_name = "VS"

    # Lists (for exporting to csv purpose)
    header_list = ["Company",
            "FCF Year 2015","FCF Year 2014","FCF Year 2013","FCF Year 2012","FCF Year 2011","Average FCF",
            "Net Income Year 2015","Net Income Year 2014","Net Income Year 2013","Net Income Year 2012","Net Income Year 2011","FCF growth",
            "Short term duration","Discount rate","Long term growth rate",
            "Shares outstanding","Current price","Intrinsic value"]
    dictObj = ReportDict(header_list)
    outDict = dictObj.getDict()
    csvObj = CSV(header_list)



    for company in FBM_KLCI:
        try:
            incomeObj = Webpage("http://quotes.wsj.com/MY/XKLS/"+company+"/financials/annual/income-statement")
            cashflowObj = Webpage("http://quotes.wsj.com/MY/XKLS/"+company+"/financials/annual/cash-flow")
            #financialsObj = Webpage("http://quotes.wsj.com/MY/XKLS/"+company+"/financials")
            dictObj.writeTo("Company", company)
            calcIntrinsicValue(incomeObj, cashflowObj, dictObj)

            csvObj.appendToCSV(outDict)

            for header in header_list:
                print "{} : {}".format(header, outDict[header])
                # print everything in order
        except IndexError:
            print "ERROR: Data not available."


def getCompany(companyObj):
    companySoup = companyObj.getSoup()
    count = 0
    company_dict = {}
    company_name = []
    company_link = []
    #print companySoup.prettify('utf-8')
    for td_tag in companySoup.find_all('td'):
        #print td_tag.contents
        #print len(td_tag.contents)
        if td_tag.contents:
            if td_tag.contents[0].encode('utf-8') == "XKLS":
                count+=1
                name = td_tag.previous_sibling.previous_sibling.span.string
                link = td_tag.previous_sibling.previous_sibling.a.get('href')
                company_dict[name] = link
                #print count, name
                #print count, link
    return company_dict


def calcIntrinsicValue(incomeObj, cashflowObj, dictObj):
    #reference: http://www.buffettsbooks.com/howtoinvestinstocks/course3/intrinsic-value-formula.html
    FCF = getPast5Years("Free Cash Flow", cashflowObj)
    dictObj.writeTo("FCF Year 2015", FCF[0])
    dictObj.writeTo("FCF Year 2014", FCF[1])
    dictObj.writeTo("FCF Year 2013", FCF[2])
    dictObj.writeTo("FCF Year 2012", FCF[3])
    dictObj.writeTo("FCF Year 2011", FCF[4])
    #print FCF

    average_fcf = sum(FCF)/len(FCF)    #MYR million / thousand
    #print 'Average FCF = ',average_fcf

    short_fcf_growth_rate = getShortFcfGrowthRate(incomeObj, dictObj)

    # What do you consider short term (most common is 10 years)?
    short_term = 10    #years

    # What discount rate to use?
    discount_rate = 0.1

    # After the 10th year, what percent (whole number) will the company continue to
    # grow into perpetuity (recommend 3% or lower)?
    long_fcf_growth_rate = 0.03
    shares_outstanding = getSharesOutstanding(incomeObj)    #million / thousand
    current_price = getCurrentPrice(incomeObj)

    dictObj.writeTo("Average FCF", average_fcf)
    dictObj.writeTo("FCF growth", short_fcf_growth_rate)
    dictObj.writeTo("Short term duration", short_term)
    dictObj.writeTo("Discount rate", discount_rate)
    dictObj.writeTo("Long term growth rate", long_fcf_growth_rate)
    dictObj.writeTo("Shares outstanding", shares_outstanding)
    dictObj.writeTo("Current price", current_price)


    FCFn = average_fcf    # free cash flow at year N; init to average_fcf for year 0
    sum_of_FCFn = 0
    DFCFn = 0   # discounted free cash flow at year N
    sum_of_DFCFn = 0

    for n in range(1,12):
        #print n
        #print "before: ",FCFn
        FCFn = FCFn*(1+short_fcf_growth_rate)   # find FV of FCF at year N
        #print "after: ", FCFn
        #print "discount rate: ", (1+discount_rate)**n
        DFCFn = FCFn/(1+discount_rate)**n  # discount back to PV
        if n == 11:
            #print 'DFCFn:',DFCFn
            #discontinued_perpetuity_cash_flow
            DPCF = (DFCFn*(1+long_fcf_growth_rate)) / (discount_rate - long_fcf_growth_rate)
            #print 'DPCF:',DPCF
            DFCFn = 0   # don't add to sum
        else:
            sum_of_DFCFn += DFCFn
            #print 'FCF',n,'=',FCFn
            #print 'DFCF',n,'=',DFCFn
            #print 'Sum of DFCFn =',sum_of_DFCFn

    intrinsic_value = (sum_of_DFCFn + DPCF)/shares_outstanding
    #print "Company: "+company_name
    #print "Intrinsic value = RM {0:.2f}" .format(intrinsic_value)

    dictObj.writeTo("Intrinsic value", intrinsic_value)
    # return intrinsic_value

def getSharesOutstanding(incomeObj):
    shares = getPast5Years("Diluted Shares Outstanding", incomeObj)
    return shares[0]    # get only the latest

def getCurrentPrice(incomeObj):
    financialsSoup = incomeObj.getSoup()

    #print financialsSoup.prettify('utf-8')
    for span_tag in financialsSoup.find_all('span'):
        if span_tag.has_attr('id'):
            #print span_tag['id']
            if span_tag['id'] == "quote_val":
                #print span_tag
                #print span_tag.contents[0]
                current_price = span_tag.contents[0]
                #print type(span_tag)
    return current_price

def getShortFcfGrowthRate(incomeObj, dictObj):
    netIncome = getPast5Years("Net Income", incomeObj)

    #print "Year 2011:", netIncome[4]
    #print "Year 2015:", netIncome[0]

    dictObj.writeTo("Net Income Year 2015", netIncome[0])
    dictObj.writeTo("Net Income Year 2014", netIncome[1])
    dictObj.writeTo("Net Income Year 2013", netIncome[2])
    dictObj.writeTo("Net Income Year 2012", netIncome[3])
    dictObj.writeTo("Net Income Year 2011", netIncome[4])

    # Equation as below. Rearrange to find short_fcf_growth_rate
    # netIncome[0] = netIncome[4]*(1+short_fcf_growth_rate)^4

    if netIncome[0] > 0 and netIncome[4] > 0:
        # cannot log -ve number
        temp1 = math.log10(float(netIncome[0])/float(netIncome[4]))
        temp2 = temp1/4
        short_fcf_growth_rate = math.pow(10, temp2)-1
        #print "Short term FCF growth rate: ",short_fcf_growth_rate
    else:
        short_fcf_growth_rate = 0
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
                #print tr_tag.td.contents[0]
                #print '!!!!!!!!!!!!!!!!!'

                value1 = tr_tag.td.next_sibling.next_sibling.string
                value2 = tr_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.string
                value3 = tr_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
                value4 = tr_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
                value5 = tr_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string

                #print value1    #latest
                #print value2
                #print value3
                #print value4
                #print value5    #5 years ago
                #print type(unicode(value1))

                retList_unicode.append(unicode(value1))
                retList_unicode.append(unicode(value2))
                retList_unicode.append(unicode(value3))
                retList_unicode.append(unicode(value4))
                retList_unicode.append(unicode(value5))

    for u in retList_unicode:

        i = u.replace(",","")   # remove comma from number
        #print i.translate("()")
        i = i.replace("(","-")  # ugly way to convert bracket number to -ve
        i = i.replace(")","")
        if i == "-":    # no data
            i = 0
        #print "i :",i
        #print type(i)
        retList_int.append(float(i))  # convert to float

    return retList_int

class Webpage:
    def __init__(self, pageURL):
        self.page_soup = None
        self.setSoup(pageURL)

    def setSoup(self, pageURL):
        print "Requesting webpage..."
        r = requests.get(pageURL)
        if r.status_code == requests.codes.ok:
            print "HTTP 200 OK"
            pageHTML = r.text.encode('utf-8')
            page_soup = BeautifulSoup(pageHTML, "html.parser")
        self.page_soup = page_soup

    def getSoup(self):
        return self.page_soup

class ReportDict:
    def __init__(self, header_list):
        self.output_dict = {}
        self.output_dict.fromkeys(header_list)    # init dictionary

    def writeTo(self, header, value):
        self.output_dict[header] = value

    def getDict(self):
        return self.output_dict

class CSV:
    def __init__(self, header_list):
        self.header_list = header_list
        with open("IntrinsicValue.csv", "wb") as f:
            for header in self.header_list:
                # write header line
                line = '{},'.format(header)
                f.write(line)

    def appendToCSV(self, outDict):
        with open("IntrinsicValue.csv", "a") as f:
            f.write("\n")
            for header in self.header_list:
                line = '{},'.format(outDict[header])
                f.write(line)

if __name__ == '__main__':
    main()

#----------------------------------------------------------------------
# Revision History  :
#
# Date           Author       Ref    Revision
# 23-Jul-2016    shianchin    1      Initial creation.
#
#----------------------------------------------------------------------