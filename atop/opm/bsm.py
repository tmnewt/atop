from scipy.stats import norm
from math import exp, log, sqrt

class BlackScholesOPM:
    '''Data container for Black-Scholes-Merton calculations
    
    Given the type of option (Call or Put), the option's underlying asset value,
    the contract's strike value, the annual volatility of the underlying, a 
    continuously compounded annual risk-free rate, and a length of time (in years)
    the class will generate and store all intermediate calculation values as well
    as various greek values associated with the option.
    
    Primary calculation is the option value.

    Currently does not support options where the underlying has intermediate cash
    flows such as a stock with a dividend payment. It will be implemented in the 
    future.'''
    def __init__(self, position: str, optype: str, 
                    underlying_value: float or int, 
                    strike_value: float or int, 
                    volatility: float, risk_free: float, 
                    time_in_years: float or int):
        
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
        self.time_in_years = time_in_years
        


        # Internal Calculations.
        self.d1 = self.d1_calc()
        self.d2 = self.d2_calc()
        self.n1 = self.normcdf_calc()[0]
        self.n2 = self.normcdf_calc()[1]

        self.value = self.value_calc()
        
        # greeks
        self.delta = self.delta_calc()
        self.gamma = self.gamma_calc()
        self.theta = self.theta_calc()
        #self.vega = self.vega_calc()
        #self.rho = self.rho_calc()

        # dev note:
        # Additional values can be calculated such as the discount factor: exp(-self.risk_free * self.time_in_years),
        # but that wouldn't be a 'true' annual discount factor... which might confuse people. 
        # Additionally, saving the sqrt(self.time_in_years) because it's used multiple times.
        # The efficiency gains might be substantial though.
        # But the cost is a bigger data container...
        # 
        # On another note:
        # Currently the class parameters can be changed. However the calculations will not update. Consider fixing this.

    def __repr__(self):
        text = '''\nData node of a Black-Scholes-Merton Model for a {op} option where the underlying is $ {under_p},
with a strike value of $ {strike_p}, an annual volatility of {vol}, a continuously-compounded 
risk-free rate of {rf}. The option expires in {years} years.'''.format(
                                                                    op = self.optype,
                                                                    under_p = self.underlying_value,
                                                                    strike_p = self.strike_value,
                                                                    vol = self.volatility,
                                                                    rf = self.risk_free,
                                                                    years = self.time_in_years
                                                                    )
        return text

    # internal class calculations.
    def d1_calc(self):
        return ((log(self.underlying_value/self.strike_value) + (self.risk_free + (self.volatility**2)/2)*self.time_in_years) / 
        (self.volatility * sqrt(self.time_in_years)))
        
    
    def d2_calc(self):
        return self.d1 - (self.volatility * sqrt(self.time_in_years))
    

    def normcdf_calc(self):
        if self.optype == 'Call':
            n1 = norm.cdf(self.d1)
            n2 = norm.cdf(self.d2)
        else: 
            # must be a put
            n1 = norm.cdf(-self.d1)
            n2 = norm.cdf(-self.d2)
        return [n1, n2]
    
    
    def value_calc(self):
        if self.optype == 'Call':
            value = self.underlying_value * self.n1 - self.strike_value * exp(-self.risk_free * self.time_in_years) * self.n2
        else: 
            #must be a put
            value = -self.underlying_value * self.n1 + self.strike_value * exp(-self.risk_free * self.time_in_years) * self.n2
        return value
    
    
    # the greeks
    def delta_calc(self):
        if self.optype == 'Call':
            delta = norm.cdf(self.d1)
        else:
            #must be a put
            delta = -norm.cdf(-self.d1)
        return delta

    
    def gamma_calc(self):
        return (1/(self.underlying_value*self.volatility*sqrt(self.time_in_years))) * norm.pdf(self.d1)
    
    
    def theta_calc(self):
        if self.optype == 'Call':
            theta = (-((self.underlying_value * norm.pdf(self.d1) * self.volatility)/(2 * sqrt(self.time_in_years))) 
            - self.risk_free * self.strike_value * exp(-self.risk_free*self.time_in_years) * norm.cdf(self.d2))
        else: 
            #must be a put
            theta = (-((self.underlying_value * norm.pdf(-self.d1) * self.volatility)/(2 * sqrt(self.time_in_years))) 
            + self.risk_free * self.strike_value * exp(-self.risk_free*self.time_in_years) * norm.cdf(-self.d2))
        return theta

    
    # recommend not using vega
    def vega_calc(self):
        if self.optype == 'Call':
            vega = self.underlying_value * norm.pdf(self.d1) * sqrt(self.time_in_years)
        else:
            #must be a put
            vega = self.strike_value * exp(-self.risk_free * self.time_in_years) * norm.pdf(self.d2) * sqrt(self.time_in_years)
        return vega
    
    
    # recommend not using rho
    def rho_calc(self):
        if self.optype == 'Call':
            pass
        else:
            pass
        return NotImplemented


    def get_value(self):
        return self.value




    def print_calc_values(self, rounding = 2, hide_greeks = False, hide_d_calc = False, hide_n_calc = False, hide_delta = False, hide_gamma = False, hide_theta = False):
        '''A nice terminal display for checking internal values
        
        Mainly used for debugging. Can also be used to show answers for problems.
        The greeks vega and rho are not implemented at this time.'''
        
        #hiding greeks
        if hide_greeks:
            hide_delta = True
            hide_gamma = True
            hide_theta = True
        
        print(self.__repr__())
        
        # rounding and heads up message 
        if hide_d_calc or hide_n_calc or hide_delta or hide_gamma or hide_theta:
            print('Display values are rounded to {} decimals.'.format(rounding))
            print('Additionally, some values are hidden!')
        else:
            print('Display values are rounded to {} decimals'.format(rounding))
        
        print('----------------')
        print('Internal Values')
        print('----------------')
        
        print('{} option value : ${}'.format(self.optype, round(self.value, rounding)))

        if hide_d_calc:
            pass
        else:
            print('d1 = {}'.format(round(self.d1, rounding)))
            print('d2 = {}'.format(round(self.d2, rounding)))

        if hide_n_calc:
            pass
        else:
            print('cumulative normal distribution using d1 = {}'.format(round(self.n1, rounding)))
            print('cumulative normal distribution using d2 = {}'.format(round(self.n2, rounding)))

        if hide_delta:
            pass
        else:
            print('greek delta = {}'.format(round(self.delta, rounding)))

        if hide_gamma:
            pass
        else:
            print('greek gamma = {}'.format(round(self.gamma, rounding)))

        if hide_theta:
            pass
        else:
            print('greek theta = {}'.format(round(self.theta, rounding)))
