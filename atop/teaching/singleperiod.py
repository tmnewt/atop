from math import sqrt, log, exp


class SinglePeriodOption:
    '''Single Period Binomial Option object

    Replicates part of the functionality of the BinomialOption class found 
    in the options directory. This class is newer and more simple to use. 
    Great for demonstrating single period binomial option pricing model 
    without having to worry about complex topics like volatility, actual
    probability, or time! This is only for educational purposes. '''

    def __init__(self, position: str, optype: str,
                    underlying_value: int or float,
                    strike_value: int or float, up_value: int or float,
                    down_value: int or float, risk_free: int or float,
                    underlying_name = 'YBM'):
        self.position =         position    
        self.optype =           optype
        self.underlying_value = underlying_value
        self.strike_value =     strike_value
        self.up_value =         up_value
        self.down_value =       down_value
        self.risk_free =        risk_free
       
        
        
        # internal calculations
        self.__pos_eff =     self.__position_effect_calc()
        self.up_payoff =     self.__up_payoff_calc()
        self.down_payoff =   self.__dn_payoff_calc()
        
        # the 'meat' of the problem
        self.hedge_ratio =   self.__hedge_calc()
        self.rf_units =      self.__rf_units_calc()
        self.value =         self.__value_calc()
        
        #Technically, extra stuff
        #risk neutral probabilites. 
        self.up_risk_neutral_prob =     self.__up_risk_neutral_calc()
        self.down_risk_neutral_prob =   self.__dn_risk_neutral_calc()
        self.volatility =               self.__volatility_calc()


        # underlying name is optional. Used in the guide
        # Defaults to 'YBM' (Your Beloved Machine)...
        self.underlying_name = underlying_name


    def __position_effect_calc(self):
        if self.position == 'Long':
            return 1   # makes no change to the calculations
        else:
            return -1  # will carry through to make the value negative, which
                       # reflects the cash inflow from shorting 

    def __up_payoff_calc(self):
        if self.optype == 'Call':
            return max(self.up_value - self.strike_value, 0) * self.__pos_eff
        else:
            return max(self.strike_value - self.up_value, 0) * self.__pos_eff

    def __dn_payoff_calc(self):
        if self.optype == 'Call':
            return max(self.down_value - self.strike_value, 0) *self.__pos_eff
        else:
            return max(self.strike_value - self.down_value, 0) *self.__pos_eff

    def __hedge_calc(self):
        return ((self.up_payoff - self.down_payoff)
                /(self.up_value - self.down_value))

    def __rf_units_calc(self):
        return (1/(1+self.risk_free)
         *(self.up_payoff-(self.hedge_ratio*self.up_value)))

    def __value_calc(self):
        return self.hedge_ratio*self.underlying_value + self.rf_units

    def __up_risk_neutral_calc(self):
        return (((1+self.risk_free)*(self.underlying_value)-self.down_value)
                            /(self.up_value-self.down_value))
    
    def __dn_risk_neutral_calc(self):
        return 1-self.up_risk_neutral_prob
    
    def __up_factor(self):
        return self.up_value/self.underlying_value
    
    def __dn_factor(self):
        return self.down_value/self.underlying_value
    
    def __volatility_calc(self):
        box = []
        box.append(1-sqrt(1+2*(self.risk_free-log(self.__up_factor())))) #works
        box.append(1+sqrt(1+2*(self.risk_free-log(self.__up_factor())))) #works...
        
        box.append(abs(1+sqrt(1+2*(self.risk_free-log(self.__dn_factor())))/-1)) 
        # prior is equivalent to: sqrt( (1+(2*self.risk_free)) + 2*log(self.underlying_value/self.down_value))-1
        
        box.append((1+sqrt(1+2*(self.risk_free-log(self.__dn_factor()))))/-1) 
        # prior equivalent to: -sqrt( (1+(2*self.risk_free)) + 2*log(self.underlying_value/self.down_value))-1
        # which is a slightly different approach.
        return box
    
    def __sanity_check(self, sigma):
        upf = exp(self.risk_free - (sigma**2 / 2) + sigma)
        dnf = exp(self.risk_free - (sigma**2 / 2) - sigma)
        return [upf, dnf]

    # 'poking' values and seeing how things change.
    def poke_underlying(self):
        return NotImplemented
    
    def poke_strike(self):
        return NotImplemented
    
    def poke_risk_free(self):
        return NotImplemented

    
    def get_value(self):
        return self.value
    
    # generates a complete solution with choices to display certain information.
    def solution(self, skip_problem_display = False,
                hide_additional = False):
        
        # items that appear numerous times.
        pos=          self.position
        opt=          self.optype
        name=         self.underlying_name
        under=  round(self.underlying_value, 2)
        strike= round(self.strike_value, 2)
        up=     round(self.up_value, 2)
        down=   round(self.down_value, 2)
        rf=     round(self.risk_free, 2)
        

        # message about input values
        print(f'>>> SinglePeriodOption({pos}, {opt}, {under}, {strike}, {up}, {down}, {rf}, {name})')
        if skip_problem_display:
            print(f'{pos} {opt} value: $ {round(self.value,4)}')
            
        else:
            # Some visual padding
            print('\n=======================================')
            print(f'  SINGLE PERIOD BINOMIAL {pos} {opt}')
            print('=======================================')

            print(f'''\nGiven:
    A single period {pos} {opt} on the asset {name} whose current price is ${under}, with a 
    strike value of ${strike}. We know for certain  {name}\'s price will either be ${up}, 
    or ${down}, next period. The current risk-free rate is {rf}

What is the fair price for this {pos} {opt} today?''')                            
        
        # Still in the solution function
            print('\n--------------------------------------')
            print(f'  Answer: {pos} {opt}\'s value: $ {round(self.value,4)}')
            print('--------------------------------------')
            

            if hide_additional:
                pass
            else:
                print('\nIntermediate calculation answers:')
                print(f'\nProblem\'s up factor: {round(self.__up_factor(),4)}')
                print(f'Problem\'s down factor: {round(self.__up_factor(),4)}')
                print(f'Hedge Ratio (a.k.a units of underlying): {round(self.hedge_ratio,4)}')
                print(f'Value of bond position for hedging purposes: $ {round(self.rf_units,4)}')
                print(f'Risk-neutral probability for up state is {round(self.up_risk_neutral_prob,4)}')
                print(f'Risk-neutral probability for down state is {round(self.down_risk_neutral_prob,4)}')
        print('____________________________________________________________\n')

            



    # ahhhhhhhh this complete guide is taking forever to finish!
    # I hate strings...
    def guide(self, hide_what_is_an_option = False):

        # common values. Makes it easier to write guide.
        pos=          self.position
        opt=          self.optype
        name=         self.underlying_name
        under=  round(self.underlying_value, 2)
        strike= round(self.strike_value, 2)
        up=     round(self.up_value, 2)
        down=   round(self.down_value, 2)
        rf=     round(self.risk_free, 2)
        

        print('\n=======================================================')
        print(f'   Guide to finding price for {pos} {opt} on {name}')
        print('=======================================================')
        print(f'''{self.__guide_meta()}

WARNING: all versions of this guide are still being worked on.

 ----------
   Intro  
 ----------
This guide aims to provide users with a complete walkthrough of calculating 
 the fair price (today's price) for a single period binomial option. It's 
 aimed at those looking for a deep dive into the subject of options. This 
 guide goes all in, meticulously walking through every step of the process
 guiding the user to the solution. At times it can come accross as
 handholding and repetitive. But I argue that this is necessary as there are
 too many concepts and values to keep track. Sometimes we just need an 
 organized and thorough method of logically walking through problems.

This guide uses the terms `price` and `value` interchangablely. They are the 
 same thing. Additionally, you might see the program produce negative currency
 values. For instance, you may see the calculated value for a short call be,
 say, $ -2.50. Which seems weird. How can a price be negative? This is simply 
 an accounting style chosen to give logical consistency to the transactions. 
 It will become important later...''')
 
 #is important for correctly describing replicating portfolios. It comes from 
 #the perspective of the buyer who pays a physical x amount of money, which is
 #a positive cash outflow. Conversely the seller earns the premium x in the 
 #form of a negative outflow (which translates to a cash inflow). Don't 
 #worry if that sounds confusing now. 
 

        if hide_what_is_an_option:
            pass
        else:
            self.__whatare_guide()
        print('\n******************')
        print(f'  Walkthrough')
        print('******************')
        # String chunk
        print(f'''
These problems deal with a 2-state model. This is a very naive (but powerful)
model which assumes that there are only 2 possible future value states 
for the underlying asset {name}: An up state where {name}\'s price is {up}
and a down state where {name}\'s price is {down}. {name}\'s current price
is {under}. 

You might be wondering, where do these values come from? How do we know 
these values? The answer is, \'it\'s complicated...\' It will be  addressed
later. For now let's just settle with these 'magic' numbers. On thing at a time.

Our first objective is finding the payoff in each state. As you will see,
the calculated payoffs are vital in the pricing model. There are just a 
couple problems; each type of option has their own rules for describing
the potential payoffs in each state. And they change depending on which
side of the trade we are on.''')
        # End of string chunk

        if self.position == 'Long':
            #String chunk fpr Long
            print(f'''
\nIn this problem we are going long, meaning we are the buying party.
We are buying an option on {name}.''')
            # End of string chunk if Long
            
            if self.optype == 'Call':
                #String chunk for if call.
                print(f'''
Buying a Call gives you the RIGHT but NOT AN OBLIGATION to buy the underlying
 asset ({name}) for the strike price of ${strike} upon exercising the option. 
 {name}\'s value is currently trading at ${under}.

These facts are important for 2 reasons for a long call option:
 First, because you have the RIGHT to purchase {name} at ${strike}, if {name} 
 moves higher than the contract's strike price of ${strike} then the value 
 of this call option (that is, its price) increases. Suppose {name}\'s value
 rises from {under} to {up}. If you owned this call option, upon exercising it,
 you get to buy {name} at {strike}. You could turn around and sell it at the
 current market price of {up} and walk away with a payoff of ${up-strike:.2f}.
 To reiterate, when 
 {name}\'s price > ${strike} this contract becomes more valuable! If the 
 contract matures and {name}\'s price > ${strike} then the value of the 
 contract is the difference in {name}\'s price - strike.

Second, this contract requires NO OBLIGATION on your part to buy 
 {name} at ${strike}. If {name}\'s price remains lower than the strike 
 price of ${strike} then you are free to walk away! While {name}\'s price < 
 ${strike} then this contract becomes worth less and less. If the contract
 matures and {name}\'s price < ${strike} the value of this contract is 0. 
 Had you bought this contract you would only be out the premium you paid.
 Compare that to outright buying the underlying asset in which case you
 would sustain further losses. 
    
These features are what makes call options special. Holders of these contracts
 have no participation in the performance of {name}, yet benifit if {name} does
 well, but are protected in the event of a downturn. There is unlimited 
 upside potential but limited downside potential!
{self.__binomial_reminder()} 

payoffs = max( underlying_given_state - strike, 0)

Which translates to:
{self.__payoff_guide_helper()}



Long Call guide not finished''')

            else: # must be a put
                print(f'''
Buying a PUT gives you the RIGHT but NOT AN OBLIGATION to sell the underlying
 asset ({name}) for the strike price of ${strike} upon exercising the option.
{name}\'s value is currently trading at ${under}.
 
These facts are important for 2 reasons for a long put option:
 First, because you have the RIGHT to purchase {name} at ${strike}, if {name} 
 moves higher than the contract's strike price of ${strike} then the value 
 of this call option (that is, its price) increases. To restate, when 
 {name}\'s price > ${strike} this contract becomes more valuable! If the 
 contract matures and {name}\'s price > ${strike} then the value of the 
 contract is the difference in {name}\'s price - strike.
 
 
 Long Put guide not finished''')


        else: # must be a short
            if self.optype == 'Call':
                print(f'''Short Call guide not finished''')
            else: # must be a put
                print(f'''Short Put guide not finished''')
        
        print('This guide is still being worked on')
        
        
        
        #print('\n Sanity Check')
        #print(self.volatility)
        #print('Up factor: {}'.format(self.__sanity_check(self.volatility[0])[0]))
        #print('Up factor: {}'.format(self.__sanity_check(self.volatility[1])[0]))
        #print('Dn factor: {}'.format(self.__sanity_check(self.volatility[2])[1]))
        #print('Dn factor: {}'.format(self.__sanity_check(self.volatility[3])[1]))
        
        
        print('____________________________________________________________\n')
    # End of guide class method

    def __whatare_guide(self):
        
        
        whatare_text = '''
 --------------------
   What are options?  
 --------------------
Options are a type of contractual agreements between two parties who are 
 legally bound to perform as specified by their agreement. 
 
Some common contractual features of options:
  *  An agreement by parties to conduct business at some point in 
     the future, but on terms set forward today in the contract.

  *  A clause that the BUYER has the `option` of walking away from
     the deal, if they so choose, with no reprecussions or breach of
     contractual duty. (this is where options get their name)

  *  A clause that the SELLER has a contractual duty to do business
     with the BUYER should the BUYER choose to do so. In exchange
     for this 


 `Option` as the same thing as `contract`. Further, these contracts are 
 standardized with universal well defined and understood clauses and language 
 which allows the agreements to be easily transferred to others (third-parties) 
 without loss of contractual duty or value. Lastly, remember all options derive
 their value from the performance of the underlying asset over the life of the
 contract.

The two parties to these contracts are a BUYER (a.k.a going LONG) of the 
 contract who pays a price (aka a premium) and on the other side is the party
 WRITING the option (aka the SELLER, aka shorting) who collects the premium 
 the buyer paid. The contract is formed with the buyer purchasing certain 
 contractual rights for which the seller is contractually obligated to 
 fullfill.



'''
        print(f'{whatare_text}')
        return 

    # save repeating self.
    def __binomial_reminder(self):
        temp_string = f'''
Since this is a single period option where {self.underlying_name} starts at 
{self.underlying_value} and either moves up to {self.up_value} or down to 
{self.down_value} (and there are no other values {self.underlying_name}
can take) we only need to calculate the potential payoffs for 2 states. 
Now given this is a {self.position} {self.optype} all potential payoff can be 
described using the following mathematical relationship:'''
        return temp_string

    
    # function to keep the guide from being bloated.
    def __payoff_guide_helper(self):
        if self.position == 'Long':
            if self.optype == 'Call':
                temp_string = f''' 
    up_payoff = max(up_value - strike, 0)
    down_payoff = max(down_value - strike, 0)
    
    Plug in the respective values and find that

    up_payoff:   max({  self.up_value} - {self.strike_value}, 0) = {round(max(self.up_value -self.strike_value,0),2)}
    down_payoff: max({self.down_value} - {self.strike_value}, 0) = {round(max(self.down_value -self.strike_value,0),2)}'''

            else: #must be a put
                temp_string = f'''Long Put guide not finished'''

        else: # must be a short
            if self.optype == 'Call':
                temp_string = f'''Short Call guide not finished'''
            else: # must be a put
                temp_string = f'''Short Put guide not finished'''
        return temp_string

    
    
    def __guide_meta(self):
        if self.position == 'Long':
            if self.optype == 'Call':
                temp_string = f'''
The following guide is auto generated based on your inputs for a {self.position}
 {self.optype}. The method `.guide()` can also generate guides for Long Puts, 
 Short Calls, and Short Puts''' 
            
            else: #must be a put
                temp_string = f'''
The following guide is auto generated based on your inputs for a {self.position}
 {self.optype}. The method `.guide()` can also generate guides for Long Calls, 
 Short Calls, and Short Puts'''

        else: # must be a short
            if self.optype == 'Call':
                temp_string = f'''
The following guide is auto generated based on your inputs for a {self.position}
 {self.optype}. The method `.guide()` can also generate guides for Long Calls
 Long Puts, and Short Puts'''
            else: # must be a put
                temp_string = f'''
The following guide is auto generated based on your inputs for a {self.position}
 {self.optype}. The method `.guide()` can also generate guides for Long Calls,
 Long Puts, and Short Calls'''
        return temp_string

#test   
#example = SinglePeriodOption('Long','Call', 100, 110, 120, 90.25, 0.05)
#print(example.value)
#example = SinglePeriodOption('Short','Call', 100, 110, 120, 90.25, 0.05)
#print(example.value)
#example = SinglePeriodOption('Long','Put', 100, 110, 120, 90.25, 0.05)
#print(example.value)
#example = SinglePeriodOption('Short','Put', 100, 110, 120, 90.25, 0.05)
#print(example.value)
# cool, it works.

#additional tests.
example = SinglePeriodOption('Short','Call', 95.54, 107.89, 120.02, 90.25, 0.0342, 'TMNQQC')
example.guide()