from math import exp, sqrt
import numpy as np


class NPeriodBOPM:

    def __init__(self, op_type, 
                        underlying, strike, 
                        volatility, risk_free, 
                        periods_in_year, time_in_years, 
                        trade_position = 'Long', 
                        factor_method = 'Jarrow'
                        ):
        
        self.op_type = op_type
        self.underlying = underlying
        self.strike = strike
        self.volatility = volatility
        self.risk_free = risk_free
        self.periods_in_year = periods_in_year
        self.time_in_years = time_in_years
        self.trade_position = trade_position
        self.factor_method = factor_method

        # internal calculations
        self.deltatime = self.__deltatime_calc()

        # when using Jarrow-Rudd specification
        if self.factor_method == 'Jarrow':
            self.upfactor = self.__jarrow_calc()[0]
            self.downfactor = self.__jarrow_calc()[1]
            self.up_neutral = self.__jarrow_calc()[2]
            self.down_neutral = self.__jarrow_calc()[3]

        # when using Cox-Ross-Rubinstein specification:
        if self.factor_method == 'Cox':
            self.upfactor = self.__cox_calc()[0]
            self.downfactor = self.__cox_calc()[1]
            self.up_neutral = self.__cox_calc()[2]
            self.down_neutral = self.__cox_calc()[3]


        self.underlying_set = self.__underlying_evolution_calc()


    # internal calc

    def __deltatime_calc(self):
        return self.time_in_years / self.periods_in_year

    def __jarrow_calc(self):   
        up_factor = exp(self.risk_free*self.deltatime - ((self.volatility**2) / 2) * self.deltatime + self.volatility*sqrt(self.deltatime))
        dn_factor = exp(self.risk_free*self.deltatime - ((self.volatility**2) / 2) * self.deltatime - self.volatility*sqrt(self.deltatime))       
        
        # The risk-neutral probabilites
        up_neutral = (exp(self.risk_free * self.deltatime) - dn_factor) / (up_factor - dn_factor)
        dn_neutral = 1-up_neutral
        return (up_factor, dn_factor, up_neutral, dn_neutral)

    def __cox_calc(self):
        up_factor = exp(self.volatility*sqrt(self.deltatime))
        dn_factor = 1/up_factor

        # The risk-neutral probabilites
        up_neutral = (exp(self.risk_free * self.deltatime) - dn_factor) / (up_factor - dn_factor)
        dn_neutral = 1-up_neutral

        return (up_factor, dn_factor, up_neutral, dn_neutral)

    def __underlying_evolution_calc(self):
        underlying_values = np.array(
            [(self.underlying * self.upfactor**j * self.downfactor**(self.periods_in_year-j)) 
            for j in range(self.periods_in_year)]
        )
        return underlying_values


        



#test:
example = NPeriodBOPM('Call', 100, 104, 0.12, 0.05, 10, 1)
print(example.deltatime)