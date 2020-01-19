from math import exp, sqrt
import numpy as np


class NPeriodBOPM:

    def __init__(self, position: str, optype: str, 
                    underlying_value: float or int, 
                    strike_value: float or int, 
                    volatility: float, risk_free: float, 
                    nperiods: int, time_in_years: float or int, 
                    factor_method = 'Jarrow'):
        
        position = position.lower().capitalize()
        if position == 'Long' or position == 'Short':
            self.position = position
        
        else:
            raise TypeError(f'''\n\n{position} does not describe a type of trade. Please input `long` or `short`
                when refering to what side of the trade you are on.''')
        
        optype = optype.lower().capitalize()
        if optype == 'Call' or optype == 'Put':
            self.optype = optype
        
        else:
            raise TypeError(f'''\n\nI've never heard of a {optype} type of option! Must be new...
                Please stick to either `Call` or `Put` type options!''')
        

        self.underlying_value = underlying_value
        self.strike_value = strike_value
        self.volatility = volatility
        self.risk_free = risk_free
        self.nperiods = nperiods
        self.time_in_years = time_in_years
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

        self.underlying_value_vector = self.__underlying_value_vector_calc()
        self.payoff_vector = self.__payoff_vector_calc()
        self.price_vector = self.__price_calc()
        self.value = self.price_vector[0]

    # internal calc

    def __deltatime_calc(self) -> float:
        return self.time_in_years / self.nperiods

    def __jarrow_calc(self):   
        up_factor = exp(self.risk_free*self.deltatime 
                        - ((self.volatility**2) / 2) * self.deltatime 
                        + self.volatility*sqrt(self.deltatime)
                        )

        dn_factor = exp(self.risk_free*self.deltatime 
                        - ((self.volatility**2) / 2) * self.deltatime 
                        - self.volatility*sqrt(self.deltatime)
                        )       
        
        # The risk-neutral probabilites
        up_neutral = (
            (exp(self.risk_free * self.deltatime) - dn_factor) 
                / (up_factor - dn_factor)
                    )

        dn_neutral = 1-up_neutral
        return (up_factor, dn_factor, up_neutral, dn_neutral)

    def __cox_calc(self):
        up_factor = exp(self.volatility*sqrt(self.deltatime))
        dn_factor = 1/up_factor

        # The risk-neutral probabilites
        up_neutral = ((exp(self.risk_free * self.deltatime) - dn_factor) 
                    / (up_factor - dn_factor) )
        dn_neutral = 1-up_neutral

        return (up_factor, dn_factor, up_neutral, dn_neutral)

    def __underlying_value_vector_calc(self):
        # Special thanks to cantaro86 for posting his solution on github
        underlying_vector = np.array(
            [(self.underlying_value * self.upfactor**j * 
            self.downfactor**(self.nperiods-j)) 
            for j in range(self.nperiods + 1)])
        return underlying_vector

    def __payoff_vector_calc(self):
        # Special thanks to cantaro86 for posting his solution on github
        payoffs = np.zeros(self.nperiods + 1) # get array going
        if self.optype == 'Call':
            payoffs[:] = np.maximum(self.underlying_value_vector - self.strike_value, 0.0)
        else:
            payoffs[:] = np.maximum(self.strike_value - self.underlying_value_vector, 0.0)
        return payoffs

    def __price_calc(self):
        # Special thanks to cantaro86 for posting his solution on github
        price_vector = self.payoff_vector
        # find prices
        for i in range(self.nperiods-1, -1, -1):
            price_vector[:-1] = (
                np.exp(-self.risk_free*self.deltatime)
                * (self.up_neutral * price_vector[1:]
                    + self.down_neutral * price_vector[:-1]))
        return price_vector
        
    def get_value(self):
        return self.value

        
#test:
#example = NPeriodBOPM('Call', 100, 100, 0.20, 0.10, 2000, 1)
#print(example.deltatime)
#print(example.upfactor)
#print(example.downfactor)
#print(example.underlying_value_vector)
#print(example.price_vector)
#print(example.price)
