#!/usr/bin/env python

#**********************************************************************
# Project           : Stock commision fee calculator
#
# File name         : stock.py
#
# Author            : Cheang Shian Chin
#
# Date created      : 20 Nov 2015
#
# Purpose           : Calculate stock sell/buy fees and breakeven price.
#
# Revision History  :
#
# Date           Author       Ref    Revision
# 10-Jul-2016    shianchin    2      Prompt user input, set max stamp duty 
#                                    and clearing fee.
# 20-Nov-2015    shianchin    1      Initial creation.
#
#**********************************************************************

def main():
    action = raw_input('{sell | buy | breakeven}: ')
    price_per_share = raw_input('Price per share in RM: ')
    share_lot = raw_input('How many lots ( 1 lot = 100 shares): ')
    
    price_per_share = float(price_per_share)   # in RM
    share_lot = int(share_lot)         # 1 lot = 100 shares
    
    gross_amount = price_per_share * share_lot * 100
    
    
    print "\n    Buy/Sell/Breakeven     ", '{:>9}'.format(action.upper())
    print "    Quantity          =    ", '{:>9}'.format('{:,}'.format(share_lot * 100))
    print "    Price             = RM ", '{:>9}'.format('{:,.6f}'.format(price_per_share))     
    print "    Gross amount      = RM ", '{:>9}'.format('{:,.2f}'.format(gross_amount))
    
    if (action == 'buy'):
        total_amount_due = buy(gross_amount, action)
        print "\n    TOTAL AMOUNT DUE  = RM ", '{:>9}'.format('{:,.2f}'.format(total_amount_due))
    elif (action == 'sell'):
        total_amount_due = sell(gross_amount, action)
        print "\n    TOTAL AMOUNT DUE  = RM ", '{:>9}'.format('{:,.2f}'.format(total_amount_due))
    elif (action == 'breakeven'):
        price_per_share = breakeven(gross_amount, price_per_share, share_lot, action)
        print "\n    Breakeven price   = RM ", '{:>9}'.format('{:,.6f}'.format(price_per_share))


def buy(gross_amount, action):    
    total_fee = fee_calculate(gross_amount, action)
    total_amount_due = gross_amount + total_fee

    return total_amount_due
  
def sell(gross_amount, action):
    total_fee = fee_calculate(gross_amount, action)
    total_amount_due = gross_amount - total_fee

    return total_amount_due

def breakeven(gross_amount, price_per_share, share_lot, action):
    total_amount_due = buy(gross_amount, action)
    
    #TODO: Might want to consolidate these constants with fee_calculate()
    brokerage_rate = 0.42/100
    clearing_fee_rate = 0.03/100
    gst_rate = 6.0/100
            
    contract_stamp = int(total_amount_due / 1000) + 1    # might have problem when gross amount is near boundary of thousand 
    
    if (contract_stamp > 200):
        contract_stamp = 200    #Max stamp duty = RM200

        
    if (total_amount_due < 2873.78):    #For anything less than RM2873.78, min brokerage fee is RM12
        brokerage_amount = 12.00
        total_fee = (((brokerage_amount)*(clearing_fee_rate + 1)*(gst_rate + 1) 
                        + (contract_stamp)*((clearing_fee_rate)*(gst_rate + 1) + 1)
                        + (total_amount_due)*(clearing_fee_rate)*(gst_rate + 1)) / (1 - (clearing_fee_rate)*(gst_rate + 1)))
        
        #t_f = [b_a(1.060318) + c_s(1.000318) + t_a_d(0.000318)] / (0.999682)
    else:
        total_fee = ((total_amount_due * (brokerage_rate*(clearing_fee_rate + 1)*(gst_rate + 1) 
                        + (clearing_fee_rate)*(gst_rate + 1)) 
                        + contract_stamp*((clearing_fee_rate)*(gst_rate + 1) + 1)) / ((1 - (clearing_fee_rate)*(gst_rate + 1)) 
                        - brokerage_rate*(clearing_fee_rate + 1)*(gst_rate + 1)))
        
        #t_f = [t_a_d[(b_r)(1.060318) + 0.000318] + c_s(1.000318)] / [0.999682 - (b_r)(1.060318)]
   
    new_gross_amount = total_amount_due + total_fee
 
    price_per_share = new_gross_amount / (share_lot * 100)
    
    #for debug
    #print "total_fee from breakeven = ", total_fee
    #print "gross_amount breakeven = ", new_gross_amount
    #print "price_per_share", price_per_share
    
    return price_per_share


def fee_calculate(gross_amount, action):
    brokerage_rate = 0.42/100
    clearing_fee_rate = 0.03/100
    gst_rate = 6.0/100
    
    brokerage_amount = gross_amount * brokerage_rate
    
    if (brokerage_amount < 12.00):
        brokerage_amount = 12.00
    
    contract_stamp = int(gross_amount / 1000) + 1     
    
    if (contract_stamp > 200):
        contract_stamp = 200    #Max stamp duty = RM200

    clearing_fee = (gross_amount + brokerage_amount + contract_stamp) * clearing_fee_rate

    if (clearing_fee > 1000):
        clearing_fee = 1000     #Max clearing fee = RM1000
    
    gst = (brokerage_amount + clearing_fee) * gst_rate
    
    total_fee = brokerage_amount + contract_stamp + clearing_fee + gst
    
    #for debug
    #total_fee_2 = (brokerage_amount)*(clearing_fee_rate + 1)*(gst_rate + 1) + (gross_amount)*(clearing_fee_rate)*(gst_rate + 1) + (contract_stamp)*(clearing_fee_rate)*(gst_rate + 1) + contract_stamp
    #print "total_fee_2 = ", total_fee_2
    
    if (action == 'buy' or action == 'breakeven'):
        total_excl_gst = gross_amount + total_fee - gst
    elif (action == 'sell'):
        total_excl_gst = gross_amount - total_fee + gst
    
    if (action != 'breakeven'):    
        print "\nFees: "
        print "    Brokerage rate    =    ", '{:>9}'.format('{:.2%}'.format(brokerage_rate))
        print "    Brokerage amount  = RM ", '{:>9}'.format('{:,.2f}'.format(brokerage_amount))
        print "    Contract stamp    = RM ", '{:>9}'.format('{:,.2f}'.format(contract_stamp))
        print "    Clearing fees     = RM ", '{:>9}'.format('{:,.2f}'.format(clearing_fee))
        print "    TOTAL (EXCL GST)  = RM ", '{:>9}'.format('{:,.2f}'.format(total_excl_gst))
        print "    GST payable       = RM ", '{:>9}'.format('{:,.2f}'.format(gst))
        print "    TOTAL FEE DUE     = RM ", '{:>9}'.format('{:,.2f}'.format(total_fee))    
    
    return total_fee    

if __name__ == '__main__':
  main()