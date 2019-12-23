import AllThingsOptions.BinomialOption as BinOption

class CallOption(BinOption):
    def __init__(self, stock_price, strike_price, up_price, down_price, risk_free, override_up_payoff = None, override_down_payoff = None):

        up_payoff = override_up_payoff
        down_payoff = override_down_payoff
        
        if (not override_up_payoff):
            up_payoff = max(self.up_price - self.strike_price, 0)
            
        if (not override_down_payoff):
            down_payoff = max(self.down_price - self.strike_price, 0)

        super().__init__(stock_price, strike_price, up_price, down_price, risk_free, up_payoff, down_payoff)

    def __repr__(self):
        return "CALL"
    
