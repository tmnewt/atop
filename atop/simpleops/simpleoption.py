class SimpleOption:
    '''Abstract class for a introducing 'simple' put and call option

    Replicates part of the functionality of the BinomialOption class found 
    in the options directory. This class is newer and more simple to use. 
    Great for demonstrating single period binomial option pricing model 
    without having to worry about complex topics like volatility, actual
    probability, or time! This is only for educational purposes. '''

    def __init__(self, stock_price, strike_price, up_price, down_price, up_payoff, down_payoff,  risk_free, trade_position = 'Long'):
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.up_price = up_price
        self.down_price = down_price
        self.up_payoff = up_payoff
        self.down_payoff = down_payoff
        self.risk_free = risk_free
        self.trade_position = trade_position

        self.hedge_ratio = self.hedge_calc()
        self.rf_units = self.rf_units_calc()
        self.price = self.price_calc()
        
        #risk neutral probabilites
        self.up_risk_neutral_prob = self.up_riskn_calc()
        self.down_risk_neutral_prob = self.dn_riskn_calc()

    def hedge_calc(self):
        return (self.up_payoff - self.down_payoff)/(self.up_price - self.down_price)

    def rf_units_calc(self):
        return (1/(1+self.risk_free))*(self.up_payoff-(self.hedge_ratio*self.up_price))

    def price_calc(self):
        return self.hedge_ratio*self.stock_price + self.rf_units

    def up_riskn_calc(self):
        return ((1+self.risk_free)*(self.stock_price)-self.down_price)/(self.up_price-self.down_price)
    
    def dn_riskn_calc(self):
        return 1-self.up_risk_neutral_prob