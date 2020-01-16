from math import sqrt, log, exp

class SinglePeriodOption:
    '''Single Period Binomial Option object

    Replicates part of the functionality of the BinomialOption class found 
    in the options directory. This class is newer and more simple to use. 
    Great for demonstrating single period binomial option pricing model 
    without having to worry about complex topics like volatility, actual
    probability, or time! This is only for educational purposes. '''

    def __init__(self, position: str, optype: str,
                    underlying_value: int or float,
                    strike_value: int or float, up_value: int or float,
                    down_value: int or float, risk_free: int or float,
                    underlying_name = 'YBM'):
        self.position =         position    
        self.optype =           optype
        self.underlying_value = underlying_value
        self.strike_value =     strike_value
        self.up_value =         up_value
        self.down_value =       down_value
        self.risk_free =        risk_free
       
        
        
        # internal calculations
        self.__pos_eff =     self.__position_effect_calc()
        self.up_payoff =     self.__up_payoff_calc()
        self.down_payoff =   self.__dn_payoff_calc()
        
        # the 'meat' of the problem
        self.hedge_ratio =   self.__hedge_calc()
        self.rf_units =      self.__rf_units_calc()
        self.value =         self.__value_calc()
        
        #Technically, extra stuff
        #risk neutral probabilites. 
        self.up_risk_neutral_prob =     self.__up_risk_neutral_calc()
        self.down_risk_neutral_prob =   self.__dn_risk_neutral_calc()
        self.volatility =               self.__volatility_calc()


        # underlying name is optional. Used in the guide
        # Defaults to 'YBM' (Your Beloved Machine)...
        self.underlying_name = underlying_name


    def __position_effect_calc(self):
        if self.position == 'Long':
            return 1   # makes no change to the calculations
        else:
            return -1  # will carry through to make the value negative, which
                       # reflects the cash inflow from shorting 

    def __up_payoff_calc(self):
        if self.optype == 'Call':
            return max(self.up_value - self.strike_value, 0) * self.__pos_eff
        else:
            return max(self.strike_value - self.up_value, 0) * self.__pos_eff

    def __dn_payoff_calc(self):
        if self.optype == 'Call':
            return max(self.down_value - self.strike_value, 0) *self.__pos_eff
        else:
            return max(self.strike_value - self.down_value, 0) *self.__pos_eff

    def __hedge_calc(self):
        return ((self.up_payoff - self.down_payoff)
                /(self.up_value - self.down_value))

    def __rf_units_calc(self):
        return (1/(1+self.risk_free)
         *(self.up_payoff-(self.hedge_ratio*self.up_value)))

    def __value_calc(self):
        return self.hedge_ratio*self.underlying_value + self.rf_units

    def __up_risk_neutral_calc(self):
        return (((1+self.risk_free)*(self.underlying_value)-self.down_value)
                            /(self.up_value-self.down_value))
    
    def __dn_risk_neutral_calc(self):
        return 1-self.up_risk_neutral_prob
    
    def __up_factor(self):
        return self.up_value/self.underlying_value
    
    def __dn_factor(self):
        return self.down_value/self.underlying_value
    
    def __volatility_calc(self):
        box = []
        box.append(1-sqrt(1+2*(self.risk_free-log(self.__up_factor())))) #works
        box.append(1+sqrt(1+2*(self.risk_free-log(self.__up_factor())))) #works...
        
        box.append(abs(1+sqrt(1+2*(self.risk_free-log(self.__dn_factor())))/-1)) 
        # prior is equivalent to: sqrt( (1+(2*self.risk_free)) + 2*log(self.underlying_value/self.down_value))-1
        
        box.append((1+sqrt(1+2*(self.risk_free-log(self.__dn_factor()))))/-1) 
        # prior equivalent to: -sqrt( (1+(2*self.risk_free)) + 2*log(self.underlying_value/self.down_value))-1
        # which is a slightly different approach.
        return box
    
    def __sanity_check(self, sigma):
        upf = exp(self.risk_free - (sigma**2 / 2) + sigma)
        dnf = exp(self.risk_free - (sigma**2 / 2) - sigma)
        return [upf, dnf]

    # 'poking' values and seeing how things change.
    def poke_underlying(self):
        return NotImplemented
    
    def poke_strike(self):
        return NotImplemented
    
    def poke_risk_free(self):
        return NotImplemented

    
    def get_value(self):
        return self.value

        
    
    def __print_helper(self): #helper func for guide()
        if self.optype == 'Long':
            print('Going long means purchasing the {} option'.format(
                self.position))
            if self.optype == 'Call':
                print('''   Buying a call gives you the RIGHT but NO OBLIGATION to PURCHASE the underlying
    asset {name} FOR the strike price of ${strike} ({name}'s value is currently trading at ${under})

    These facts are important for 2 reasons for a long call contract:
    First, because this contract gives you the RIGHT to purchase {name} at ${strike}, if 
    {name} moves higher than the strike price of ${strike} then the value of this call 
    option (that is, its price) increases. So, when {name}\'s price > ${strike} 
    then this contract becomes more valuable! If contract matures with {name}\'s price > ${strike}
    then the value of the contract is the difference in {name}\'s price - strike.

    Second, because this contract requires NO OBLIGATION on your part to buy {name} at ${strike}, 
    if {name}\'s price remains lower than the strike price of ${strike} then you 
    are free to walk away. So, while {name}\'s price < ${strike} then this contract 
    becomes worth less and less. If 
    
    These feature are what makes call options special.
    What this all means is there is potential for huge upside if {name}\'s is higher than
    ''')

            else:
                print('''   Buying a put gives you the RIGHT to SELL the underlying asset at
    the strike price. But you have NO OBLIGATION to exercise 
    this right if the underlying > strike. This means you have 
    unlimited upside and limited downside.''')

        else:
            print('Shorting means selling the option (a.k.a writing an option)')
    
    

    # Guide that walks through the pricing like its a homework problem.
    def guide(self, rounding = 2, hide_solution = False):
        
        # message about input values
        # Some visual padding
        print('=======================================')
        print('  SINGLE PEIORD BINOMIAL {} {} '.format(
            self.position, self.optype))
        print('=======================================')
        
        print('''Given a single period {pos} {opt} where the underlying value
is {stock_p}, with a strike value of {strike_p}, an up value of {up}, a down 
value of {down}, and a risk free rate of {rf} what is the price of this option?

Note: All display values are rounded to {rnd} decimal places. However, all
calculations are precise.
'''.format(
                            pos = self.position,
                            opt = self.optype,
                            stock_p = round(self.underlying_value, 2),
                            strike_p = round(self.strike_value, 2),
                            up = round(self.up_value, 2),
                            down = round(self.down_value, 2),
                            rf = round(self.risk_free, 3),
                            rnd = rounding)
                            )
        
        # Still in the print_calc_values function
        print('-------------------')
        print('Pricing Solution')
        print('-------------------')

        print('{} {} value: $ {}'.format(self.position, self.optype,
                round(self.value, rounding))
                )
        
        if hide_solution:
            pass
        else:
            print('''Remember: all options are agreements between two parties who are legally bound
to perform as specified by their agreement. So think of the word \'Option\' as the same thing as
'contract'. Further, these contracts are standardized with well defined and agreed upon clauses 
and language. Therefor the agreements can easily be transferred to others (third-parties) with (tradeable).

The two parties to this contract One side is the buyer of the option and on the other
side is the person writing the option (a.k.a the seller).
    ''')
            print('Recall that this a {} option'.format(self.optype))
            self.__print_helper()
            
            print('First, find the payoffs in the up and down state:')
            print('For the up payoff: up_value - underlying')
            print('        up payoff: {}'.format(
                                self.up_payoff))
            print('')
            print('Up state payoff is {} and down state payoff is {}'.format(
                round(self.up_payoff, rounding),
                round(self.down_payoff, rounding))
                )
            
            print('~~~~~~')
            print('Proof')
            print('~~~~~~')
            print('Hedge Ratio (a.k.a units of underlying): {}'.format(
                round(self.hedge_ratio, rounding))
                )
            
            print('Value of bond position for hedging purposes: $ {}'.format(
                round(self.rf_units, rounding))
                )

        
            print('Risk-neutral probability for up state is {}'.format(
                round(self.up_risk_neutral_prob, rounding)))
            print('Risk-neutral probability for down state is {}'.format(
                round(self.down_risk_neutral_prob, rounding)))

            print('Problem\'s up factor: {}'.format(self.__up_factor()))
            print('Problem\'s down factor: {}'.format(self.__dn_factor()))
            
            
            # Insane Sanity check
            
            print('\n Sanity Check')

            print(self.volatility)

            print('Up factor: {}'.format(self.__sanity_check(self.volatility[0])[0]))
            print('Up factor: {}'.format(self.__sanity_check(self.volatility[1])[0]))
            print('Dn factor: {}'.format(self.__sanity_check(self.volatility[2])[1]))
            print('Dn factor: {}'.format(self.__sanity_check(self.volatility[3])[1]))
        print('____________________________________________________________\n')




    

#test   
#example = SinglePeriodOption('Long','Call', 100, 110, 120, 90.25, 0.05)
#print(example.value)
#example = SinglePeriodOption('Short','Call', 100, 110, 120, 90.25, 0.05)
#print(example.value)
#example = SinglePeriodOption('Long','Put', 100, 110, 120, 90.25, 0.05)
#print(example.value)
#example = SinglePeriodOption('Short','Put', 100, 110, 120, 90.25, 0.05)
#print(example.value)
# cool, it works.

#additional tests.
example = SinglePeriodOption('Short','Call', 95, 110, 120, 90.25, 0.05)
example.guide()
    