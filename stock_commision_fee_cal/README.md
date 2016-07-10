# Stock sell/buy/breakeven price calculator

Usage:
1. Run stock.py
2. Enter 1st input: {sell | buy | breakeven} 
3. Enter 2nd input: {Share price in RM} 
4. Enter 3rd input: {Amount of share in Lot}

Transaction costs taken from:
http://www.bursamalaysia.com/market/securities/equities/trading/transaction-costs/


Logic of breakeven code:
1. run buy algorithm
2. get total amount due
3. set to total amount due in sell algorithm
4. unknown new gross amount <- find this


-----------In math term:-----------
t_a_d = new_g_a - t_f
Rearranging:
new_g_a = t_a_d + t_f       # equation 1

t_f = b_a + c_s + c_f + gst                     # total_fee = sum of all fees
    = b_a + c_s + c_f + (b_a + c_f)(0.06)       # assuming gst_rate = 6%
    = b_a(1 + 0.06) + c_s + c_f(1 + 0.06)
    = (b_a + c_f)(1.06) + c_s
    = [b_a + (new_g_a + b_a + c_s)(0.0003)](1.06) + c_s     # assuming clearing_fee_rate = 0.03%
    = [b_a + new_g_a(0.0003) + b_a(0.0003) + c_s(0.0003)](1.06) + c_s
    = [b_a(1 + 0.0003) + (new_g_a + c_s)(0.0003)](1.06) + c_s
    = b_a(1.0003)(1.06) + new_g_a(0.0003)(1.06) + c_s(0.0003)(1.06) + c_s       

Rearranging:    
t_f - new_g_a(0.0003)(1.06) = b_a(1.0003)(1.06) + c_s[(0.0003)(1.06) + 1]       # equation 2

For L.H.S., substitute equation 1 into equation 2:
t_f - new_g_a(0.0003)(1.06) = t_f - (t_a_d + t_f)(0.0003)(1.06)
                        = t_f - t_f(0.0003)(1.06) - t_a_d(0.0003)(1.06)
                        = t_f[1 - (0.0003)(1.06)] - t_a_d(0.0003)(1.06)
Therefore,
t_f[1 - (0.0003)(1.06)] - t_a_d(0.0003)(1.06) = b_a(1.0003)(1.06) + c_s[(0.0003)(1.06) + 1]
t_f(0.999682) - t_a_d(0.000318) = b_a(1.060318) + c_s(1.000318)
t_f(0.999682) = b_a(1.060318) + c_s(1.000318) + t_a_d(0.000318)
t_f = [b_a(1.060318) + c_s(1.000318) + t_a_d(0.000318)] / (0.999682)    #Use this to calculate total_fee if brokerage_amount = 12

if b_a > 12:
Substitue b_a = (new_g_a)(b_r)
              = (t_a_d + t_f)(b_r)
Thus,
t_f(0.999682) = (t_a_d + t_f)(b_r)(1.060318) + c_s(1.000318) + t_a_d(0.000318)
t_f(0.999682) - (t_f)(b_r)(1.060318) = (t_a_d)(b_r)(1.060318) + c_s(1.000318) + t_a_d(0.000318)
t_f[0.999682 - (b_r)(1.060318)] = t_a_d[(b_r)(1.060318) + 0.000318] + c_s(1.000318) 
t_f = {t_a_d[(b_r)(1.060318) + 0.000318] + c_s(1.000318)} / [0.999682 - (b_r)(1.060318)]    #Use this to calculate total_fee if brokerage_amount > 12


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

....i give up. See above math terms instead of actual variables.