from math import sqrt, log

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
                    down_value: int or float, risk_free: int or float):
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
        holder = []
        holder.append(1-sqrt(1+2*(self.risk_free-log(self.__up_factor()))))
        holder.append(abs(1+sqrt(1+2*(self.risk_free-log(self.__dn_factor())))/-1))
        return holder
    
    # 'poking' values and seeing how things change.
    def poke_underlying(self):
        return NotImplemented
    
    def poke_strike(self):
        return NotImplemented
    
    def poke_risk_free(self):
        return NotImplemented

    
    def get_value(self):
        return self.value

    
    # Guide that walks through the pricing like its a homework problem.
    def print_guide(self, 
                        rounding = 2, 
                        hide_solution = False, 
                        ):
        
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
calculations are precise. Negative values reflect selling (aka short) an asset.
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
            
            print('Up state payoff is {} and down state payoff is {}'.format(
                round(self.up_payoff, rounding),
                round(self.down_payoff, rounding))
                )
            
            print('~~~~~~')
            print('Proof')
            print('~~~~~~')
            print('Hedge Ratio (units of underlying): {}'.format(
                round(self.hedge_ratio, rounding))
                )
            
            print('Value of bond position for hedging purposes: $ {}'.format(
                round(self.rf_units, rounding))
                )

            

        
        
            print('Risk-neutral probability for up state is {}'.format(
                round(self.up_risk_neutral_prob, rounding)))
            print('Risk-neutral probability for down state is {}'.format(
                round(self.down_risk_neutral_prob, rounding)))
        print('____________________________________________________________\n')




    

#test   
example = SinglePeriodOption('Long','Call', 100, 110, 120, 90.25, 0.05)
print(example.value)
#example = SinglePeriodOption('Short','Call', 100, 110, 120, 90.25, 0.05)
#print(example.value)
#example = SinglePeriodOption('Long','Put', 100, 110, 120, 90.25, 0.05)
#print(example.value)
#example = SinglePeriodOption('Short','Put', 100, 110, 120, 90.25, 0.05)
#print(example.value)
# cool, it works.

#additional tests.
print(example.volatility)
    