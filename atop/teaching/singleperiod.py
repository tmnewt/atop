from math import sqrt, log, exp


class SinglePeriodOption:
    '''Single Period Binomial Option object

    Replicates part of the functionality of the BinomialOption class found 
    in the options directory. This class is newer and more simple to use. 
    Great for demonstrating single period binomial option pricing model 
    without having to worry about complex topics like volatility, actual
    probability, or time! This is only for educational purposes. '''

    def __init__(self, position: str, optype: str,
                    underlying_value: float or int,
                    strike_value: float or int, up_value: float or int,
                    down_value: float or int, risk_free: float or int,
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
    
    
    # part of reality checks
    def __volatility_calc(self):
        box = []
        box.append(1-sqrt(1+2*(self.risk_free-log(self.__up_factor())))) #works
        box.append(1+sqrt(1+2*(self.risk_free-log(self.__up_factor())))) #works...
        box.append(abs(1+sqrt(1+2*(self.risk_free-log(self.__dn_factor())))/-1)) 
        # equivalent to: sqrt( (1+(2*self.risk_free)) + 2*log(self.underlying_value/self.down_value))-1
        box.append((1+sqrt(1+2*(self.risk_free-log(self.__dn_factor()))))/-1) 
        # equivalent to: -sqrt( (1+(2*self.risk_free)) + 2*log(self.underlying_value/self.down_value))-1
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

    
    # Part of reality checks
    # Put call parity check. Can't check when positions are short... yet.
    def put_call_parity_check(self):
        if self.optype == 'Call':
            flip_pos = 'Put'
        else:
            flip_pos = 'Call'
        flip = SinglePeriodOption('Long',flip_pos, self.underlying_value, 
                                                 self.strike_value, 
                                                 self.up_value,
                                                 self.down_value,
                                                 self.risk_free)
        if self.optype == 'Call':
            check = (flip.get_value() + self.underlying_value
                    -self.strike_value/(1+self.risk_free)
                    -self.get_value())
        # main must be a put
        else:
            check = (self.get_value() + self.underlying_value
                    -self.strike_value/(1+self.risk_free)
                    -flip.get_value())
        print(f'''
            Passes put-call-parity check when:
            put + underlying = PV(strike) + call
               
               rearrange
            
            put + underlying - PV(strike) - call = 0
            
            Calculated value is: {round(check,8)}
            ''')
    
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
                print(f'Problem\'s down factor: {round(self.__dn_factor(),4)}')
                print(f'Hedge Ratio (a.k.a units of underlying): {round(self.hedge_ratio,4)}')
                print(f'Value of bond position for hedging purposes: $ {round(self.rf_units,4)}')
                print(f'Risk-neutral probability for up state is {round(self.up_risk_neutral_prob,4)}')
                print(f'Risk-neutral probability for down state is {round(self.down_risk_neutral_prob,4)}')
        print('____________________________________________________________\n')






    # Everything below here probably needs to find its way to its own file.
    # But before doing that, it should be finished.
    # ahhhhhhhh this complete guide is taking forever to finish!
    # I hate strings...
    def guide(self, hide_intro = False, 
                    hide_what_is_an_option = False,):

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

WARNING: all versions of this guide are still being worked on.''')
        
        if hide_intro:
            pass
        
        # Intro string chunk
        else:
            print('''
 ----------
   Intro  
 ----------
This guide aims to provide users with a complete walkthrough of calculating 
 the fair price (today's price) for a single period binomial option.
 I hope to help those looking to dive deep into the subject of options. The 
 guide goes all in, meticulously walking through every step of the process
 guiding the user to the solution. At times it can come accross as
 handholding and repetitive. But I argue that this is necessary as there are
 too many concepts and values to keep track. Sometimes we just need an 
 organized and thorough method of logically walking through problems. Lastly:
 the key feature of this guide is that it is dynamic and handles long calls,
 long puts, short calls, and short puts!

Some housekeeping first:

The guide uses the terms `price` and `value` interchangablely. They are the 
 same thing. Additionally, you might see the program produce negative currency
 values. For instance, you may see the calculated value for a short call be,
 say, $ -2.50. Which seems weird. How can a price be negative? This is simply 
 an accounting style chosen to give logical consistency to the transactions. 
It will become important later for correctly describing replicating portfolios''')
        #End of intro string chunk


        if hide_what_is_an_option:
            pass
        else:
            self.__whatare_guide()
        
        
        print('\n******************')
        print(f'  Walkthrough')
        print('******************')
        # Taking about the problem chunk
        print(f'''
Stating the problem:

There is a single period {pos} {opt} on the asset {name} whose current 
 price is ${under}, with a strike price of ${strike}. 
 Next period {name}\'s price will either be ${up}, 
 or ${down}, next period. The current risk-free rate is {rf}

What is the fair price for this {pos} {opt} today? 

First step is to find the payoff states for the next period.
 A single period binomial option follows a 2-state model. 
 Imagine there are only 2 possible future states of value for the 
 underlying asset {name}: An `up` state where {name}\'s price is {up}
 and a down state where {name}\'s price is {down}.

        You might be wondering, where do these values come from? How do 
        we know {name} will move exactly to these values? The simple answer
        is that it is just an example. But a more fitting answer would be, 
        \'it\'s complicated...\' It will be addressed later, I promise.
        But, for now let's just settle with these `magic` numbers. 
        One thing at a time.

Now, the 2 standard types of options are: CALLs and a PUTs. 
Additionally, the 2 sides to this trade: a buyer and seller. 
 
 * Remember, this generated guide focuses on {self.optype}. 
   To see the walkthrough from a different perspective change the 
   `position` and the `op_type` arguments.''')
        # End of string chunk
        
        
        # logic for each type and each possible position.
        if self.position == 'Long':
            print(f'''
\nIn this problem we are going long, meaning we are purchasing a
{opt} option on {name}.''')
            
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
 Or, after exercising the option  you could just keep {name}, happy that you
 acquired it for a cheaper price.''')

              
                print(f'''
Second, this contract requires NO OBLIGATION on your part to buy 
 {name} at ${strike}. If {name}\'s price remains lower than the strike 
 price of ${strike} then you are free to walk away! While {name}\'s price < 
 ${strike} then this contract becomes worth less and less. If the contract
 matures and {name}\'s price < ${strike} the value of this contract is 0. 
 Had you bought this contract you would only be out the premium you paid.
 Compare that to outright buying the underlying asset in which case you
 would sustain further losses. 
    
These features are what make long call options special. Holders of a long 
 call option simultaneously have no participation in the performance of 
 {name}, yet can benifit if {name} does well, but are not hurt should 
 {name}\'s value fall.  Therefore this long call option has significant
 upside potential and the only downside is the price you pay for the 
 option today. 

{self.__binomial_reminder()} 

payoffs = max( underlying_given_state - strike, 0)

Which translates to:
{self.__payoff_guide_helper()}


Long Call guide not finished''')

            else: # must be a put
                print(f'''
Buying a PUT gives you the RIGHT but NOT AN OBLIGATION to SELL the underlying
 asset ({name}) for the strike price of ${strike} upon exercising the option.
 {name}\'s value is currently trading at ${under}.
 
        We cannot stress these facts enough! People easily confuse 
        puts with shorting stocks (likely because of its similarites 
        in the payoff diagrams. That and because the term SELL is 
        used in describing a key feature of a put.)

 First, unlike a long call you are not paying for the right to potentially
 purchase {name} at {strike} but instead payinf for the right to potentially
 SELL {name} at {strike}. The counter party that sold you this put option on
 {name} is now obligated 
 
  because you have the RIGHT to purchase {name} at ${strike}, if {name} 
 moves higher than the contract's strike price of ${strike} then the value 
 of this call option (that is, its price) increases. To restate, when 
 {name}\'s price > ${strike} this contract becomes more valuable! If the 
 contract matures and {name}\'s price > ${strike} then the value of the 
 contract is the difference in {name}\'s price - strike.
 
MISSING STUFF HERE!!!
{self.__binomial_reminder()}

payoffs = max( strike - underlying_given_state, 0)

Which translates to:
{self.__payoff_guide_helper()}


Long Put guide not finished''')


        else: # must be a short
            if self.optype == 'Call':
                print(f'''

MISSING STUFF HERE FOR SHORT CALL GUIDE!!!
{self.__binomial_reminder()}
payoffs = -max( underlying_given_state - strike, 0)

Which translates to:
{self.__payoff_guide_helper()}

Short Call guide not finished
''')
            else: # must be a put
                print(f'''

MISSING STUFF HERE FOR SHORT PUT GUIDE!!!
{self.__binomial_reminder()}

payoffs = -max( strike - underlying_given_state, 0)

Which translates to:
{self.__payoff_guide_helper()}

Short Put guide not finished''')
        

        #print('\n Sanity Check')
        #print(self.volatility)
        #print('Up factor: {}'.format(self.__sanity_check(self.volatility[0])[0]))
        #print('Up factor: {}'.format(self.__sanity_check(self.volatility[1])[0]))
        #print('Dn factor: {}'.format(self.__sanity_check(self.volatility[2])[1]))
        #print('Dn factor: {}'.format(self.__sanity_check(self.volatility[3])[1]))
        
        
        print('___________________________________________________\n')
    # End of guide class method

    def __whatare_guide(self):
        
        #whatare_options string chunk
        whatare_text = f'''
--------------------
 What are options?  
--------------------
All options are contractual agreements between two parties.
  Typically these contractual agreements are based on European, English,
  and American contract and business law. Like generic contracts, 
  options also derive their value from the performance of the parties 
  to the contract. But, it is the unique contractual structure 
  of these particular contracts which make options noteworthy.
 
Some `universal` contractual features unique to options:
  *  An agreement by parties to perform some obligation at some point in 
     the future (typically within 1 year), but on terms set forth today.

  *  An agreement that the BUYER has the `option` of walking away from
     the deal, if they so choose, with no reprecussions or breach of
     contractual duty. (this is where options get their name).

  *  An agreement that the SELLER has a contractual duty to perform some 
     obligation for the BUYER should the BUYER deemand performance from 
     the Seller. 

  *  In exchange for this agreement the buyer pays some value to the
     seller today for seller\'s promise to perform.   

  ^^^^^This is pretty much all options are!

Further, the option contracts you would find by Googling the term
 `financial options` are standardized types with universally 
 agreed upon clauses/legalese which allow such options to be 
 easily bought and sold to others (third-parties) without loss 
 of contractual duty and value.

To reiterate:
    * Options are contracts
    * These contracts have value
    * Options have unique features when it comes to contracts
        * Specifically the buyer\'s choice to exit the contract
    * There are 2 parties to the deal
    * a BUYER (a.k.a going LONG) of the contract 
        * who pays some value (aka the premium) 
    * a SELLER (aka the UNDERWRITER, aka shorting) 
        * who collects the premium from the buyer. 
    * These contracts are standardized and can be traded'''
        #End of whatare_options string chunk
        print(f'{whatare_text}')
        return 

    # save repeating self.
    def __binomial_reminder(self):
        temp_string = f'''
The big question is: How much should we pay for this contract? 
What is this deal worth today?

To start, we begin by identifying the potential payoff states, which are
vital to correctly pricing the contract.

Since this is a single period option where {self.underlying_name} starts at 
 {self.underlying_value} and either moves up to {self.up_value} or down to 
 {self.down_value} (and there are no other values {self.underlying_name}
 can take) we only need to calculate the potential payoffs for 2 states. 
 Now given this is a {self.position} {self.optype} the potential payoff
 values can be  described using the following mathematical relationship:'''
        return temp_string

    
    # function to keep the guide from being bloated.
    def __payoff_guide_helper(self):
        if self.position == 'Long':
            if self.optype == 'Call':
                temp_string = f''' 
    up_payoff = max(up_value - strike, 0)
    down_payoff = max(down_value - strike, 0)
    
    Plug in the respective values and find that,

    up_payoff:   max({  self.up_value} - {self.strike_value}, 0) = {round(max(self.up_value -  self.strike_value,0),2)}
    down_payoff: max({self.down_value} - {self.strike_value}, 0) = {round(max(self.down_value -self.strike_value,0),2)}'''

            else: #must be a put
                temp_string = f'''
    up_payoff = max(strike - up_value, 0)
    down_payoff = max(strike - down_value, 0)
    
    Plug in the respective values and find that,

    up_payoff:   max({self.strike_value} - {self.up_value  }, 0) = {round(max(self.strike_value -  self.up_value,0),2)}
    down_payoff: max({self.strike_value} - {self.down_value}, 0) = {round(max(self.strike_value -self.down_value,0),2)}'''

        else: # must be a short
            if self.optype == 'Call':
                temp_string = f'''
    up_payoff =   -max(up_value - strike, 0)
    down_payoff = -max(down_value - strike, 0)
    
    Plug in the respective values and find that,

    up_payoff:   -max({  self.up_value} - {self.strike_value}, 0) = {-round(max(self.up_value -  self.strike_value,0),2)}
    down_payoff: -max({self.down_value} - {self.strike_value}, 0) = {-round(max(self.down_value -self.strike_value,0),2)}'''
            
            else: # must be a put
                temp_string = f'''
    up_payoff = max(strike - up_value, 0)
    down_payoff = max(strike - down_value, 0)
    
    Plug in the respective values and find that,

    up_payoff:   -max({self.strike_value} - {self.up_value  }, 0) = {-round(max(self.strike_value -  self.up_value,0),2)}
    down_payoff: -max({self.strike_value} - {self.down_value}, 0) = {-round(max(self.strike_value -self.down_value,0),2)}'''
        return temp_string
    # end of __payoff_guide_helper()


    def __guide_hedge(self):
        return

    


    def __guide_rf_units(self):
        return


    def __guide_pricing(self):
        return
    
    




    def __guide_meta(self):
        if self.position == 'Long':
            if self.optype == 'Call':
                temp_string = f'''
The following guide is auto generated based on your inputs for
a {self.position} {self.optype}. The method `.guide()` can also 
generate guides for Long Puts, Short Calls, and Short Puts.
To see those guides change the `position` and `op_type` 
arguments.''' 
            else: #must be a put
                temp_string = f'''
The following guide is auto generated based on your inputs for 
a {self.position} {self.optype}. The method `.guide()` can also 
generate guides for Long Calls, Short Calls, and Short Puts.
To see those guides change the `position` and `op_type` 
arguments'''
        else: # must be a short
            if self.optype == 'Call':
                temp_string = f'''
The following guide is auto generated based on your inputs for 
a {self.position} {self.optype}. The method `.guide()` can also 
generate guides for Long Calls, Long Puts, and Short Puts.
To see those guides change the `position` and `op_type` 
arguments'''
            else: # must be a put
                temp_string = f'''
The following guide is auto generated based on your inputs for 
a {self.position} {self.optype}. The method `.guide()` can also 
generate guides for Long Calls, Long Puts, and Short Calls.
To see those guides change the `position` and `op_type` 
arguments'''
        return temp_string
    #end of __guide_meta()





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
example = SinglePeriodOption('Short','Put', 95.54, 107.89, 120.02, 90.25, 0.0342)
example.solution()
example = SinglePeriodOption('Short','Call', 95.54, 107.89, 120.02, 90.25, 0.0342)
example.solution()

example.put_call_parity_check()

#example.solution()
#example.guide( hide_intro= True ,hide_what_is_an_option=True)







# JUNKYARD

# SOME STUFF ON LONG CALL. dropped because of references to time.
#To reiterate, when {name}\'s price > ${strike} this contract becomes 
#more valuable! If the 
#contract matures and {name}\'s price > ${strike} then the value of the 
#contract is the difference in {name}\'s price - strike.