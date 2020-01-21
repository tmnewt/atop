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
        self.value_vector = self.__value_calc()
        self.value = self.value_vector[0]

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

    def __value_calc(self):
        # Special thanks to cantaro86 for posting his solution on github
        value_vector = self.payoff_vector
        # find values
        for i in range(self.nperiods-1, -1, -1):
            value_vector[:-1] = (
                np.exp(-self.risk_free*self.deltatime)
                * (self.up_neutral * value_vector[1:]
                    + self.down_neutral * value_vector[:-1]))
        return value_vector

    def value_calc_step_in(self):
        # Special thanks to cantaro86 for posting his solution on github
        
        # find values
        if self.nperiods > 10:
            print('refuse to run more than 9 iterations for the step-in example!')
        else:
            underlying_step_in = np.array(
                [(self.underlying_value * self.upfactor**j * 
                self.downfactor**(self.nperiods-j)) 
                for j in range(self.nperiods + 1)])
            print('possible underlying end states:')
            print(underlying_step_in)

            print('calculating payoffs')
            payoffs_step_in = np.zeros(self.nperiods + 1) # get array going
            if self.optype == 'Call':
                payoffs_step_in[:] = np.maximum(underlying_step_in - self.strike_value, 0.0)
            else:
                payoffs_step_in[:] = np.maximum(self.strike_value - underlying_step_in, 0.0)
            print(payoffs_step_in)
            value_vector_step_in = payoffs_step_in
            
            print('copy payoff vector to value_vector')

            for i in range(self.nperiods-1, -1, -1):
                print('\nNEXT ITERATION')
                print('value_vector at start')
                print(value_vector_step_in)
                print(f'step 1: multiply last {self.nperiods} values in value vector by up_risk_neutral scalar')
                print(f'step 2: multiply first {self.nperiods} value in value vector by down_rik_neutral scalar')
                print('step 3: add product vectors together.')
                print('step 4: discount resulting vector by e^(-risk-free * deltatime)')
                value_vector_step_in[:-1] = (
                    np.exp(-self.risk_free*self.deltatime)
                    * (self.up_neutral * value_vector_step_in[1:]
                        + self.down_neutral * value_vector_step_in[:-1]))
                print('value_vector at end of iteration')
                print(value_vector_step_in)
            print('task completed')
            print(f'option value is at zero index: {value_vector_step_in[0]}')
        return
        
    def get_value(self):
        return self.value

        
#test:
#example = NPeriodBOPM('Call', 100, 100, 0.20, 0.10, 2000, 1)
#print(example.deltatime)
#print(example.upfactor)
#print(example.downfactor)
#print(example.underlying_value_vector)
#print(example.value_vector)
#print(example.value)
