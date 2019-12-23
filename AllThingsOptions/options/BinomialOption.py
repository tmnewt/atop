class BinomialOption:
    '''Creates a single-period two-state option object, by default, a call option.
        
        Object calculates price (premium) of single-period option of an arbitrary time period
        Requires current underlying stock price, strike price, price in up state,
        price in down state, risk free rate.
        
        The risk free rate used should reflect the actual rate of interest earned during the time period.
        For instance, if the option is for 6 months, enter the calculated interest rate earned in those 6 months.

        By default, period payoffs for both up and down states are calculated internally.
        User can override these calculated payoffs by passing their own values.
        This is useful for calculating an 'inner' single period of a much larger multi-period option pricing model.
        Consider that the payoffs are not the possible stock values at some arbitrary time before maturity but 
        instead the price of the next binomial period option. 
        '''
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
    def print_calc_values(self, rounding = 2, hide_hegde_ratio = False, hide_risk_free_units = False, hide_state_payoffs = False, hide_risk_neutral_probabilites = False):
        

        # provides a message to user if any field is hidden.
        if hide_hegde_ratio or hide_risk_free_units or hide_state_payoffs or hide_risk_neutral_probabilites:
            headsup = 'Additionally, not all calculated fields are displayed!'
        else:
            headsup = ''

        overide_message = ''
        if self.overridden:
            overide_message = '\nUSER HAS OPTED TO OVERRIDE PAYOFF VALUES! BE AWARE THIS WILL AFFECT CALCULATIONS!'
        
        # message about inputed values
        # Some visual padding
        print('===============================================================================')
        print('  INFORMATION FOR A SINGLE PEIORD {} OPTION USING BINMOMIAL PRICING METHOD'.format(self))
        print('===============================================================================')
        
        print('''\nThe calculations below are for a single period {op_type} option where the underlying value is {stock_p}, 
with a strike price of {strike_p}, an up price of {up}, a down price of {down}, and a risk free rate of {rf}%.
All outputs are rounded to {rnd} decimal places. {hdsup} {ovride_msg}\n'''.format(op_type = self,
                                                                                stock_p = self.stock_price,
                                                                                strike_p = self.strike_price,
                                                                                up = self.up_price,
                                                                                down = self.down_price,
                                                                                rf = self.risk_free,
                                                                                rnd = rounding,
                                                                                hdsup = headsup,
                                                                                ovride_msg = overide_message ))
        
        # Still in the print_calc_values function
        print('--------------')
        print('Calculations')
        print('--------------')
        
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
            print('Calculated risk neutral probability for up state is {} and for down state risk neutral probability is {}'.format(round(self.up_risk_neutral_prob, rounding), 
                                                                                                                                    round(self.down_risk_neutral_prob, rounding)))
        print('_____________________________________________________________________________________________________________\n')

















    