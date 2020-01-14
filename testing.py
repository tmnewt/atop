# showcasing the classes

from atop.options.calloption import CallOption 
from atop.options.putoption import PutOption
from atop.options.nperiodbopm import NPeriodBOPM
from atop.blackscholes.bsmnode import BsmNode

# The CallOption and PutOption class handle single period options whose 
# underlying values are known for the next time period. The options price 
# is calculated using a single period binomial option pricing model (BOPM).
# Example
binomial_call = CallOption(100, 110, 120, 90.25, 0.0513)
print(binomial_call.option_price)

# The classes internally calculate the payoff states
print('Up Payoff: {}'.format(binomial_call.up_payoff))
print('Down Payoff: {}'.format(binomial_call.down_payoff))
# The class also solves for the hedge-ratio, the risk-free units, 
# and the risk-neutral probabilies.
print('Hedge-ratio: {}'.format(binomial_call.hedge_ratio))
print('Risk-free units: {}'.format(binomial_call.rf_units))
print('Up risk-neutral probability: {}'.format(
                                    binomial_call.up_risk_neutral_prob))
print('Down risk-neutral probability: {}'.format(  
                                    binomial_call.down_risk_neutral_prob))

# All of this information is wrapped up in a nice little terminal output
# function called print_calc_values() which has parameters to hide answers 
# to internal calculations. Rounding defaults to 2 decimal points
binomial_call.print_calc_values()
print("Same input but hiding answers to internal calculations")
binomial_call.print_calc_values(rounding=4, 
                                hide_hedge_ratio=True, 
                                hide_risk_free_units=True)



# A significant limitation is these classes can't handle volatility.
# Instead they rely on 'knowing' the next periods underlying value.



# Lastly, these classes do have a useful feature in 'overriding' payoff
# states, which allows for building out a n-period binomial tree. 
# Properly 'chaining' these options can generate a price for an n-period
# binomial price.  

# example of 2 period binomial option price (see multiperiod notebook)
nodeT1up = CallOption(110, 110, 121, 104.50, 0.05)
nodeT1down = CallOption(95, 110, 104.50, 90.25, 0.05)
nodeT0 = CallOption(100, 110, 110, 95, 0.05, 
                    nodeT1up.option_price, nodeT1down.option_price)
nodeT0.print_calc_values()

# I actually hate these classes. They are the oldest and poorly constructed.
# All their issues are addressed in other classes. Speaking of which:

# Example of more compact n-period binomial option pricing model.
two_period_call = NPeriodBOPM('Call', 100, 110, 0.14247, 0.05, 2, 1)
print(two_period_call.get_price())

# Can also use this for valuing puts
two_period_put = NPeriodBOPM('Put', 100, 110, 0.14247, 0.05, 2, 1)
print(two_period_put.get_price())

# Those examples calculated the up & down factors using Jarrow-Rudd
# specification. But we can also use the Cox-Ross-Rubinstein specification.

cox_example = NPeriodBOPM('Call', 100, 110, 0.14247, 0.05, 2, 1, 'Cox')
print(cox_example.get_price())  # notice the different price.

# We can add even more periods! Here is 10,000 time periods.
two_period_put = NPeriodBOPM('Call', 100, 110, 0.14247, 0.05, 10000, 1)
print(two_period_put.get_price())

# that's pretty much the same answer given by the Black-Scholes-Merton model
# Observe:
bsm_example = BsmNode('Call', 100, 110, 0.14247, 0.05, 1)
print(bsm_example.price)