from math import exp


class OnePeriodBOPM:

    def __init__(self, op_type, 
                        underlying_value, strike_value, 
                        volatility, risk_free,
                        trade_position = 'Long'):

        self.op_type = op_type
        self.underlying_value = underlying_value
        self.strike_value = strike_value
        self.volatility = volatility
        self.risk_free = risk_free
        self.trade_position = trade_position
        
        # find stuff for next period
        self.upfactor = self.__jarrow_calc()[0]
        self.downfactor = self.__jarrow_calc()[1]
        self.up_neutral = self.__jarrow_calc()[2]
        self.down_neutral = self.__jarrow_calc()[3]



        # internal calc
        self.__pos_eff =     self.__position_effect_calc()
        self.up_payoff =     self.__up_payoff_calc()
        self.down_payoff =   self.__dn_payoff_calc()
        


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
        return

    def __next_period_dn_value(self):
        return

    def get_price(self):
        return self.value