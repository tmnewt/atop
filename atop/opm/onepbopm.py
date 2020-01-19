from math import exp


class OnePeriodBOPM:

    def __init__(self, position: str, optype: str,
                    underlying_value: float or int,
                    strike_value: float or int,
                    volatility: float,
                    risk_free: float or int):
        self.position = position
        self.optype = optype
        self.underlying_value = underlying_value
        self.strike_value = strike_value
        self.volatility = volatility
        self.risk_free = risk_free
        
        # find stuff for next period
        self.upfactor = self.__jarrow_calc()[0]
        self.downfactor = self.__jarrow_calc()[1]
        self.up_neutral = self.__jarrow_calc()[2]
        self.down_neutral = self.__jarrow_calc()[3]

        
        # stuff for payoffs
        self.up_value  =     self.__next_period_up_value()
        self.down_value=     self.__next_period_dn_value()
        self.__pos_eff =     self.__position_effect_calc()
        self.up_payoff =     self.__up_payoff_calc()
        self.down_payoff =   self.__dn_payoff_calc()
        

        # the 'meat' of the problem
        self.hedge_ratio =   self.__hedge_calc()
        self.rf_units =      self.__rf_units_calc()
        self.value =         self.__value_calc()


    # the only factor calculator I trust for single periods
    def __jarrow_calc(self):   
        up_factor = exp(self.risk_free  
                        - ((self.volatility**2) / 2)  
                        + self.volatility)

        dn_factor = exp(self.risk_free  
                        - ((self.volatility**2) / 2)  
                        - self.volatility)       
        
        # The risk-neutral probabilites
        up_neutral = ((exp(self.risk_free) - dn_factor) 
                        / (up_factor - dn_factor))

        dn_neutral = 1-up_neutral
        return (up_factor, dn_factor, up_neutral, dn_neutral)
    

    def __next_period_up_value(self):
        return self.underlying_value * self.upfactor

    def __next_period_dn_value(self):
        return self.underlying_value * self.downfactor

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
    
    def get_value(self):
        return self.value

