from atop.simpleops.simpleoption import SimpleOption

class SimplePut(SimpleOption):
    def __init__(self, stock_price, strike, up_price, down_price, risk_free):
        
        up_payoff = max(strike - up_price, 0)
        down_payoff = max(strike - down_price, 0)

        super().__init__(stock_price, strike, up_price, down_price, up_payoff, down_payoff, risk_free)