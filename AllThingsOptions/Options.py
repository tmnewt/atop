class BinomialOption:
    def __init__(self, stock_price, strike_price, up_value, down_value, risk_free, option_type = 'Call'):
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.up_value = up_value
        self.down_value = down_value
        self.risk_free = risk_free
        self.option_type = option_type
        
        if option_type == 'Call':
            self.option_is_a_put = False
        if option_type == 'Put':
            self.option_is_a_put = True 

        
        # calculations done all at once.
        
        # flow control for call or put options
        # in the up state
        if self.option_is_a_put:
            # this mimics the up state payoff structure for a put 
            self.up_payoff = max(self.strike_price - self.up_value, 0)
        else:
            # this mimics the up payoff structure for a call 
            self.up_payoff = max(self.up_value - self.strike_price, 0) 
        
        # in the down state
        if self.option_is_a_put:
            # this mimics the down payoff structure for a put 
            self.down_payoff = max(self.strike_price - self.down_value, 0)
        else: 
            self.down_payoff = max(self.down_value - self.strike_price, 0)
        

        # 
        self.hedge_ratio =  (self.up_payoff - self.down_payoff)/(self.up_value - self.down_value)
        self.rf_units = (1/(1+self.risk_free))*(self.up_payoff-(self.hedge_ratio*self.up_value))

        #work back to present value. By no-arbitrage rules and replication this calculation is the option price. 
        self.option_price = self.hedge_ratio*self.stock_price + self.rf_units
        
        #risk neutral probabilites
        self.up_risk_neutral_prob = ((1+self.risk_free)*(self.stock_price)-self.down_value)/(self.up_value-self.down_value)
        self.down_risk_neutral_prob = 1-self.up_risk_neutral_prob

    # packed into a nice display function    
    def print_calc_values(self, rounding = 2, hide_hegde_ratio = False, hide_risk_free_units = False, hide_state_payoffs = False, hide_risk_neutral_probabilites = False):
        
        # provides a message to user if any field is hidden.
        if hide_hegde_ratio or hide_risk_free_units or hide_state_payoffs or hide_risk_neutral_probabilites:
            headsup = 'Additionally, NOT ALL FIELDS ARE DISPLAYED!'
        else:
            headsup = ''
        
        # message about inputed values
        print('''The following values are for a single period {} option where the underlying value is {}, a strike price of {}, an up value of {}, 
a down value of {}, and a risk free rate of {}%. All outputs are rounded to {} decimal places. {}'''.format(self.option_type, self.stock_price, self.strike_price, self.up_value, self.down_value, self.risk_free, rounding, headsup))

        print('''\n------------------------
{} Option Information
------------------------'''.format(self.option_type))
        
        print('Calculated Option Price: {}'.format(round(self.option_price, rounding)))
        
        if hide_hegde_ratio:
            pass
        else:
            print('Calculated Hedge Ratio: {}'.format(round(self.hedge_ratio, rounding)))

        if hide_risk_free_units:
            pass
        else:
            print('Calculated present value of bond position: {}'.format(round(self.rf_units, rounding)))

        if hide_state_payoffs:
            pass
        else:
            print('Up state payoff is {} and down state payoff is {}'.format(self.up_payoff, self.down_payoff))

        if hide_risk_neutral_probabilites:
            pass
        else: 
            print('Calculated risk neutral probability for up state is {} and for down state risk neutral probability is {}'.format(round(self.up_risk_neutral_prob, rounding), round(self.down_risk_neutral_prob, rounding)))


















    