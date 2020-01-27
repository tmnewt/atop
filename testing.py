# showcasing the classes

from atop.opm.npbopm import NPeriodBOPM
from atop.opm.bsmopm import BlackScholesOPM
from atop.opm.onepbopm import OnePeriodBOPM

from atop.teaching.singleperiod import SinglePeriodClassic


# n-period binomial option pricing model.
print('N-period binomial pricing model examples:')
n_period_example = NPeriodBOPM('Long', 'Call', 100, 110, 0.14247, 0.05, 2, 1)
print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}') 

n_period_example = NPeriodBOPM('short', 'Call', 100, 110, 0.14247, 0.05, 2, 1)
print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}')

n_period_example = NPeriodBOPM('Long', 'put', 100, 110, 0.14247, 0.05, 2, 1)
print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}')

n_period_example = NPeriodBOPM('short', 'put', 100, 110, 0.14247, 0.05, 2, 1)
print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}')

n_period_example = NPeriodBOPM('long', 'call', 100, 110, 0.14247, 0.05, 500, 1)
print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}')

n_period_example = NPeriodBOPM('short', 'call', 100, 110, 0.14247, 0.05, 500, 1)
print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}')

n_period_example = NPeriodBOPM('long', 'put', 100, 110, 0.14247, 0.05, 500, 1)
print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}')

n_period_example = NPeriodBOPM('short', 'put', 100, 110, 0.14247, 0.05, 500, 1)
print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}\n')

print('diminishing calculation change for using more periods illustration:')

n_period_example = NPeriodBOPM('long', 'call', 100, 110, 0.14247, 0.05, 500, 1)
print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}')

n_period_example = NPeriodBOPM('long', 'call', 100, 110, 0.14247, 0.05, 1000, 1)
print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}')

n_period_example = NPeriodBOPM('long', 'call', 100, 110, 0.14247, 0.05, 5000, 1)
print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}')

n_period_example = NPeriodBOPM('long', 'call', 100, 110, 0.14247, 0.05, 10000, 1)
print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}')

#n_period_example = NPeriodBOPM('long', 'call', 100, 110, 0.14247, 0.05, 20000, 1)
#print(f'{n_period_example.nperiods} period {n_period_example.position} {n_period_example.optype}: {n_period_example.get_value():.5f}')


# Observe:
print('\nBlack-Scholes-Merton option pricing model examples:')
bsm_example = BlackScholesOPM('Long', 'Call', 100, 110, 0.14247, 0.05, 1)
print(f'{bsm_example.position} {bsm_example.optype}: {bsm_example.get_value():.5f}')

bsm_example = BlackScholesOPM('short', 'Call', 100, 110, 0.14247, 0.05, 1)
print(f'{bsm_example.position} {bsm_example.optype}: {bsm_example.get_value():.5f}')

bsm_example = BlackScholesOPM('long', 'put', 100, 110, 0.14247, 0.05, 1)
print(f'{bsm_example.position} {bsm_example.optype}: {bsm_example.get_value():.5f}')

bsm_example = BlackScholesOPM('short', 'put', 100, 110, 0.14247, 0.05, 1)
print(f'{bsm_example.position} {bsm_example.optype}: {bsm_example.get_value():.5f}\n')




# Back to more simple stuff:
print('\nOnePeriodBOPM examples:')
# Using the class `OnePeriodBOPM` 
one_period_example = OnePeriodBOPM('Long', 'Call', 100, 110, 0.14247, 0.05)
print(f'{one_period_example.position} {one_period_example.optype}: {one_period_example.get_value():.5f}')

one_period_example = OnePeriodBOPM('short', 'Call', 100, 110, 0.14247, 0.05)
print(f'{one_period_example.position} {one_period_example.optype}: {one_period_example.get_value():.5f}')

one_period_example = OnePeriodBOPM('Long', 'Put', 100, 110, 0.14247, 0.05)
print(f'{one_period_example.position} {one_period_example.optype}: {one_period_example.get_value():.5f}')

one_period_example = OnePeriodBOPM('short', 'Put', 100, 110, 0.14247, 0.05)
print(f'{one_period_example.position} {one_period_example.optype}: {one_period_example.get_value():.5f}')


# Back to the NPeriodBOPM:
print('\nForcing NPeriodBOPM to be 1 period examples:')
# We can also force it to behave like the single period binomial pricing tool!
nperiod_example = NPeriodBOPM('Long', 'Call', 100, 110, 0.14247, 0.05, 1, 1)
print(f'{nperiod_example.position} {nperiod_example.optype}: {nperiod_example.get_value():.5f}') 

nperiod_example = NPeriodBOPM('short', 'call', 100, 110, 0.14247, 0.05, 1, 1)
print(f'{nperiod_example.position} {nperiod_example.optype}: {nperiod_example.get_value():.5f}')

nperiod_example = NPeriodBOPM('Long', 'Put', 100, 110, 0.14247, 0.05, 1, 1)
print(f'{nperiod_example.position} {nperiod_example.optype}: {nperiod_example.get_value():.5f}')

nperiod_example = NPeriodBOPM('short', 'Put', 100, 110, 0.14247, 0.05, 1, 1)
print(f'{nperiod_example.position} {nperiod_example.optype}: {nperiod_example.get_value():.5f}\n')



print('''by the way: because of numpy broadcasting nature we
can't capture the changes in the pricing array. To get around this,
there is a \'step-in\' method''')
print('\nNPeriodBOPM step in:')
nperiod_example = NPeriodBOPM('Long', 'Call', 100, 110, 0.14247, 0.05, 4, 1)
nperiod_example.value_calc_step_in()


#from atop.options.calloption import CallOption 

# The CallOption and PutOption class handle single period options whose 
# underlying values are known for the next time period. The options price 
# is calculated using a single period binomial option pricing model (BOPM).
# Example
#binomial_call = CallOption(100, 110, 120, 90.25, 0.0513)
#print(binomial_call.option_price)
#
## The classes internally calculate the payoff states
#print('Up Payoff: {}'.format(binomial_call.up_payoff))
#print('Down Payoff: {}'.format(binomial_call.down_payoff))
## The class also solves for the hedge-ratio, the risk-free units, 
## and the risk-neutral probabilies.
#print('Hedge-ratio: {}'.format(binomial_call.hedge_ratio))
#print('Risk-free units: {}'.format(binomial_call.rf_units))
#print('Up risk-neutral probability: {}'.format(
#                                    binomial_call.up_risk_neutral_prob))
#print('Down risk-neutral probability: {}'.format(  
#                                    binomial_call.down_risk_neutral_prob))
#
## All of this information is wrapped up in a nice little terminal output
## function called print_calc_values() which has parameters to hide answers 
## to internal calculations. Rounding defaults to 2 decimal points
#binomial_call.print_calc_values()
#print("Same input but hiding answers to internal calculations")
#binomial_call.print_calc_values(rounding=4, 
#                                hide_hedge_ratio=True, 
#                                hide_risk_free_units=True)
#
#
#
## A significant limitation is these classes can't handle volatility.
## Instead they rely on 'knowing' the next periods underlying value.
#
#
#
## Lastly, these classes do have a useful feature in 'overriding' payoff
## states, which allows for building out a n-period binomial tree. 
## Properly 'chaining' these options can generate a price for an n-period
## binomial price.  
#
## example of 2 period binomial option price (see multiperiod notebook)
#nodeT1up = CallOption(110, 110, 121, 104.50, 0.05)
#nodeT1down = CallOption(95, 110, 104.50, 90.25, 0.05)
#nodeT0 = CallOption(100, 110, 110, 95, 0.05, 
#                    nodeT1up.option_price, nodeT1down.option_price)
#nodeT0.print_calc_values()
# I actually hate these classes. They are the oldest and poorly constructed.
# All their issues are addressed in other classes. Speaking of which: