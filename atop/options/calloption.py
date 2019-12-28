from atop.options.binomialoption import BinomialOption

class CallOption(BinomialOption):
    def __init__(self, stock_price, strike_price, up_price, down_price, risk_free, override_up_payoff = None, override_down_payoff = None, override = False):

        up_payoff = override_up_payoff
        down_payoff = override_down_payoff
        
        
        if override_up_payoff == None:
            up_payoff = max(up_price - strike_price, 0)
        else: override = True

        if (not override_down_payoff):
            down_payoff = max(down_price - strike_price, 0)
        else:
            override = True

        super().__init__(stock_price, strike_price, up_price, down_price, risk_free, up_payoff, down_payoff, override)

    def __repr__(self):
        return "CALL"
    
