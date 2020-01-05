from scipy.stats import norm
import math

def bsm_find_call_price(underlying_asset_price, strike_price, annual_volatility, annual_cc_risk_free, time_in_years = 1, annual_cc_dividend_yield = 0):
    
    
    
    d1 = (math.log(underlying_asset_price/strike_price) + (annual_cc_risk_free - annual_cc_dividend_yield + (annual_volatility**2)/2)*time_in_years)/(annual_volatility * math.sqrt(time_in_years))
    d2 = d1 - (annual_volatility * math.sqrt(time_in_years)) 

    # use d1 and d2 in a a cumulative standard normal distribution function
    n1 = norm.cdf(d1)
    n2 = norm.cdf(d2)

    # black-scholes-merton calculation: 
    price = underlying_asset_price * math.exp(-annual_cc_dividend_yield*time_in_years) * n1 - strike_price * math.exp(-annual_cc_risk_free*time_in_years)*n2
    
    return price


def bsm_find_put_price(underlying_asset_price, strike_price, annual_volatility, annual_cc_risk_free, time_in_years = 1, annual_cc_dividend_yield = 0):
    
    
    
    d1 = (math.log(underlying_asset_price/strike_price) + (annual_cc_risk_free - annual_cc_dividend_yield + (annual_volatility**2)/2)*time_in_years)/(annual_volatility * math.sqrt(time_in_years))
    d2 = d1 - (annual_volatility * math.sqrt(time_in_years)) 

    # use d1 and d2 in a a cumulative standard normal distribution function
    n1 = norm.cdf(-d1)
    n2 = norm.cdf(-d2)

    # black-scholes-merton calculation: 
    price = strike_price * math.exp(-annual_cc_risk_free*time_in_years) * n2 - underlying_asset_price * math.exp(-annual_cc_dividend_yield*time_in_years) * n1

    return price



#playing around.
# check to see if the following produces the correct results.
call_example = bsm_find_call_price(100, 110, 0.14247, 0.05, 1)
print('Call price : ${}'.format(call_example))

put_example = bsm_find_put_price(100, 110, 0.14247, 0.05, 1)
print('Put price : ${}'.format(put_example))


#double check by put-call parity:
putcall_check_1 = round(float(put_example) + 100.00 - 110.00/math.exp(0.05) - float(call_example), 10)
print('Put-call parity difference should be zero. calculations say: {}'.format(putcall_check_1))

# taken from a text book.
# check the dividend feature:
ex_call_with_dividends = bsm_find_call_price(1000, 1100, 0.14247, 0.06, 1, annual_cc_dividend_yield = 0.02)
print('Call price with dividends : ${}'.format(ex_call_with_dividends))

ex_put_with_dividends = bsm_find_put_price(1000, 1100, 0.14247, 0.06, 1, annual_cc_dividend_yield = 0.02)
print('Put price with dividends: ${}'.format(ex_put_with_dividends))


putcall_check_2 = float(ex_put_with_dividends) + 1000.00 - 1100.00/math.exp(0.06) - float(ex_call_with_dividends) -(0.02 * 1000)/math.exp(0.02)
print('Put-call parity difference should be zero. calculations say: {}'.format(putcall_check_2))

print('dangit...')
#another approach to put price using call price:
ex_put_with_dividends_repeat = ex_call_with_dividends - 1000*math.exp(-0.02*1) + 1100*math.exp(-0.06*1)
print(ex_put_with_dividends_repeat)
# everything works...
