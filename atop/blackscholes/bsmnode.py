# don't create a parent class here. There is nothing to be gained doing that.

from scipy.stats import norm
from math import exp, log, sqrt

class BsmNode:
    def __init__(self, op_type, underlying, strike, volatility, risk_free, time_in_years):
        self.op_type = op_type
        self.underlying = underlying
        self.strike = strike
        self.volatility = volatility
        self.risk_free = risk_free
        self.time_in_years = time_in_years

        self.d1 = self.d1_calc()
        self.d2 = self.d2_calc()
        self.n1 = self.normcdf_calc()[0]
        self.n2 = self.normcdf_calc()[1]

        self.price = self.price_calc()

    # class calculations
    def d1_calc(self):
        return (log(self.underlying/self.strike) + (self.risk_free + (self.volatility**2)/2)*self.time_in_years)/(self.volatility * sqrt(self.time_in_years))
        
    def d2_calc(self):
        return self.d1 - (self.volatility * sqrt(self.time_in_years))
    
    def normcdf_calc(self):
        if self.op_type == 'Call':
            n1 = norm.cdf(self.d1)
            n2 = norm.cdf(self.d2)
        else: # must be a put
            n1 = norm.cdf(-self.d1)
            n2 = norm.cdf(-self.d2)
        return [n1, n2]
    
    
    def price_calc(self):
        if self.op_type == 'Call':
            price = self.underlying * self.n1 - self.strike * exp(-self.risk_free * self.time_in_years) * self.n2
        else: #must be a put
            price = -self.underlying * self.n1 + self.strike * exp(-self.risk_free * self.time_in_years) * self.n2
        return price
    


        
