from atop.simpleops.simpleoption import SimpleOption

class SimpleCall(SimpleOption):
    def __init__(self, stock_price, strike, up_price, down_price, risk_free):
        
        up_payoff = max(up_price - strike, 0)
        down_payoff = max(down_price - strike, 0)

        super().__init__(stock_price, strike, up_price, down_price, up_payoff, down_payoff, risk_free)
