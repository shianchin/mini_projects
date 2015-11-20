import sys

def main():
    if len(sys.argv) != 4:
        print 'HOW TO USE THIS: '
        print '     For Linux:'
        print '     ./stock.py {sell | buy | breakeven} {Share price in RM} {Amount of share in Lot}'
        print '     For Windows:'
        print '     python stock.py {sell | buy | breakeven} {Share price in RM} {Amount of share in Lot}'
        sys.exit(1)

    action = sys.argv[1]
    price_per_share = sys.argv[2]
    share_lot = sys.argv[3]
    
    print "Your first variable is:", action
    print "Your second variable is:", price_per_share
    print "Your third variable is:", share_lot
    
    price_per_share = float(price_per_share)   # in RM
    share_lot = int(share_lot)         # 1 lot = 100 shares
    
    gross_amount = price_per_share * share_lot * 100
    
    
    print "\n    Buy/Sell               ", '{:>8}'.format(action.upper())
    print "    Quantity          =    ", '{:>8}'.format('{:,}'.format(share_lot * 100))
    print "    Price             = RM ", '{:>8}'.format('{:,.6f}'.format(price_per_share))     
    print "    Gross amount      = RM ", '{:>8}'.format('{:,.2f}'.format(gross_amount))
    
    if (action == 'buy'):
        total_amount_due = buy(gross_amount, action)
    elif (action == 'sell'):
        total_amount_due = sell(gross_amount, action)
    
    print "\n    TOTAL AMOUNT DUE  = RM ", '{:>8}'.format('{:,.2f}'.format(total_amount_due))
    


    
        
def buy(gross_amount, action):
    total_fee = fee_calculate(gross_amount, action)
    total_amount_due = gross_amount + total_fee

    return total_amount_due
  
def sell(gross_amount, action):
    total_fee = fee_calculate(gross_amount, action)
    total_amount_due = gross_amount - total_fee

    return total_amount_due

#def breakeven(gross_amount, action):

"""
run buy code
get total amount due
set to total amount due in sell code

unknown gross amount <- find this

-----------In math term:-----------
t_a_d = g_a - t_f
Rearranging:
g_a = t_a_d + t_f       # equation 1

t_f = b_a + c_s + c_f + gst
    = b_a + c_s + c_f + (b_a + c_f)(0.06)       # assuming gst_rate = 6%
    = b_a(1 + 0.06) + c_s + c_f(1 + 0.06)
    = (b_a + c_f)(1.06) + c_s
    = [b_a + (g_a + b_a + c_s)(0.0003)](1.06) + c_s     # assuming clearing_fee_rate = 0.03%
    = [b_a + g_a(0.0003) + b_a(0.0003) + c_s(0.0003)](1.06) + c_s
    = [b_a(1 + 0.0003) + (g_a + c_s)(0.0003)](1.06) + c_s
    = b_a(1.0003)(1.06) + g_a(0.0003)(1.06) + c_s(0.0003)(1.06) + c_s       

Rearranging equation 2:    
t_f - g_a(0.0003)(1.06) = b_a(1.0003)(1.06) + c_s[(0.0003)(1.06) + 1]       # equation 2

For L.H.S., substitute equation 1 into equation 2:
t_f - g_a(0.0003)(1.06) = t_f - (t_a_d + t_f)(0.0003)(1.06)
                        = t_f - t_f(0.0003)(1.06) - t_a_d(0.0003)(1.06)
                        = t_f[1 - (0.0003)(1.06)] - t_a_d(0.0003)(1.06)
Therefore,
t_f[1 - (0.0003)(1.06)] - t_a_d(0.0003)(1.06) = b_a(1.0003)(1.06) + c_s[(0.0003)(1.06) + 1]
t_f(0.999682) - t_a_d(0.000318) = b_a(1.060318) + c_s(1.000318)
t_f(0.999682) - t_a_d(0.000318) = [b_a + c_s](1.000318)


-----------In term of actual variables:-----------
total_amount_due = gross_amount - total_fee
Thus, gross_amount = total_amount_due + total_fee

total_fee
= brokerage_amount + contract_stamp + clearing_fee + gst
= brokerage_amount + contract_stamp + clearing_fee + (brokerage_amount + clearing_fee) * gst_rate
= (brokerage_amount)(gst_rate + 1) + contract_stamp + (clearing_fee)(gst_rate + 1)
= (brokerage_amount + clearing_fee)(gst_rate + 1) + contract_stamp
= (brokerage_amount + (gross_amount + brokerage_amount + contract_stamp)*clearing_fee_rate)(gst_rate + 1) + contract_stamp
= (brokerage_amount + (gross_amount)(clearing_fee_rate) + (brokerage_amount)(clearing_fee_rate) + (contract_stamp)(clearing_fee_rate))(gst_rate + 1) + contract_stamp
= ((brokerage_amount)*(clearing_fee_rate + 1) + ((gross_amount) + (contract_stamp))*(clearing_fee_rate))*(gst_rate + 1) + contract_stamp
= (brokerage_amount)*(clearing_fee_rate + 1)*(gst_rate + 1) + (gross_amount)*(clearing_fee_rate)*(gst_rate + 1) + (contract_stamp)*(clearing_fee_rate)*(gst_rate + 1) + contract_stamp

total_fee - (gross_amount)*(clearing_fee_rate)*(gst_rate + 1) = (brokerage_amount)*(clearing_fee_rate + 1)*(gst_rate + 1) + (contract_stamp)*((clearing_fee_rate)*(gst_rate + 1) + 1)
"""

    
def fee_calculate(gross_amount, action):
    brokerage_rate = 0.42/100
    clearing_fee_rate = 0.03/100
    gst_rate = 6.0/100
    
    
    if (gross_amount * brokerage_rate < 12.00):
        brokerage_amount = 12.00
    else:
        brokerage_amount = gross_amount * brokerage_rate
    
    
    contract_stamp = int(gross_amount / 1000) + 1     #boundary condition not very sure; REMINDER: adjust this to max = 10
    clearing_fee = (gross_amount + brokerage_amount + contract_stamp) * clearing_fee_rate
    gst = (brokerage_amount + clearing_fee) * gst_rate
    
    total_fee = brokerage_amount + contract_stamp + clearing_fee + gst
    total_fee_2 = ((brokerage_amount)*(clearing_fee_rate + 1) + ((gross_amount) + (contract_stamp))*(clearing_fee_rate))*(gst_rate + 1) + contract_stamp
    print total_fee_2
    
    if (action == 'buy'):
        total_excl_gst = gross_amount + total_fee - gst
    elif (action == 'sell'):
        total_excl_gst = gross_amount - total_fee + gst
        
    print "\nFees: "
    print "    Brokerage rate    =    ", '{:>8}'.format('{:.2%}'.format(brokerage_rate))
    print "    Brokerage amount  = RM ", '{:>8}'.format('{:,.2f}'.format(brokerage_amount))
    print "    Contract stamp    = RM ", '{:>8}'.format('{:,.2f}'.format(contract_stamp))
    print "    Clearing fees     = RM ", '{:>8}'.format('{:,.2f}'.format(clearing_fee))
    print "    TOTAL (EXCL GST)  = RM ", '{:>8}'.format('{:,.2f}'.format(total_excl_gst))
    print "    GST payable       = RM ", '{:>8}'.format('{:,.2f}'.format(gst))
    print "    TOTAL FEE DUE     = RM ", '{:>8}'.format('{:,.2f}'.format(total_fee))    
    
    return total_fee    

if __name__ == '__main__':
  main()