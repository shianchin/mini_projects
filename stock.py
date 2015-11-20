import locale
locale.setlocale( locale.LC_ALL, '' )

import math

from decimal import *
getcontext().prec = 2

    
def main():
    price_per_share = 0.80   #in RM
    share_lot = 10000           #one lot = 100 shares
    
    gross_amount = price_per_share * share_lot * 100
    
    
    
    total_fee = fee_calculate(gross_amount)
    total_amount = gross_amount + total_fee
    
    #print locale.currency(total_amount)
    
    
    sell_fee = fee_calculate(total_amount)
    
    sell_total = total_amount + sell_fee
    
    
    sell_actual = total_amount + fee_calculate(sell_total)
    
    print "\nGross amount:"
    print "   total_amount = RM ", '{:>9}'.format('{:,.2f}'.format(total_amount))
    print "   sell_fee     = RM ", '{:>9}'.format('{:,.2f}'.format(sell_fee))
    print "   sell_total   = RM ", '{:>9}'.format('{:,.2f}'.format(sell_total))
    print "   sell_actual  = RM ", '{:>9}'.format('{:,.2f}'.format(sell_actual))
  

def fee_calculate(amount):
    brokerage_fee_rate = 0.42/100
    clearing_fee_rate = 0.03/1000
    gst_rate = 6.0/100
    
    
    if (amount * brokerage_fee_rate < 12.00):
        brokerage_fee = 12.00
    else:
        brokerage_fee = amount * brokerage_fee_rate
    
    print "\namount = ", amount
    contract_fee = int(amount / 1000) + 1
    clearing_fee = amount * clearing_fee_rate
    gst = (brokerage_fee + clearing_fee) * gst_rate
    
    total_fee = brokerage_fee + contract_fee + clearing_fee + gst
    
    print "\nFees: "
    print "   brokerage_fee = RM ", '{:>9}'.format('{:,.2f}'.format(brokerage_fee))
    print "   contract_fee  = RM ", '{:>9}'.format('{:,.2f}'.format(contract_fee))
    print "   clearing_fee  = RM ", '{:>9}'.format('{:,.2f}'.format(clearing_fee))
    print "   gst           = RM ", '{:>9}'.format('{:,.2f}'.format(gst))
    print "\n   total_fee     = RM ", '{:>9}'.format('{:,.2f}'.format(total_fee))
    return total_fee    

if __name__ == '__main__':
  main()