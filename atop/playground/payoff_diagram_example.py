import numpy as np
import matplotlib.pyplot as plt

# playground file.

# goal is to generate payoff values for any underlying value
# these will be used to plot the payoff diagrams.


# there are many different logical ways of approaching this problem...
# calls
def net_long_call_payoffs(strike, price):
    payoff_list = []
    for underlying in range(101):
        if underlying <= strike:     
            payoff = 0 - price
        else:       
            payoff = (underlying - strike) - price  
        payoff_list.append(payoff)
    return payoff_list

def net_short_call_payoffs(strike, price):
    payoff_list = []
    for underlying in range(101):
        if underlying <= strike:
            payoff = price
        else:
            payoff = price - (underlying - strike)
        payoff_list.append(payoff)
    return payoff_list

# puts
def net_long_put_payoffs(strike, price):
    payoff_list = []
    for underlying in range(101):
        if underlying <= strike:
            payoff = (strike - underlying) - price
        else:
            payoff = -price
        payoff_list.append(payoff)
    return payoff_list

def net_short_put_payoffs(strike, price):
    payoff_list = []
    for underlying in range(101):
        if underlying <= strike:
            payoff = price - (strike - underlying)
        else:
            payoff = price
        payoff_list.append(payoff)
    return payoff_list

# stocks
def net_long_stock_payoffs(buy_price, broker_fee):
    payoff_list = []
    for underlying in range(101):
        payoff = underlying - buy_price - broker_fee
        payoff_list.append(payoff)
    return payoff_list


def net_short_stock_payoffs(sell_price, broker_fee):
    payoff_list = []
    for underlying in range(101):
        payoff = sell_price - underlying - broker_fee
        payoff_list.append(payoff)
    return payoff_list

# zero-coupon-bonds (arbitrary time)
def net_long_rf_payoffs(principal, rate):
    pass

def net_short_rf_payoffs(principal, rate):
    pass



#testing to make sure asset payoff calculation are correct.

#a = net_long_call_payoffs(40, 5.23)
#print(a) # eww. This is why I use numpy...
##works though

a = np.array(net_long_call_payoffs(40, 5.23))
b = np.array(net_short_call_payoffs(40, 5.23))
#print(b)
##works


c = np.array(net_long_put_payoffs(25, 3.22))
#print(c)
#works

d = np.array(net_short_put_payoffs(30, 2.59))
#print(d)
#works

#e = np.array(net_long_stock_payoffs(40, 0.04))
#f = np.array(net_short_stock_payoffs(20, 0.10))

x = np.arange(0, 101)

y = a + c


#plt.plot(x, a, label='Long Call')
#plt.plot(x, c, label='Long Put')
plt.plot(x, y, label='Together')
plt.axhline(y=0, color='r', linestyle='--')
#plt.plot(x, e, label='Long Stock')
#plt.plot(x, f, label='Short Stock')

plt.xlabel('Underlying Value')
plt.ylabel('Profit')
plt.legend()
plt.grid(True)
plt.show(block = True)



