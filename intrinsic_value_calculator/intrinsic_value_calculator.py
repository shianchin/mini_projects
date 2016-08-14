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
import csv
import datetime
import math
import re
import requests
import threading
import time

def main():
    #companyObj = Webpage("http://quotes.wsj.com/company-list/country/malaysia/1")
    #company_dict = getCompany(companyObj)
    #for k, v in company_dict.items():
    #    print k,v
    
    # FBM KLCI TOP 30 companies
    FBM_KLCI = [ "AMBANK"
               , "ASTRO"
               , "AXIATA"
               , "BAT"
               , "CIMB"
               , "DIGI"
               , "FGV"
               , "GENTING"
               , "GENM"
               , "HLBANK"
               , "HLFG"
               , "IHH"
               , "IOICORP"
               , "IOIPG"
               , "KLK"
               , "MAYBANK"
               , "MAXIS"
               , "MISC" #!!!!!!!
               , "PCHEM"
               , "PETDAG"
               , "PETGAS"
               , "PPB"
               , "PBBANK"
               , "RHBBANK"  #!!!!!!!
               , "SKPETRO"
               , "SIME"
               , "TM"
               , "TENAGA"
               , "UMW"
               , "YTL"]
    
    # FBM_KLCI = ["AMBANK",
    #             "TIMECOM",
    #             "VS",
    #             "DLADY"]

    # Lists (for exporting to csv purpose)
    header_list = ["Company",
            "FCF Year 2015","FCF Year 2014","FCF Year 2013","FCF Year 2012","FCF Year 2011","Average FCF",
            "Net Income Year 2015","Net Income Year 2014","Net Income Year 2013","Net Income Year 2012","Net Income Year 2011","FCF growth",
            "Short term duration","Discount rate","Long term growth rate",
            "Shares outstanding","Current price","Intrinsic value"]
    dictObj = ReportDict(header_list)
    csvObj = CSV(header_list)

    start_time = time.time()
    '''
    # Create and start the Thread objects.
    myThreads = []    # a list of all the Thread objects
    for company in FBM_KLCI:
        threadObj = threading.Thread(target=startProcess, args=[company, dictObj, header_list])
        myThreads.append(threadObj)
        threadObj.start()
    # Wait for all threads to end.
    for myThread in myThreads:
        threadObj.join()
    print('Done.')
    '''
    for company in FBM_KLCI:
        startProcess(company, dictObj, header_list, csvObj)
    end_time = time.time()
    delta_time = end_time - start_time
    print ("\nTime elapsed: {}m{:.2f}s".format(int(delta_time/60), delta_time%60))

def startProcess(company, dictObj, header_list, csvObj):  
    try:
        url_root = "http://quotes.wsj.com/MY/XKLS/"
        incomeObj = Webpage(url_root+company+"/financials/annual/income-statement")
        cashflowObj = Webpage(url_root+company+"/financials/annual/cash-flow")
        #financialsObj = Webpage(url_root+company+"/financials")
        dictObj.writeTo("Company", company)
        calcIntrinsicValue(incomeObj, cashflowObj, dictObj)
        csvObj.appendToCSV(dictObj.getDict())
        for header in header_list:
            print ("{} : {}".format(header, dictObj.getDictValue(header)))
            # print everything in order
    except IndexError:
        print ("ERROR: Data not available.")

def getCompany(companyObj):
    companySoup = companyObj.getSoup()
    count = 0
    company_dict = {}

    for td_tag in companySoup.find_all('td'):
        if td_tag.contents:
            if td_tag.contents[0].encode('utf-8') == "XKLS":
                count+=1
                name = td_tag.previous_sibling.previous_sibling.span.string
                link = td_tag.previous_sibling.previous_sibling.a.get('href')
                company_dict[name] = link
                
    return company_dict


def calcIntrinsicValue(incomeObj, cashflowObj, dictObj):
    #reference: http://www.buffettsbooks.com/howtoinvestinstocks/course3/intrinsic-value-formula.html
    FCF = getPast5Years("Free Cash Flow", cashflowObj)
    dictObj.writeTo("FCF Year 2015", "RM {}".format(FCF[0]))
    dictObj.writeTo("FCF Year 2014", "RM {}".format(FCF[1]))
    dictObj.writeTo("FCF Year 2013", "RM {}".format(FCF[2]))
    dictObj.writeTo("FCF Year 2012", "RM {}".format(FCF[3]))
    dictObj.writeTo("FCF Year 2011", "RM {}".format(FCF[4]))

    average_fcf = int(sum(FCF)/len(FCF))    #MYR (NOT rounded to millions/thousands)

    short_fcf_growth_rate = getShortFcfGrowthRate(incomeObj, dictObj)

    # What do you consider short term (most common is 10 years)?
    short_term = 10    #years

    # What discount rate to use?
    discount_rate = 0.1

    # After the 10th year, what percent (whole number) will the company continue to
    # grow into perpetuity (recommend 3% or lower)?
    long_fcf_growth_rate = 0.03
    shares_outstanding = int(getSharesOutstanding(incomeObj))    #NOT rounded to millions/thousands
    current_price = float(getCurrentPrice(incomeObj))

    dictObj.writeTo("Average FCF", "RM {}".format(average_fcf))
    dictObj.writeTo("FCF growth", "{:.2%}".format(short_fcf_growth_rate))
    dictObj.writeTo("Short term duration", "{} years".format(short_term))
    dictObj.writeTo("Discount rate", "{:.2%}".format(discount_rate))
    dictObj.writeTo("Long term growth rate", "{:.2%}".format(long_fcf_growth_rate))
    dictObj.writeTo("Shares outstanding", "{:} shares".format(shares_outstanding))
    dictObj.writeTo("Current price", "RM {:.2f}".format(current_price))

    #DFCFn = 0   # discounted free cash flow at year N
    sum_of_DFCFn = 0
    
    # formula refers to buffettsbooks.com
    for n in range(1,short_term+1):
        sum_of_DFCFn += (average_fcf * (1 + short_fcf_growth_rate)**n) / (1 + discount_rate)**n
    
    # Discounted Free Cash Flow at (short_term + 1)
    DFCF_last = ((average_fcf * (1 + short_fcf_growth_rate)**(short_term + 1)) / (1 + discount_rate)**(short_term + 1))
    # Discounted Perpetuity Cash Flow
    DPCF = DFCF_last * (1 + long_fcf_growth_rate) / (discount_rate - long_fcf_growth_rate)

    intrinsic_value = (sum_of_DFCFn + DPCF)/shares_outstanding
    #print "Intrinsic value = RM {0:.2f}" .format(intrinsic_value)

    dictObj.writeTo("Intrinsic value", "RM {:.2f}".format(intrinsic_value))
    # return intrinsic_value

def getSharesOutstanding(incomeObj):
    shares = getPast5Years("Diluted Shares Outstanding", incomeObj)
    return shares[0]    # get only the latest

def getCurrentPrice(incomeObj):
    financialsSoup = incomeObj.getSoup()

    for span_tag in financialsSoup.find_all('span'):
        if span_tag.has_attr('id'):
            if span_tag['id'] == "quote_val":
                current_price = span_tag.contents[0]
    return current_price

def getShortFcfGrowthRate(incomeObj, dictObj):
    netIncome = getPast5Years("Net Income", incomeObj)
    dictObj.writeTo("Net Income Year 2015", "RM {}".format(netIncome[0]))
    dictObj.writeTo("Net Income Year 2014", "RM {}".format(netIncome[1]))
    dictObj.writeTo("Net Income Year 2013", "RM {}".format(netIncome[2]))
    dictObj.writeTo("Net Income Year 2012", "RM {}".format(netIncome[3]))
    dictObj.writeTo("Net Income Year 2011", "RM {}".format(netIncome[4]))

    # Equation as below. Rearrange to find short_fcf_growth_rate
    # netIncome[0] = netIncome[4]*(1+short_fcf_growth_rate)^4

    if netIncome[0] > 0 and netIncome[4] > 0:
        # cannot log -ve number
        temp1 = math.log10(float(netIncome[0])/float(netIncome[4]))
        temp2 = temp1/4
        short_fcf_growth_rate = math.pow(10, temp2)-1
    else:
        short_fcf_growth_rate = 0
    return short_fcf_growth_rate

def getPast5Years(toFind, webObj):
    valList_unicode = []
    valList_int = []
    webSoup = webObj.getSoup()

    for th_tag in webSoup.find_all('th'):
        if th_tag.attrs:
            if re.search(r'All values MYR Millions', th_tag.string):
                rounding_factor = 1000000
            elif re.search(r'All values MYR Thousands', th_tag.string):
                rounding_factor = 1000
            else:
                rounding_factor = 1
                print ("Unknown rounding factor.")

    for tr_tag in webSoup.find_all('tr'):
        if tr_tag.td:
            if tr_tag.td.contents[0] == toFind:
                value1 = tr_tag.td.next_sibling.next_sibling    #latest
                value2 = value1.next_sibling.next_sibling
                value3 = value2.next_sibling.next_sibling
                value4 = value3.next_sibling.next_sibling
                value5 = value4.next_sibling.next_sibling       #5 years ago

                valList_unicode.append(value1.string)
                valList_unicode.append(value2.string)
                valList_unicode.append(value3.string)
                valList_unicode.append(value4.string)
                valList_unicode.append(value5.string)

    for u in valList_unicode:
        i = u.replace(",","")   # remove comma from number
        #print i.translate("()")
        i = i.replace("(","-")  # ugly way to convert bracket number to -ve
        i = i.replace(")","")
        if i == "-":    # no data
            i = 0
        valList_int.append(float(i)*rounding_factor)  # convert to float

    valList_int = [int(i) for i in valList_int]     # convert to int
    return valList_int

class Webpage:
    def __init__(self, pageURL):
        self.page_soup = None
        self.setSoup(pageURL)

    def setSoup(self, pageURL):
        print ("Requesting webpage...")
        r = requests.get(pageURL)
        if r.status_code == requests.codes.ok:
            print ("HTTP 200 OK")
            pageHTML = r.text.encode('utf-8')
            self.page_soup = BeautifulSoup(pageHTML, "html.parser")

    def getSoup(self):
        return self.page_soup

class ReportDict:
    def __init__(self, header_list):
        self.output_dict = {}
        self.output_dict.fromkeys(header_list)    # init dictionary

    def writeTo(self, header, value):
        self.output_dict[header] = value

    def getDictValue(self, header):
        return self.output_dict[header]

    def getDict(self):
        return self.output_dict

class CSV:
    def __init__(self, header_list):
        self.header_list = header_list
        timenow = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = "IntrinsicValue"+timenow+".csv"
        with open(self.filename, 'w', newline='') as f:
            wr = csv.writer(f)
            # write header line
            wr.writerows([self.header_list])
       
    def appendToCSV(self, outDict):
        with open(self.filename, "a") as f:
            for header in self.header_list:
                line = '{},'.format(outDict[header])    #use comma separator
                f.write(line)
            f.write("\n")

if __name__ == '__main__':
    main()

#----------------------------------------------------------------------
# Revision History  :
#
# Date           Author       Ref    Revision
# 14-Aug-2016    shianchin    3      Tweaked intrinsic calculation algorithm.
# 03-Aug-2016    shianchin    2      Update to Python 3.5.2
# 23-Jul-2016    shianchin    1      Initial creation.
#
#----------------------------------------------------------------------