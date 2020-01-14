# this code is outdated and should be ignored.
# will be removed sometime in the future.


class BinomialOption:
    
    def __init__(self, stock_price, strike_price, up_price, down_price, risk_free, up_payoff, down_payoff, overridden=False):
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.up_price = up_price
        self.down_price = down_price
        self.risk_free = risk_free
        self.up_payoff = up_payoff
        self.down_payoff = down_payoff
        self.overridden = overridden

        self.hedge_ratio =  (self.up_payoff - self.down_payoff)/(self.up_price - self.down_price)
        self.rf_units = (1/(1+self.risk_free))*(self.up_payoff-(self.hedge_ratio*self.up_price))

        #work back to present value. By no-arbitrage rules and replication this calculation is the option price. 
        self.option_price = self.hedge_ratio*self.stock_price + self.rf_units
        
        #risk neutral probabilites
        self.up_risk_neutral_prob = ((1+self.risk_free)*(self.stock_price)-self.down_price)/(self.up_price-self.down_price)
        self.down_risk_neutral_prob = 1-self.up_risk_neutral_prob



    # packed into a nice function to quickly display information   
    def print_calc_values(self, 
                        rounding = 2, 
                        hide_hedge_ratio = False, 
                        hide_risk_free_units = False, 
                        hide_state_payoffs = False, 
                        hide_risk_neutral_probabilites = False):
        

        # provides a message to user if any field is hidden.
        if hide_hedge_ratio or hide_risk_free_units or hide_state_payoffs or hide_risk_neutral_probabilites:
            headsup = 'Additionally, not all calculated fields are displayed!'
        else:
            headsup = ''

        overide_message = ''
        if self.overridden:
            overide_message = '\nUSER HAS OPTED TO OVERRIDE PAYOFF VALUES! BE AWARE THIS WILL AFFECT CALCULATIONS!'
        
        # message about input values
        # Some visual padding
        print('===============================================================================')
        print('  INFORMATION FOR A SINGLE PEIORD {} OPTION USING BINOMIAL PRICING METHOD'.format(self))
        print('===============================================================================')
        
        print('''\nThe calculations below are for a single period {op_type} option where the underlying value is {stock_p}, 
with a strike price of {strike_p}, an up price of {up}, a down price of {down}, and a risk free rate of {rf}.
All outputs are rounded to {rnd} decimal places. {hdsup} {overide_msg}\n'''.format(op_type = self,
                                                                                stock_p = round(self.stock_price, rounding),
                                                                                strike_p = round(self.strike_price, rounding),
                                                                                up = round(self.up_price, rounding),
                                                                                down = round(self.down_price, rounding),
                                                                                rf = round(self.risk_free, rounding),
                                                                                rnd = rounding,
                                                                                hdsup = headsup,
                                                                                overide_msg = overide_message ))
        
        # Still in the print_calc_values function
        print('--------------')
        print('Calculations')
        print('--------------')
        
        print('Calculated Option Price: $ {}'.format(round(self.option_price, rounding)))
        
        if hide_hedge_ratio:
            pass
        else:
            print('Calculated Hedge Ratio: {}'.format(round(self.hedge_ratio, rounding)))

        if hide_risk_free_units:
            pass
        else:
            print('Calculated present value of bond position: $ {}'.format(round(self.rf_units, rounding)))

        if hide_state_payoffs:
            pass
        else:
            print('Up state payoff is {} and down state payoff is {}'.format(round(self.up_payoff, rounding),
                                                                            round(self.down_payoff, rounding)))

        if hide_risk_neutral_probabilites:
            pass
        else: 
            print('Calculated risk-neutral probability for up state is {}'.format(round(self.up_risk_neutral_prob, rounding)))
            print('Calculated risk-neutral probability for down state is {}'.format(round(self.down_risk_neutral_prob, rounding)))
        print('________________________________________________________________________________________________________\n')

















    