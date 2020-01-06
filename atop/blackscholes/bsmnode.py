# don't create a parent class here. There is nothing to be gained doing that.

from scipy.stats import norm
from math import exp, log, sqrt

class BsmNode:
    '''Data container for Black-Scholes-Merton calculations
    
    Given the type of option (Call or Put), the option's underlying asset price,
    the contract's strike price, the annual volatility of the underlying, a 
    continuously compounded annual risk-free rate, and a length of time (in years)
    the class will generate and store all intermediate calculation values as well
    as various greek values associated with the option.
    
    Primary calculation is the option price.

    Currently does not support options where the underlying has intermediate cash
    flows such as a stock with a dividend payment. It will be implemented in the 
    future.'''
    def __init__(self, op_type, underlying, strike, volatility, risk_free, time_in_years):
        self.op_type = op_type
        self.underlying = underlying
        self.strike = strike
        self.volatility = volatility
        self.risk_free = risk_free
        self.time_in_years = time_in_years

        # Internal Calculations.
        self.d1 = self.d1_calc()
        self.d2 = self.d2_calc()
        self.n1 = self.normcdf_calc()[0]
        self.n2 = self.normcdf_calc()[1]

        self.price = self.price_calc()
        
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
with a strike price of $ {strike_p}, an annual volatility of {vol}, a continuously-compounded 
risk-free rate of {rf}. The option expires in {years} years.'''.format(
                                                                    op = self.op_type,
                                                                    under_p = self.underlying,
                                                                    strike_p = self.strike,
                                                                    vol = self.volatility,
                                                                    rf = self.risk_free,
                                                                    years = self.time_in_years
                                                                    )
        return text

    # internal class calculations.
    def d1_calc(self):
        return ((log(self.underlying/self.strike) + (self.risk_free + (self.volatility**2)/2)*self.time_in_years) / 
        (self.volatility * sqrt(self.time_in_years)))
        
    
    def d2_calc(self):
        return self.d1 - (self.volatility * sqrt(self.time_in_years))
    

    def normcdf_calc(self):
        if self.op_type == 'Call':
            n1 = norm.cdf(self.d1)
            n2 = norm.cdf(self.d2)
        else: 
            # must be a put
            n1 = norm.cdf(-self.d1)
            n2 = norm.cdf(-self.d2)
        return [n1, n2]
    
    
    def price_calc(self):
        if self.op_type == 'Call':
            price = self.underlying * self.n1 - self.strike * exp(-self.risk_free * self.time_in_years) * self.n2
        else: 
            #must be a put
            price = -self.underlying * self.n1 + self.strike * exp(-self.risk_free * self.time_in_years) * self.n2
        return price
    
    
    # the greeks
    def delta_calc(self):
        if self.op_type == 'Call':
            delta = norm.cdf(self.d1)
        else:
            #must be a put
            delta = -norm.cdf(-self.d1)
        return delta

    
    def gamma_calc(self):
        return (1/(self.underlying*self.volatility*sqrt(self.time_in_years))) * norm.pdf(self.d1)
    
    
    def theta_calc(self):
        if self.op_type == 'Call':
            theta = (-((self.underlying * norm.pdf(self.d1) * self.volatility)/(2 * sqrt(self.time_in_years))) 
            - self.risk_free * self.strike * exp(-self.risk_free*self.time_in_years) * norm.cdf(self.d2))
        else: 
            #must be a put
            theta = (-((self.underlying * norm.pdf(-self.d1) * self.volatility)/(2 * sqrt(self.time_in_years))) 
            + self.risk_free * self.strike * exp(-self.risk_free*self.time_in_years) * norm.cdf(-self.d2))
        return theta

    
    # recommend not using vega
    def vega_calc(self):
        if self.op_type == 'Call':
            vega = self.underlying * norm.pdf(self.d1) * sqrt(self.time_in_years)
        else:
            #must be a put
            vega = self.strike * exp(-self.risk_free * self.time_in_years) * norm.pdf(self.d2) * sqrt(self.time_in_years)
        return vega
    
    
    # recommend not using rho
    def rho_calc(self):
        if self.op_type == 'Call':
            pass
        else:
            pass
        return NotImplemented








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
        
        print('{} option price : ${}'.format(self.op_type, round(self.price, rounding)))

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
        
example = BsmNode('Call', 100, 110, 0.14247, 0.05, 1)
print(example.delta)
print(example.gamma)
example = BsmNode('Put', 100, 110, 0.14247, 0.05, 1)
print(example.delta)
print(example.gamma)
print(example.theta_calc())
example.print_calc_values()

